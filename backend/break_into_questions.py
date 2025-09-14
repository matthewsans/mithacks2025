import requests, re, json
from typing import List

TANDEMN_URL = "https://api.tandemn.com/api/v1/chat/completions"
MODEL_ID    = "Qwen/Qwen3-32B-AWQ"

_session = requests.Session()

def _post_tandemn(messages: list, api_key: str) -> str:
    """Call Tandemn and return assistant content as plain text, sanitized."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_ID,
        "messages": messages,
        "temperature": 0,           # deterministic
        "top_p": 1,
        "max_tokens": 800,
        # Many models honor this to emit strict JSON.
        "response_format": {"type": "json_object"}
    }
    r = _session.post(TANDEMN_URL, headers=headers, json=data, timeout=40)
    r.raise_for_status()
    txt = r.json()["choices"][0]["message"]["content"]
    # Safety: strip code fences and stray tags if any provider injects them.
    txt = re.sub(r"<.*?>", "", txt, flags=re.S)
    txt = re.sub(r"```(?:json|txt|markdown)?", "", txt).strip()
    return txt

def extract_companies(user_input: str, api_key: str, max_companies: int = 4) -> List[str]:
    """
    Extract public company names in order of mention; map brands to parent (Google -> Alphabet).
    Returns up to `max_companies`.
    """
    messages = [
        {"role": "system", "content":
            'Return STRICT JSON ONLY: {"companies": ["...", "..."]}. '
            "Extract up to 4 PUBLIC company names explicitly or implicitly mentioned. "
            "Map brands to canonical parents (e.g., Google -> Alphabet). No extra text."
        },
        {"role": "user", "content": user_input},
    ]
    raw = _post_tandemn(messages, api_key)

    def parse_json(s: str):
        try:
            return json.loads(s)
        except Exception:
            m = re.search(r"\{.*\}", s, flags=re.S)
            return json.loads(m.group(0)) if m else {"companies": []}

    companies = (parse_json(raw).get("companies") or [])
    # basic cleanup/dedup
    seen, cleaned = set(), []
    for c in companies:
        name = re.sub(r"\s+", " ", (c or "")).strip()
        if name and name.lower() not in seen:
            seen.add(name.lower())
            cleaned.append(name)
    return cleaned[:max_companies]

def _get_canonical_templates(api_key: str, user_input: str) -> List[str]:
    """
    Ask the model for EXACTLY 5 company-agnostic templates using the literal token COMPANY_TOKEN.
    We will replace COMPANY_TOKEN with real company names BEFORE returning to the caller.
    """
    messages = [
        {"role": "system", "content":
            'Return STRICT JSON ONLY: {"templates":["...","...","...","...","..."]}. '
            "Generate five concise, filings-answerable questions (10-K/10-Q). "
            "Each MUST include the literal token COMPANY_TOKEN where the company name belongs, "
            "prefer possessive phrasing (e.g., COMPANY_TOKEN\'s ...). "
            "Avoid comparisons, explanations, chart names, or markdown. No numbering. "
            "Prefer explicit time scopes (e.g., last 8 quarters, last 5 fiscal years, most recent fiscal year)."
        },
        {"role": "user", "content":
            "Produce the 5 canonical templates (they will be used identically for each company). "
            f"Request: {user_input}"
        },
    ]
    raw = _post_tandemn(messages, api_key)

    def parse_json(s: str):
        try:
            return json.loads(s)
        except Exception:
            m = re.search(r"\{.*\}", s, flags=re.S)
            return json.loads(m.group(0)) if m else {"templates": []}

    templates = parse_json(raw).get("templates") or []

    # sanitize & cap to 5
    out = []
    for t in templates:
        t = re.sub(r"^\s*\d+\.\s*", "", (t or "")).strip()
        t = re.sub(r"\s+", " ", t)
        if t:
            out.append(t)
        if len(out) == 5:
            break
    return out

def _expand_for_companies(templates: List[str], companies: List[str]) -> List[str]:
    """Apply the identical 5 templates to each company (replace COMPANY_TOKEN)."""
    if not templates:
        return []
    if not companies:
        # If no company detected, just return the templates with a generic label removed.
        return [t.replace("COMPANY_TOKEN ", "").replace("COMPANY_TOKEN", "").strip() for t in templates]

    expanded = []
    for t in templates:
        for c in companies:
            expanded.append(t.replace("COMPANY_TOKEN", c))
    # de-dup while preserving order
    seen, dedup = set(), []
    for q in expanded:
        k = q.lower()
        if k not in seen:
            seen.add(k)
            dedup.append(q)
    return dedup

def build_semantic_rag_queries(user_input: str, api_key: str, max_companies: int = 4) -> List[str]:
    """
    Public API (same name you already use).
    - Detect up to `max_companies` companies from `user_input`.
    - Get a single canonical set of 5 templates (with COMPANY_TOKEN).
    - Return the fully expanded, company-specific questions (no placeholders).
    - If only one company is mentioned, you’ll get 5 questions (for that one company).
    - If multiple companies are mentioned, you’ll get 5 * N questions, with identical wording per company.
    """
    companies  = extract_companies(user_input, api_key, max_companies=max_companies)
    templates  = _get_canonical_templates(api_key, user_input)
    questions  = _expand_for_companies(templates, companies)
    return questions or [user_input]  # fallback: return the original request

def build_semantic_rag_queries_delimited(user_input: str, api_key: str, sep: str = "|||") -> str:
    """Same as above, but returns a single string joined by `sep`."""
    return sep.join(build_semantic_rag_queries(user_input, api_key))
