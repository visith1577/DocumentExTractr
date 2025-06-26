from paddleocr import PaddleOCR
from helper import normalize_box
from PIL import Image
from paddleocr import PPStructureV3


ocr = PaddleOCR(
    use_doc_orientation_classify=True,
    use_doc_unwarping=True,
    use_textline_orientation=True
)

pipeline = PPStructureV3(
    use_chart_recognition=False # this model is deactivated for easier setup
)

def apply_ocr(examples: list[str]) -> list[str]:
    words: list[str] = []
    for example in examples:
      image = Image.open(example).convert("L")
      width, height = image.size

      # Run PaddleOCR
      result = ocr.predict(example) # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

      doc_words: list[str] = []
      boxes = []

      ocr_data = result[0] # pyright: ignore[reportUnknownVariableType]

      # Get texts and boxes from the OCR result
      rec_texts: dict[str, str] = ocr_data['rec_texts'] # pyright: ignore[reportUnknownVariableType]
      rec_boxes = ocr_data['rec_boxes'] # pyright: ignore[reportUnknownVariableType]

      for i, text in enumerate(rec_texts): # pyright: ignore[reportUnknownArgumentType]
          if not text.strip():
              continue

          box = rec_boxes[i] # pyright: ignore[reportUnknownVariableType]

          # Ensure box has 4 coordinates
          if len(box) == 4: # pyright: ignore[reportUnknownArgumentType]
              box = [int(coord) for coord in box] # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
              norm_box = normalize_box(box, width, height)
              doc_words.append(text)
              boxes.append(norm_box)  # pyright: ignore[reportUnknownMemberType]
      words.append(" ".join(doc_words))

    return words

def apply_structured(path: str, document_type: str)-> str:
    match document_type:
        case "resume":
            output = pipeline.predict( # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
                input=path,
                use_doc_orientation_classify=True,
                use_doc_unwarping=True,
                use_table_recognition=True,
                use_seal_recognition=False,
                use_textline_orientation=True,
            )
        case "scientific_publication":
            output = pipeline.predict( # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
                input=path,
                use_doc_orientation_classify=True,
                use_doc_unwarping=True,
                use_chart_recognition=True,
                use_table_recognition=True,
                use_seal_recognition=True,
                use_textline_orientation=True,
                use_formula_recognition=True,
                use_table_orientation_classify=True
            )

        case "email":
            output = pipeline.predict( # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
                input=path,
                use_doc_orientation_classify=True,
                use_doc_unwarping=True,
                use_seal_recognition=True,
                use_textline_orientation=True,
            )

        case _:
            output = pipeline.predict( # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
                input=path,
                use_doc_orientation_classify=True,
                use_doc_unwarping=True,
                use_textline_orientation=True,
            )

    markdown_list: list[str] = []

    for res in output: # pyright: ignore[reportUnknownVariableType]
        md_info = res.markdown # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        markdown_list.append(md_info) # pyright: ignore[reportUnknownArgumentType]

    markdown_texts: str = pipeline.concatenate_markdown_pages(markdown_list) # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    return markdown_texts # pyright: ignore[reportUnknownVariableType]