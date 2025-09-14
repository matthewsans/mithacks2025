from backend.build_html.givemecode import generate_financial_dashboard
API_KEY = "gk-lg2FEI1z_oknwrbbbuya"

rag_output = '''
Question: What is the total revenue of5 Sigma Corp in the most recent fiscal year?

Answer: Based on the provided text, there are multiple companies mentioned and their revenues reported in different formats (billions vs. millions).  There's no single "5 Sigma Corp" mentioned.  The excerpts show the following revenue figures:

A company with $18.8 Billion in revenue: This company is not named but has a breakdown of revenue by segment. The total revenue is presented as the sum of its parts (Global Business Solutions, Consumer, Credit Karma, and ProTax).
A company with $558.3 Million in revenue: This unnamed company explicitly states its revenue for the fiscal year ended June 30, 2025.
Another unnamed company with $1,713.2 million in revenue: This company's fiscal year ended in 2025.


To answer your question accurately, I need the full name of the company whose total revenue you are seeking.  The excerpts show revenue figures for several different companies but don't consistently name them.
Question: What is the total revenue of Aeluma Inc in the most recent fiscal year?

Answer: Based on the provided text, there are multiple revenue figures, and it's unclear which one represents Aeluma Inc.'s total revenue for the most recent fiscal year.  The excerpts show data for different companies and different fiscal year ends.

One excerpt shows a company with revenue of $9,221.5 million for the year ended July 31, 2025.  However, this is not explicitly stated to be Aeluma Inc.

Another excerpt shows a company with revenue of $558,273,000 for the year ended June 30, 2025. Again, this is not explicitly identified as Aeluma Inc.

A third excerpt mentions EVI Industries, Inc. with revenue of approximately $30.8 million for fiscal 2025. This is not Aeluma's revenue.

To determine Aeluma Inc.'s total revenue, more information is needed, specifically a clear statement identifying the relevant financial statement from the 10-K.
Question: What is the percentage change in revenue for alt5 Sigma Corp from the previous fiscal year?

Answer: Alt5 Sigma Corp (the name is inferred from the provided text as it's the only company with provided financial data in this format) had a 9.8% increase in revenue from the previous fiscal year.  The revenue for the fiscal year ended June 30, 2025 was $558.3 million.
Question: What is the percentage change in revenue for Aeluma Inc from the previous fiscal year?

Answer: There are multiple companies mentioned with varying revenue changes:

Aeluma Inc.:  The provided text does not contain financial information for a company called Aeluma Inc.

Company with $853,699,000 in total revenue (2025): This unnamed company experienced an 11.8% increase in revenue from $763,855,000 in 2024.

EVI Industries, Inc.: This company saw a revenue increase from $423,357,744 in 2024 to $433,485,131 in 2025.  This represents a change of approximately $10,127,387 or a 2.4% increase.

Unnamed company with $42.3 million in revenue (2024): This unnamed company had a 6.5% increase in revenue from $39.7 million in 2023 to $42.3 million in 2024.

Unnamed company with $81.4 billion in sales (2025): This unnamed company experienced a 3.2% increase in sales from the previous fiscal year.

Please note that some excerpts include unaudited data and non-GAAP measures (like adjusted operating income), which might differ from the reported figures.  Without knowing which company excerpt you're referring to as "Aeluma Inc.", a precise answer cannot be given.
Question: What is the revenue per share for alt5 Sigma Corp in the most recent fiscal year?

Answer: The provided text states that alt5 Sigma Corp (Sigma) had a diluted net income per share of $13.67 in fiscal year 2025.  However, it does not provide the revenue for Sigma, only total revenue for the unnamed parent company.  Therefore, revenue per share for alt5 Sigma Corp cannot be calculated from this information.
Question: What is the revenue per share for Aeluma Inc in the most recent fiscal year?

Answer: The provided text gives Aeluma Inc.'s revenue for the year ended June 30, 2025 as $696,162,000.  However, it does not provide the number of outstanding shares for Aeluma Inc.  Therefore, it's impossible to calculate the revenue per share.

'''

def get_html_mock(rag_output: str):
    """Mock HTML generation without API call"""
    print("Using mock HTML generation...")
    
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
        .question {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; border-radius: 4px; }}
        .answer {{ margin: 10px 0; padding: 10px; background: #e9ecef; border-radius: 4px; }}
        .source {{ font-size: 0.9em; color: #666; margin-top: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Financial Analysis Dashboard</h1>
        <div class="content">
            {rag_output.replace(chr(10), '<br>')}
        </div>
    </div>
</body>
</html>
"""
    
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote dashboard.html")

    return html

def get_html(rag_output: str):
    """Main function that tries API first, falls back to mock on timeout"""
    try:
        print("Attempting to use Tandem API for HTML generation...")
        html = generate_financial_dashboard(rag_output, API_KEY, title="Financial Dashboard")
        with open("dashboard.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Wrote dashboard.html")
        return html
    except Exception as e:
        print(f"API call failed: {e}")
        print("Falling back to mock HTML generation...")
        return get_html_mock(rag_output)
