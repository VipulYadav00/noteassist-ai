from transformers import BartForConditionalGeneration, BartTokenizer
import torch

MODEL_NAME = "facebook/bart-large-cnn"

# Load once at startup
tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

device = torch.device("cpu")
model.to(device)


def summarize_text(text: str, max_length: int = 130) -> str:
    """
    Generate abstractive summary using BART
    """
    if not text or len(text.split()) < 20:
        # Too short to summarize meaningfully
        return text

    inputs = tokenizer.encode(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(device)

    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return summary
