import requests, json, csv, time
# 879e3cf7a9ce2c1fcc156f42ad73f643cf9796bdc1b74996debccc7cbca32061
API_KEY = "c1932efcf2a5dc3e89353ff8a0ba94b57589d0c55b834a8d18b3d9fb1ea1a3b5"
BASE_URL = "https://api.sec-api.io"
PAGE_SIZE = 200     
query = 'formType:"10-K"'

with open("all_10k.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ticker", "formType", "companyName", "filedAt", "linkToFilingDetails"])

    from_index = 0
    while True:
        payload = {
            "query": { "query_string": { "query": query } },
            "from": from_index,
            "size": PAGE_SIZE,
            "sort": [{ "filedAt": { "order": "desc" } }]
        }

        resp = requests.post(
            f"{BASE_URL}/?token={API_KEY}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        resp.raise_for_status()
        data = resp.json()

        filings = data.get("filings", [])
        if not filings:  
            break

        for item in filings:
            writer.writerow([
                item.get("ticker"),
                item.get("formType"),
                item.get("companyName"),
                item.get("filedAt"),
                item.get("linkToFilingDetails")
            ])

        from_index += PAGE_SIZE    
        time.sleep(0.5)          

print("save all data to all_10k.csv")
