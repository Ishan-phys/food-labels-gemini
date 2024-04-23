import os 
import sys
import uuid
import base64
import json
import tempfile
from typing import List
import cv2
import numpy as np
from io import BytesIO

from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from fastapi import FastAPI, Request, Form, Response, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


from PIL import Image
from dotenv import load_dotenv

from src.exception import CustomException
from src.logger import logger
from src.utils.image_utils import convert_to_base64, convert_to_html
from src.prompt import get_label_prompt
from src.utils.text_utils import process_output

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def extract_info_from_label(uploaded_image_path):
    """Extract nutritional information from the uploaded image

    Args:
        uploaded_image_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0, convert_system_message_to_human=True)
        logger.info("Model loaded successfully")

        message  = get_label_prompt(uploaded_image_path)
        logger.info(f"Prompt generated successfully")

        response = llm.invoke(message)
        logger.info("Response received successfully")
        
        output = response.content

        return output
    
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_file(image: UploadFile = Form(...), ageGroup: str = Form(...), gender: str = Form(...)):
    
    #print(f"Image: {image.file.read()}")
    contents = await image.read()
    image_data = BytesIO(contents)
    img = Image.open(image_data)
    rgb_image = img.convert("RGB")
    print(f"image type: {type(rgb_image)}")
    img.show()

    image_array = np.array(rgb_image)

    print(f"read the image file: {image.filename}")
    print(f"dropdown1: {ageGroup}")
    print(f"dropdown2: {gender}")
    
    res = extract_info_from_label(image_array)
    # response_dict = process_output(string=res)

    # Do your processing with the image and numbers here
    # For now, let's just return the uploaded file name and the numbers
    return JSONResponse({"status":200, "response": res})

# @app.post("/get_answer")
# async def get_answer(question: str = Form(...)):

#     response      = extract_info_from_label()
#     response_dict = process_output(string=response)

#     # Input will be the age-group, gender and the image of the food label item
#     relevant_docs = db.similarity_search(question)
#     context = ""
#     relevant_images = []
#     for d in relevant_docs:
#         if d.metadata['type'] == 'text':
#             context += '[text]' + d.metadata['original_content']
#         elif d.metadata['type'] == 'table':
#             context += '[table]' + d.metadata['original_content']
#         elif d.metadata['type'] == 'image':
#             context += '[image]' + d.page_content
#             relevant_images.append(d.metadata['original_content'])
#     result = qa_chain.run({'context': context, 'question': question})
#     return JSONResponse({"relevant_images": relevant_images[0], "result": result})


if __name__ == "__main__":
    app()