import os 
import sys
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

from src.exception import CustomException
from src.logger import logger
from src.utils.text_utils import process_output_string
from src.prompt import get_label_extraction_prompt

load_dotenv()

# Intialize the LLM models and Embeddings
llm_vision_model = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0, convert_system_message_to_human=True)
llm_text_model   = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, convert_system_message_to_human=True)
embeddings       = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Initialize the vector database
persist_directory = 'vectordb'
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def extract_info_from_label(uploaded_image_path):
    """Extract nutritional information from the uploaded image

    Args:
        uploaded_image_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        message  = get_label_extraction_prompt(uploaded_image_path)
        logger.info(f"Prompt generated successfully")

        response = llm_vision_model.invoke(message)
        logger.info("Response received successfully")

        output = process_output_string(response.content)
        logger.info(f"Output processed successfully. Output JSON: {output}")

        return output
    
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

        return None


def query_vector_db(label_info, gender, age_group, rag_prompt):
    """Query the vector database to get the nutritional goals for
    a specific gender and age group. Based on these goals assess the healthiness
    of the food label.

    Args:
        label_info (str): _description_
        gender (str): _description_
        age_group (str): _description_

    Returns:
        str: the response from the model
    """
    try:

        output_parser = StrOutputParser()

        # initialize the RAG chain
        chain = rag_prompt | llm_text_model | output_parser

        relevant_docs = vectordb.similarity_search(f"What are the nutritional goals for a {gender} in the age group {age_group}?")

        context = ""

        for doc in relevant_docs:
            if doc.metadata.get('age_group') == age_group and doc.metadata.get('gender') == gender:
                context += doc.page_content

        print(f"context: {context}\n") 
        print(f"label_info: {label_info}\n")
        print(f"gender: {gender}, age_group:{age_group}\n")

        response = chain.invoke({"context": context, "label_info": label_info})

        return response
    
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)

        return None