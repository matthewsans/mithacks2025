import chromadb
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key="API_KEY_HERE")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Setup ChromaDB
client = chromadb.CloudClient(
    api_key='key-goes-here',
    tenant='tenant-id-goes-here',
    database='database-name-goes-here'
)
collection = client.get_collection(name="sec_10k_collection")

def ask_question(question):
    # Get relevant chunks
    results = collection.query(
        query_texts=[question],
        n_results=5,
        include=["documents", "metadatas"]
    )
    
    # Create context
    context = "\n\n".join(results['documents'][0])
    
    # Ask Gemini
    prompt = f"""Based on these SEC 10-K excerpts, answer: {question}

Context:
{context}

Answer with specific numbers and company names:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Usage
print("Ask questions about SEC 10-K data (type 'quit' to exit):")
while True:
    question = input("\nQuestion: ")
    if question.lower() == 'quit':
        break
        
    answer = ask_question(question)
    print(f"\nAnswer: {answer}")
    print("-" * 50)