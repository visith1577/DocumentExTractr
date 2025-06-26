from datetime import datetime
from typing import Literal
import dspy


class ResumeExtraction(dspy.Signature):
    """
    Extract the relevant information from text of resume through ocr.
    Output provide the relevant categories if available from the text.
    """

    resume_text: str = dspy.InputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    # output
    name: str = dspy.OutputField(desc="who's resume is it?")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    emails: str = dspy.OutputField(desc="personal email")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    phones: list[str] = dspy.OutputField(desc="personal phone number")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    addresses: list[str] = dspy.OutputField(desc="personal address")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    websites: list[str] = dspy.OutputField(desc="related websites")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    social_profiles: dict[str, str] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="social media name as key : profile link as value."
    )

    skills_categorized: dict[str, list[str]] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="set of skills extracted from resume and categorised."
    )
    experience_insights: list[dict[str, str]] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="list of experiences from each institution/organisation/project"
    )
    achievement_metrics: list[dict[str, str]] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="metric infomation from achievements."
    )
    career_progression: dict[str, str] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="career progress timeline/ duration per position."
    )
    personality_traits: list[str] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="personality traits observed or mentioned."
    )


class EmailExtraction(dspy.Signature):
    """Enhanced email data needs to be extracted from the email text exctracted via ocr"""

    email_text: str = dspy.InputField(desc="Input data")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    # output
    email_from: str = dspy.OutputField(desc="sender email")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    email_to: list[str] = dspy.OutputField(desc="receipient emails")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    cc: list[str] = dspy.OutputField(desc="receipient emails carbon copy")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    bcc: list[str] = dspy.OutputField(desc="receipient emails blind carbon copy")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    subject: str = dspy.OutputField(desc="email subject")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    date: datetime = dspy.OutputField(desc="email sent date")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    body: str = dspy.OutputField(desc="email body")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    attachments: list[str] = dspy.OutputField(desc="mentioned attachements")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    emotional_tone: dict[str, float] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="professional, friendly ... etc."
    )
    intent_hierarchy: list[dict[str, str]] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="primary, secondary and optional intents."
    )
    action_items: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    stakeholders: list[dict[str, str]] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    follow_up_required: bool = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    priority_level: Literal["low", "medium", "high"] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    relationship_context: str = dspy.OutputField(desc="what is the email related to ?")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]


class ScientificPaperExtractaction(dspy.Signature):
    """Extract scientific paper data with LLM insights from the ocr extracted scientific publication data."""

    scipub_text: str = dspy.InputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    # output
    title: str = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="title or best description of the scientific publication."
    )
    authors: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    affiliations: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    abstract: str = dspy.OutputField(desc="abstract of the paper")  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    keywords: list[str] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="most impactful words/tokens in the paper."
    )
    sections: dict[str, str] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="breakdown of the sections in the paper."
    )
    citations: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    references: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    figures_tables: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    doi: str = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    journal: str = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    publication_date: datetime = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    research_contribution: dict[str, str] = dspy.OutputField(  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
        desc="who and what was contributed. provide the who as key and what as value."
    )
    methodology_type: str = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    research_gaps_identified: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    future_work_suggestions: list[str] = dspy.OutputField()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
