import requests, re, json
from typing import List

TANDEMN_URL = "https://api.tandemn.com/api/v1/chat/completions"
MODEL_ID    = "Qwen/Qwen3-32B-AWQ"

_session = requests.Session()

def _post_tandemn(messages: list, api_key: str) -> str:
    """Call Tandemn and return assistant content as plain text, sanitized."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": 0.3,
        "top_p": 0.9,
        "max_tokens": 800,
        "response_format": {"type": "json_object"}
    }
    r = _session.post(TANDEMN_URL, headers=headers, json=payload, timeout=40)
    r.raise_for_status()
    txt = r.json()["choices"][0]["message"]["content"]
    txt = re.sub(r"<.*?>", "", txt, flags=re.S)
    txt = re.sub(r"```(?:json|txt|markdown)?", "", txt).strip()
    return txt

def break_down_financial_question(user_input: str, api_key: str) -> List[str]:
    """
    Given a natural language financial question (comparison, standalone, or general),
    return a list of 5–10 focused sub-questions that can be answered using SEC filings
    or structured financial data (for use in RAG).

    Returns:
        List[str]: A list of standalone or comparative sub-questions (not templates).
    """
    messages = [
        {
            "role": "system",
            "content": (
                'Your job is to break down financial analysis prompts into 5 to 10 specific, '
                'factual sub-questions that can each be answered from structured financial filings '
                '(e.g. 10-Ks, or income statements). '
                'You must return only the sub-questions. '
                'Don\'t give a subquestion with a specific year unless a year is given'
                'Each question should be clear, grounded in data (e.g., revenue, net income, R&D), '
                'and answerable from financial reports. Include comparisons if asked. '
                'No markdown, no numbering, no extra text. '
                'Return JSON only: {"sub_questions": ["...", "...", "..."]}'
            )
        },
        {
            "role": "user",
            "content": f"Prompt: {user_input}"
        }
    ]

    raw = _post_tandemn(messages, api_key)

    def parse_json(s: str):
        try:
            return json.loads(s)
        except Exception:
            m = re.search(r"\{.*\}", s, flags=re.S)
            return json.loads(m.group(0)) if m else {"sub_questions": []}

    result = parse_json(raw)
    return result.get("sub_questions", [])
