import dspy

from config import get_settings
from model.dspy_signatures import (
    ResumeExtraction,
    EmailExtraction,
    ScientificPaperExtractaction,
)

settings = get_settings()

lm = dspy.LM(
    settings.model_name, api_base=settings.model_url, api_key=settings.model_api_key
)
dspy.configure(lm=lm)  # pyright: ignore[reportAny]


class Extractor:
    def __init__(self):
        self.resume_extractor: dspy.Predict = dspy.Predict(ResumeExtraction)
        self.email_extractor: dspy.Predict = dspy.Predict(EmailExtraction)
        self.scipub_extractor: dspy.Predict = dspy.Predict(ScientificPaperExtractaction)

    def get_extraction(self, doc_type: str, doc_text: str):  # pyright: ignore[reportUnknownParameterType]
        match doc_type:
            case "resume":
                ex = self.resume_extractor(resume_text=doc_text)  # pyright: ignore[reportUnknownVariableType]
                return ex.toDict()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            case "scientific_publication":
                ex = self.scipub_extractor(scipub_text=doc_text)  # pyright: ignore[reportUnknownVariableType]
                return ex.toDict()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            case "email":
                ex = self.email_extractor(email_text=doc_text)  # pyright: ignore[reportUnknownVariableType]
                return ex.toDict()  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
            case _:
                return "Unknown document type."
