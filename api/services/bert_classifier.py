from transformers import BertTokenizer, BertForSequenceClassification
import torch

IDX2LABEL: dict[int, str] = {0: "resume", 1: "email", 2: "scientific_publication"}

tokenizer: BertTokenizer = BertTokenizer.from_pretrained( # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    "visithck/Bert-Based-Docu-classify"
)  
model: BertForSequenceClassification = BertForSequenceClassification.from_pretrained( # pyright: ignore[reportUnknownMemberType]
    "visithck/Bert-Based-Docu-classify", num_labels=3
)  

if torch.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

_ = model.to(device)  # pyright: ignore[reportUnknownMemberType,reportArgumentType]
_ = model.eval()


def classify_document_text(doc_text: str) -> str:
    inputs = tokenizer(doc_text, padding=True, truncation=True, return_tensors="pt").to(
        device
    )
    input_ids = inputs.input_ids  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]
    attention_mask = inputs.attention_mask  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType]

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)  # pyright: ignore[reportAny]
        logits = outputs.logits  # pyright: ignore[reportAny]

    predicted_class_index = torch.argmax(logits, dim=1).item()  # pyright: ignore[reportAny]

    # Convert the predicted index back to the label
    predicted_label: str = IDX2LABEL.get(predicted_class_index, "Unknown")  # pyright: ignore[reportCallIssue, reportArgumentType, reportUnknownVariableType]

    return predicted_label  # pyright: ignore[reportUnknownVariableType]
