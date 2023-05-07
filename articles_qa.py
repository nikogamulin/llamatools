from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import OpenAI
import os
import configparser

# Get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the parent folder
os.chdir(script_dir)

config = configparser.ConfigParser()
config.read('config.ini')

os.environ['OPENAI_API_KEY'] = config['api_keys']['OPENAI_API_KEY']

# Supplying a persist_directory will store the embeddings on disk
PERSIST_DIRECTORY_FIRST_PAGE = 'data/vectorstore/db_first_page'
PERSIST_DIRECTORY = 'data/vectorstore/db'

# generate vectorstores for the documents

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

docsearch = Chroma(persist_directory=PERSIST_DIRECTORY_FIRST_PAGE,
                           embedding_function=embeddings)

# expose this index in a retriever interface
retriever = docsearch.as_retriever(
    search_type="similarity", search_kwargs={"k": 2})

qa = RetrievalQA.from_chain_type(llm=OpenAI(
), chain_type="stuff", retriever=retriever, return_source_documents=True)

query = "how to estimate chemical index of nitrogen"
result = qa({"query": query})

print(result)


# https://github.com/hwchase17/chroma-langchain/blob/master/persistent-qa.ipynb
