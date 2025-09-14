import requests, re

TANDEMN_URL = "https://api.tandemn.com/api/v1/chat/completions"
MODEL_ID    = "Qwen/Qwen3-32B-AWQ"
_session    = requests.Session()

def generate_financial_dashboard(
    rag_text: str,
    api_key: str,
    title: str = "Financial Overview",
    timeout: int = 90
) -> str:
    """
    Build a full HTML dashboard from a free-form financial RAG text blob.
    - No JSON schema required.
    - Model extracts metrics (revenue, net income, cash, debt, etc.) and time series from prose.
    - Produces a single HTML document (Chart.js, minimal CSS, responsive grid).

    Args:
        rag_text: Arbitrary text containing Q&A / excerpts / narratives from filings.
        api_key:  Tandemn API key.
        title:    Title for the dashboard <h1>.
        timeout:  HTTP timeout in seconds (HTML can be large).

    Returns:
        str: A complete HTML string (no markdown fences, ready to serve).
    """

    system_prompt = (
        "You are a financial front-end generator that creates elegant, responsive, and insightful dashboards. "
        "Your job is to analyze the financial text provided by the user and return a COMPLETE, SELF-CONTAINED HTML document ONLY "
        "(no markdown, no prose outside HTML, no explanations). The output should be production-grade, suitable for executive review.\n\n"

        "Design Requirements:\n"
        "1. Analyze the text for clear financial metrics: revenue, net income, operating income, cash, debt, equity, assets, R&D expenses, etc. "
        "Parse time series (annual or quarterly), segment breakdowns, and calculate derived metrics like ROE and profit margins when possible.\n"
        "2. Build visually appealing KPI cards:\n"
        "   - Use a modern, responsive grid layout (Flexbox or CSS Grid).\n"
        "   - Display KPIs with currency symbols, large bold numbers, labels, optional percent change YoY if present.\n"
        "   - Use color indicators (green for positive change, red for negative).\n"
        "3. Render insightful charts using Chart.js:\n"
        "   - Line chart: revenue and net income over time (by year or quarter).\n"
        "   - Bar chart: segment breakdowns or expense categories if found.\n"
        "   - Optional: pie chart for composition if useful.\n"
        "   - Charts must use different colors for each series, and include titles and axis labels.\n"
        "4. Style Requirements:\n"
        "   - Use embedded CSS (no external stylesheets or fonts).\n"
        "   - Light, professional theme (white background, gray tones, modern font like Arial or system default).\n"
        "   - Ensure mobile responsiveness.\n"
        "5. Optional Enhancements (if data allows):\n"
        "   - Include tooltips, legends, and hover effects on charts.\n"
        "   - Annotate charts with YoY % changes.\n"
        "   - Add ROE if both net income and equity are available.\n"
        "   - Create a summary section or executive overview with bullet points if needed.\n"
        "6. Never fabricate values. Only display what can be confidently extracted or calculated from the input. Skip unknowns gracefully.\n\n"
        "Output: A single full HTML5 document, ready to serve directly in a browser. Embed all JS/CSS inline via CDN."
    )


    user_prompt = (
        f"Title for the page: {title}\n\n"
        "Below is the free-form financial context. Extract what you can confidently, and render KPI cards and charts. "
        "Only include tables/charts that correspond to metrics explicitly present in the text. "
        "Do NOT fabricate intermediate years/quarters that are not in the text. "
        "Prefer exact values and labels that appear in the text. "
        "Return ONLY the HTML document.\n\n"
        "----- BEGIN CONTEXT -----\n"
        f"{rag_text}\n"
        "----- END CONTEXT -----\n"
    )

    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        "temperature": 0.2,    # slightly creative for layout, but conservative for data
        "top_p": 0.9,
        "max_tokens": 3500
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = _session.post(TANDEMN_URL, headers=headers, json=payload, timeout=timeout)
    r.raise_for_status()

    html = r.json()["choices"][0]["message"]["content"]

    # Clean common wrappers the model might add
    html = re.sub(r"<think>.*?</think>", "", html, flags=re.S)
    html = re.sub(r"```(?:html)?", "", html).strip()

    return html
