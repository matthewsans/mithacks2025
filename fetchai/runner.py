
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from test_wo_anthropic import Test

COLLECTION_NAME = "your_collection_name"
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vectorstore = Chroma.from_texts(
    texts=[
        "This is a document about pineapple",
        "This is a document about oranges",
        "This is a document about iron"
    ],
    embedding=embeddings,
    collection_name=COLLECTION_NAME
)

retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.1}
)



test = Test(retriever)