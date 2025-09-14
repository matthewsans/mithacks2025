
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from test_wo_anthropic import Test
import chromadb

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

client = chromadb.CloudClient(
    api_key='ck-CgjiogLt3X2NZD6tVoFAmzdFUHjhXBfTPepAZ4HWu99x',
    tenant='a2faafc5-2326-4a13-957a-4626ef39a875',
    database='qAnts',
)


# AIzaSyB_760I5bmGaoHzconRf5lOGKjhrJQxZ_A

vectorstore = Chroma(client=client, 
                     embedding_function=embeddings,
                     collection_name='sec_10k_collection')



retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"score_threshold": 0.1}
)



test = Test(retriever)