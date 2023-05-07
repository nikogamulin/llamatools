import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain import OpenAI
import os
import configparser

# Get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the parent folder
os.chdir(os.path.join(script_dir, '..'))

config = configparser.ConfigParser()
config.read('config.ini')

os.environ['OPENAI_API_KEY'] = config['api_keys']['OPENAI_API_KEY']

# Supplying a persist_directory will store the embeddings on disk
PERSIST_DIRECTORY_FIRST_PAGE = 'data/vectorstore/db_first_page'
PERSIST_DIRECTORY = 'data/vectorstore/db'

# generate vectorstores for the documents

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])

# Define a function to retrieve an answer and references for a given question


def get_answer_and_references(question):
    docsearch = Chroma(persist_directory=PERSIST_DIRECTORY,
                       embedding_function=embeddings)

    # expose this index in a retriever interface
    retriever = docsearch.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    qa = RetrievalQA.from_chain_type(llm=OpenAI(
    ), chain_type="stuff", retriever=retriever, return_source_documents=True)

    result = qa({"query": question})

    print(result)
    answer, reference = result["result"], result["source_documents"]

    return answer, reference

# Define the main function to create the app interface


def main():
    st.title("Question Answering App")
    question = st.text_input("Enter your question here:")

    if st.button("Submit"):
        if question:
            # Call the function to get the answer and references
            answer, reference = get_answer_and_references(question)
            reference = list(map(lambda x: x.metadata["source"], reference))

            # Display the answer and references on the app interface
            st.header("Answer:")
            st.write(answer)

            st.header("References:")
            st.write(reference)
        else:
            st.warning("Please enter a question.")


if __name__ == "__main__":
    main()
# path = 'data/raw/articles_firstpage_txt/1982 Reddy - Mineralization of Nitrogen in Organic Soils.txt'

# filename_with_extension = os.path.basename(path)
# filename, extension = os.path.splitext(filename_with_extension)

# print(filename)  # Output: '1982 Reddy - Mineralization of Nitrogen in Organic Soils'
