import csv, os, re, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_CSV = "all_10k.csv"
OUTPUT_DIR = "sec_texts_by_company"
os.makedirs(OUTPUT_DIR, exist_ok=True)

headers = {
    "User-Agent": "YourCompany YourApp/1.0 (contact@yourcompany.com)"
}

def safe_filename(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9._ -]+', '_', name)[:150]

def fetch_and_extract(company: str, url: str):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        for s in soup(["script", "style"]):
            s.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_clean = "\n".join(chunk for chunk in chunks if chunk)

        fname = f"{safe_filename(company)}.txt"
        path = os.path.join(OUTPUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_clean)
        return f"Saved: {path}"

    except Exception as e:
        return f"Error {company}: {e}"

def main():
    tasks = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        with ThreadPoolExecutor(max_workers=10) as executor:
            for row in reader:
                if row["linkToFilingDetails"]:
                    company = row["companyName"] or "Unknown"
                    tasks.append(executor.submit(fetch_and_extract, company, row["linkToFilingDetails"]))
            for fut in as_completed(tasks):
                print(fut.result())

if __name__ == "__main__":
    main()
