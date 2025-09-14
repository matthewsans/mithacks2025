# test_wo_anthropic.py

import pandas as pd
# from langchain_anthropic import ChatAnthropic

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores.base import VectorStoreRetriever

class Test:
    def __init__(self, retriever: VectorStoreRetriever) -> None:
        self.retriever = retriever
            
    # --- 2. Create the Query Transformation Chain ---
    # (LLM is removed)

    # Create a prompt that instructs the LLM to rewrite the query
    rewrite_template = """
    You are an expert at crafting search queries for a financial vector database.
    Rewrite the user's question into a more detailed and descriptive query that is 
    likely to find the most relevant documents.

    Original question: {question}

    Rewritten query:
    """
    rewrite_prompt = ChatPromptTemplate.from_template(rewrite_template)

    # --- 3. Function to Format Output as DataFrame ---
    def format_docs_to_df(self, docs):
        if not docs:
            return pd.DataFrame()
        data_list = [doc.metadata | {'page_content': doc.page_content} for doc in docs]
        return pd.DataFrame(data_list)

    # This full chain will not work as it is missing the LLM component.
    # full_chain = (
    #     query_transformer_chain
    #     | retriever
    #     | RunnableLambda(format_docs_to_df)
    # )

    # You can directly use the retriever without the LLM for now.
    def run_retriever(self, question):
        docs = self.retriever.invoke(question)
        return self.format_docs_to_df(docs)

# --- 5. Run the Workflow ---
if __name__ == "__main__":
    # original_question = "fruit"
    
    # print("--- Retrieving Data with Original Question ---")
    # results_df = run_retriever(original_question)
    
    # print(results_df)

    pass