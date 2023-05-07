from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
import os
import configparser

# Get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the parent folder
os.chdir(script_dir)

config = configparser.ConfigParser()
config.read('config.ini')

os.environ['OPENAI_API_KEY'] = config['api_keys']['OPENAI_API_KEY']

DOCUMENTS_FOLDER_FIRST_PAGE = 'data/raw/articles_firstpage_txt'
DOCUMENTS_FOLDER = 'data/raw/articles_txt'

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
PERSIST_DIRECTORY_FIRST_PAGE = 'data/vectorstore/db_first_page'
PERSIST_DIRECTORY = 'data/vectorstore/db'

# generate vectorstores for the documents

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

for (document_folder, persist_directory) in [(DOCUMENTS_FOLDER_FIRST_PAGE, PERSIST_DIRECTORY_FIRST_PAGE), (DOCUMENTS_FOLDER, PERSIST_DIRECTORY)]:
    # check if the persist_directory exists
    if not os.path.exists(persist_directory):
        loader = DirectoryLoader(document_folder, glob='**/*.txt')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)
        docsearch = Chroma.from_documents(
            texts, embeddings, persist_directory=persist_directory)