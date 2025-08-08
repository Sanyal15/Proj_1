import pandas as pd
import json
import requests

def build_prompt(df: pd.DataFrame, num_rows: int = 3) -> str:
    # Convert sample rows to JSON-serializable format
    sample = df.head(num_rows).copy()

    # Convert any Timestamp or non-serializable types
    for col in sample.columns:
        if pd.api.types.is_datetime64_any_dtype(sample[col]):
            sample[col] = sample[col].astype(str)
        elif pd.api.types.is_timedelta64_dtype(sample[col]):
            sample[col] = sample[col].astype(str)

    sample_rows = sample.values.tolist()
    columns = sample.columns.tolist()

    prompt = f"""
You are an AI trained to classify business datasets into industries.
Given the following column headers and a few sample rows, identify the most likely industry.

Only respond with one of these categories:
["E-commerce", "Finance", "Pharmaceuticals", "Logistics", "Manufacturing", "Education", "Media", "HR", "Insurance", "SaaS"]

Columns: {columns}
Sample rows:
{json.dumps(sample_rows, indent=2)}

Return just the industry name.
"""
    return prompt.strip()

def detect_industry(df: pd.DataFrame, model_url: str = "http://localhost:11434/api/generate") -> str:
    prompt = build_prompt(df)

    # Call Ollama/Mistral locally
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(model_url, json=payload)
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        return f"Error: {e}"
