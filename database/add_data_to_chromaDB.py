import os
import chromadb

# ---- 1️⃣  Setup ChromaDB Client ----
client = chromadb.CloudClient(
  api_key='ck-CgjiogLt3X2NZD6tVoFAmzdFUHjhXBfTPepAZ4HWu99x',
  tenant='a2faafc5-2326-4a13-957a-4626ef39a875',
  database='qAnts'
)

collection = client.get_or_create_collection(name="sec_10k_collection")

# ---- 2️⃣  Process all files in folder ----
folder_path = "sec_texts_by_company"

# ---- 3️⃣  Helper: split text into overlapping chunks ----
def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Yield overlapping text chunks.
    chunk_size: max characters in each chunk
    overlap:    repeated characters between chunks for context
    """
    start = 0
    while start < len(text):
        end = start + chunk_size
        yield text[start:end]
        start = end - overlap  # keep a small overlap for better context

# ---- 4️⃣  Process each file in the folder ----
if not os.path.exists(folder_path):
    print(f"❌ Folder '{folder_path}' not found!")
    exit()

txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
total_files = len(txt_files)

if total_files == 0:
    print(f"❌ No .txt files found in '{folder_path}'")
    exit()

print(f"📂 Found {total_files} files to process")

for file_idx, filename in enumerate(txt_files, 1):
    file_path = os.path.join(folder_path, filename)
    company_name = os.path.splitext(filename)[0]
    
    print(f"[{file_idx}/{total_files}] Processing: {company_name}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        chunk_count = 0
        for i, chunk in enumerate(chunk_text(text, chunk_size=1000, overlap=200)):
            doc_id = f"{company_name}_{i}"
            collection.add(
                documents=[chunk],
                ids=[doc_id],
                metadatas=[{"company": company_name, "chunk": i, "filename": filename}]
            )
            chunk_count += 1
        
        print(f"   ✅ Uploaded {chunk_count} chunks for {company_name}")
        
    except Exception as e:
        print(f"   ❌ Error processing {filename}: {str(e)}")
        continue

print("🎉 Finished processing all files!")