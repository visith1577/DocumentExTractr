import os
import shutil
import tempfile
from pydantic import BaseModel
from ocr import apply_ocr, apply_structured
from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

class OcrResponse(BaseModel):
    ocr_output: str


@app.post("/ocr", response_model=OcrResponse)
async def ocr_prediction(images: list[UploadFile] = File(...)): # pyright: ignore[reportCallInDefaultInitializer]
    # Read image bytes
    temp_dir = tempfile.mkdtemp()
    image_paths: list[str] = []
    try:
        for image in images:
            if image.filename is not None:
                file_path: str = os.path.join(temp_dir, image.filename) 
                with open(file_path, "wb") as f:
                    content = await image.read()
                    _ = f.write(content)
                image_paths.append(file_path)
        extracted_texts = apply_ocr(image_paths)
        extracted_texts = [text.replace("\n", ' ') for text in extracted_texts]
        return OcrResponse(ocr_output=" ".join(extracted_texts))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
    finally:
        shutil.rmtree(temp_dir)



@app.post("/structured-ocr/{doc_type}", response_model=OcrResponse)
async def structured_ocr(doc_type: str, images: list[UploadFile] = File(...)): # pyright: ignore[reportCallInDefaultInitializer]
    # Read image bytes
    temp_dir = tempfile.mkdtemp()
    image_paths: list[str] = []
    try:
        for image in images:
            if image.filename is not None:
                file_path: str = os.path.join(temp_dir, image.filename) 
                with open(file_path, "wb") as f:
                    content = await image.read()
                    _ = f.write(content)
                image_paths.append(file_path)
        extracted_texts = apply_structured(image_paths[0], doc_type)
        return OcrResponse(ocr_output=extracted_texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR processing failed: {str(e)}")
    finally:
        shutil.rmtree(temp_dir)