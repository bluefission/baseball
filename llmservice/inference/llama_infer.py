import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
from guidance import models, guidance, gen, user, system, assistant, select
import re

model_name = "meta-llama/Llama-3.2-1B-Instruct"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map=None
)
model.to("cuda")

# Log GPU setup
print("[INFO] CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("[INFO] CUDA device:", torch.cuda.get_device_name(0))
    print("[INFO] CUDA memory allocated:", torch.cuda.memory_allocated() // 1024**2, "MB")
    print("[INFO] CUDA memory reserved:", torch.cuda.memory_reserved() // 1024**2, "MB")
    for name, param in model.named_parameters():
        if not param.is_cuda:
            print(f"[WARNING] Model parameter {name} is NOT on CUDA!")

# Wrap model for guidance
# llm = models.Transformers(model=model, tokenizer=tokenizer)

def get_fresh_llm():
    return models.Transformers(model=model, tokenizer=tokenizer)

# Run the generation function
def run_generate_response(prompt: str) -> dict:
    start_time = time.time()

    stop_token = tokenizer.decode(tokenizer.encode("\n")[0])

    llm = get_fresh_llm()
    with system():
        lm = llm + f"""\
        You are a helpful assistant that generates structured summaries
        about baseball player statistics.
        """

    with user():
        lm += f"""{prompt}"""
        lm += "\nDraft a brief summary of the player's performance: "

    with assistant():
        lm += "In brief, "
        lm += gen('summary', max_tokens=120, temperature=0.3, stop=[stop_token, "\n", "<|end|>", "<|im_end|>"])

    with user():
        lm += "\nList 2 of their specific strengths?: "
    with assistant():
        lm += "Two of his specific strengths are "
        lm += gen('strengths', max_tokens=20, temperature=0.3, stop=[stop_token, "\n", "<|end|>", "<|im_end|>"])

    with user():
        lm += "Two of his specific weaknesses are "
        lm += "\nList 2 of their specific weaknesses?: "
    with assistant():
        lm += gen('weaknesses', max_tokens=20, temperature=0.3, stop=[stop_token, "\n", "<|end|>", "<|im_end|>"])

    with user():
        lm += "\nIn one sentence suggest a strategy for this player moving forward?: "
    with assistant():
        lm += "This player should "
        lm += gen('strategy', max_tokens=50, temperature=0.8, stop=[stop_token, "\n", "<|end|>", "<|im_end|>"])
    
    end_time = time.time()
    print("[INFO] Inference completed in", round(end_time - start_time, 2), "seconds.")
    if torch.cuda.is_available():
        print("[INFO] CUDA memory post-inference:", torch.cuda.memory_allocated() // 1024**2, "MB")

    
    return {
        "strengths": lm["strengths"],
        "weaknesses": lm["weaknesses"],
        "strategy": lm["strategy"],
        "summary": lm["summary"]
    }
