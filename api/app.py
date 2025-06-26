from logging import Logger
from uuid import uuid4
from pydantic import UUID4
from starlette.status import (
    # HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from fastapi import BackgroundTasks, FastAPI, File, HTTPException, UploadFile

import httpx
from config import get_settings
from services.lm_extractor import Extractor
from model import ClassifyResponse, ExtractResponse, LivenessResponse, OcrResponse
from services.bert_classifier import classify_document_text

app = FastAPI()
settings = get_settings()
inmemory_doc_cache: dict[str, str] = {}
extractor = Extractor()
logger = Logger(name="main-api-logger")


async def call_structured_ocr_and_cache(
    doc_id: UUID4,
    doc_type: str,
    files_data: list[tuple[str, tuple[str | None, bytes, str | None]]],
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"http://0.0.0.0:3002/structured-ocr/{doc_type}",
                files=files_data,
            )
            logger.info(f"ocr structured output: {response.json()}")
            status = response.raise_for_status().status_code
            if status != 200:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail="OCR processing failed"
                )
            ocr_response = OcrResponse(**response.json())  # pyright: ignore[reportAny]
            ocr_output = ocr_response.ocr_output
            inmemory_doc_cache[str(doc_id)] = ocr_output
    except Exception as e:
        logger.warning(f"error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.post("/classify-docs", response_model=ClassifyResponse)
async def doc_classifier(
    background_tasks: BackgroundTasks, files: list[UploadFile] = File(...)  # pyright: ignore[reportCallInDefaultInitializer]
): 
    try:
        doc_id = uuid4()
        status = 200
        ocr_result = ""
        files_data = []
        try:
            files_data = [
                ("files", (file.filename, await file.read(), file.content_type))
                for file in files
            ]
            async with httpx.AsyncClient() as client:
                ocr_response = await client.post(
                    "http://0.0.0.0:3002/ocr",
                    files=files_data,
                )
                logger.info(f"ocr response: {ocr_response.json()}")
                status = ocr_response.raise_for_status().status_code
                ocr_response = OcrResponse(**ocr_response.json())  # pyright: ignore[reportAny]
                ocr_result = ocr_response.ocr_output

        except Exception as e:
            raise HTTPException(
                status_code=status, detail=f"OCR service failed: {str(e)}"
            )

        if ocr_result == "":
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST, detail="OCR result empty"
            )

        document_type = classify_document_text(ocr_result)
        logger.info(f"document type: {document_type}")
        background_tasks.add_task(
            call_structured_ocr_and_cache, doc_id, document_type, files_data
        )

        return ClassifyResponse(doc_id=doc_id, type=document_type)
    except Exception as e:
        logger.warning(f"error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.get("/extraction/{doc_type}/{doc_id}", response_model=ExtractResponse)
async def retrieve_extraction(doc_type: str, doc_id: UUID4):
    try:
        ocr_output = inmemory_doc_cache.get(str(doc_id))
        if ocr_output is None:
            raise HTTPException(status_code=404, detail="Extraction not ready")

        extraction = extractor.get_extraction(doc_type, ocr_output) # pyright: ignore[reportUnknownVariableType]
        logger.info(f"document extraction results: {extraction}")
        return ExtractResponse(
            document_type="document", extraction_results=extraction # pyright: ignore[reportArgumentType]
        )
    except Exception as e:
        logger.warning(f"error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")


@app.get("/live", response_model=LivenessResponse)
def liveness():
    try:
        return LivenessResponse(status=str(HTTP_200_OK))
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
