from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

MODEL_NAME = "prithivida/grammar_error_correcter_v1"

# Load once at startup
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

# CPU safe
device = torch.device("cpu")
model.to(device)


def correct_grammar(text: str) -> str:
    """
    Correct grammar using T5 model
    """
    if not text.strip():
        return text

    input_text = "gec: " + text

    input_ids = tokenizer.encode(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=256
    ).to(device)

    outputs = model.generate(
        input_ids,
        max_length=256,
        num_beams=4,
        early_stopping=True
    )

    corrected_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return corrected_text
