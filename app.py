import sys
import numpy as np
from io import BytesIO

from fastapi import FastAPI, Request, Form, Response, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


from PIL import Image
from dotenv import load_dotenv

from src.exception import CustomException
from src.logger import logger
from src.main_funcs import extract_info_from_label, query_vector_db
from src.prompt import get_rag_prompt

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


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_file(image: UploadFile = Form(...), ageGroup: str = Form(...), gender: str = Form(...)):
    """Function to upload the image and get the nutritional information from the image, 
    and query the vector database to get the nutritional goals for the given age group.

    Args:
        image (UploadFile, optional): _description_. Defaults to Form(...).
        ageGroup (str, optional): _description_. Defaults to Form(...).
        gender (str, optional): _description_. Defaults to Form(...).

    Returns:
        _type_: _description_
    """
    try:
        contents   = await image.read()
        image_data = BytesIO(contents)
        img        = Image.open(image_data)
        rgb_image  = img.convert("RGB")

        image_array = np.array(rgb_image)

        logger.info(f"read the image file: {image.filename}")
        logger.info(f"dropdown1: {ageGroup}")
        logger.info(f"dropdown2: {gender}")

        age_group = str(ageGroup).lower()
        gender    = str(gender).lower()
        
        # Extract the nutritional information from the image
        label_info = extract_info_from_label(image_array)
        
        if label_info is None:
            return JSONResponse({"status":500, "response": "Error processing the image"})
        
        else: 
            # Query the vector database to get the nutritional goals for the given age group and gender
            response = query_vector_db(label_info, gender, age_group, rag_prompt=get_rag_prompt())
            logger.info(f"Response from the model: {response}")

        return JSONResponse({"status":200, "response": response})
    
    except Exception as e:
        error_message = CustomException(e, sys)
        logger.error(error_message)
        return JSONResponse({"status":500, "response": "Error processing the image"})


if __name__ == "__main__":
    app()