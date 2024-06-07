from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text.strip(): # Check if the extracted text is not empty
                text += page_text.strip() + " " # Add extracted text to the overall text
    return text.strip() # Remove leading/trailing whitespace from the final text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversional_chain():
    prompt_template = """
    Answer the questions as detailed as possible from the provided context, if the answer is not in
    provided context just say, "answer is not available in the given file", Provide accurate answers\n\n
    Context:\n{context}?\n
    Question:\n{question}\n

    Answer:  
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.form['question']
    pdf_docs = request.files.getlist('pdf_docs')
    
    if not pdf_docs:
        return jsonify({'response': 'No PDF files uploaded'})
    
    raw_text = get_pdf_text(pdf_docs)
    if not raw_text: # Check if the extracted text is empty
        return jsonify({'response': 'No text extracted from PDF files'})
    
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)
    response = user_input(user_question)
    return jsonify({'response': response})

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    index_path = "faiss_index"
    if not os.path.exists(index_path):
        return "FAISS index file does not exist. Please ensure the index is created and saved."
    
    new_db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    if not user_question.strip(): # Check if the user question is empty
        return "No question provided."
    
    docs = new_db.similarity_search(user_question)

    chain = get_conversional_chain()

    response = chain.invoke({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    return response["output_text"]

if __name__ == '__main__':
    app.run(debug=True)
