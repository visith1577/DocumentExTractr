# from datetime import datetime
from pydantic import UUID4, BaseModel


class LivenessResponse(BaseModel):
    status: str


class ClassifyResponse(BaseModel):
    doc_id: UUID4
    type: str


class ExtractResponse(BaseModel):
    document_type: str
    extraction_results: dict[str, str]


class OcrResponse(BaseModel):
    ocr_output: str


# class ResumeExtractResponse(BaseModel):
#     name: str
#     emails: str
#     phones: list[str]
#     addresses: list[str]
#     websites: list[str]
#     social_profiles: dict[str, str]
#     skills_categorized: dict[str, list[str]]
#     experience_insights: list[dict[str, str]]
#     achievement_metrics: list[dict[str, str]]
#     career_progression: dict[str, str]
#     personality_traits: list[str]

# class Stakeholder(BaseModel):
#     name: str
#     role: str

# class Intent(BaseModel):
#     primary_intent: str | None = None
#     secondary_intent: str | None = None
#     optional_intent: str | None = None

# class EmailExtractionResponse(BaseModel):
#     email_from: str
#     email_to: list[str]
#     cc: list[str]
#     bcc: list[str]
#     subject: str
#     date: datetime
#     body: str
#     attachments: list[str]
#     emotional_tone: dict[str, float]
#     intent_hierarchy: list[dict[str, str]]
#     action_items: list[str]
#     stakeholders: list[Stakeholder]
#     follow_up_required: bool
#     priority_level: str
#     relationship_context: str
