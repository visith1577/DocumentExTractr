# OCR API service
### Main components
This is mainly built using PaddleOCR. After careful testing of different ocr models, namely pyteseract, paddlepaddle, easyocr and docling + smoldocling paddleocr was determined as the more superior choice. 

- docling + smoldocling : Goto choice if all data were pdfs
- In this i assume that all incoming are images (pdfs will be converted to jpeg)
- PaddleOCR was used for OCR, specifically the PP-OCRv5 for document classification and PP-StructureV3 for first phase of structured data collection
- Noteble reasons for choice were
    - Better capturing of charts and tables
    - orientation and image warping fixes are applied in model pipeline
    - textline orientation capabilities
    - multilingual capabilities
    - table recognition
    - seal recognition
    - formulae recognition
    - native convert to markdown capability
    
    **cons**
    - Consist of pipeline of several models, need a relatively powerful gpu for hosting

### Reasons why OCR was it's own service
- Individual scalability
- OCR specifically requires GPU
- Conflicting python dependancies and lack of uv support makes it difficult to manage if placed with rest of application


## steps to setup OCR API service
- follow below guidlines for installation of paddleocr in your environment. GPU is recommended.
*from personal use CPU tend to take 20 - 30 min so highly recommend switching to GPU*
**(Installation guidelines for PaddlePaddle)[https://www.paddlepaddle.org.cn/documentation/docs/en/install/index_en.html]** 
- install requirements using pip (recommend to create virtual environment)
- source .venv/bin/activate 
- install paddleocr with .venv is activates 

### install requirements
```bash
pip install -r requirements.txt
```

### start application server
```bash
fastapi run app:app --host 0.0.0.0 --port 3002
```
*This will start a fastapi server in port 3002*

> [!NOTE]
> BasedPyright is used for python type checking 

> [!TIP]
> for swagger docs goto http://127.0.0.1:3002/docs 