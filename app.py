from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

import chainlit as cl
import os 
import sys
from src.exception import CustomException
from src.logger import logger
from src.preprocess_img import preprocess_image

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@cl.on_chat_start
async def on_chat_start():
    
    elements = [
        cl.Image(name="image1", display="inline", path="images/food-labels-SM.jpg")
    ]

    await cl.Message(content="Welcome to the Nutritional Facts Info!", elements=elements).send()
    
    res = await cl.AskUserMessage(content="What is your age?", timeout=10).send()
    cl.user_session.set("age", res['output'])

    res = await cl.AskUserMessage(content="What is your gender?", timeout=10).send()
    cl.user_session.set("gender", res['output'])


@cl.on_message
async def on_message(msg: cl.Message):
    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    print(images)

    # Read the first image
    with open(images[0].path, "r") as f:
        pass

    await cl.Message(content=f"Received {len(images)} image(s)").send()

    preprocess_image(images[0].path)

    print("Image processed")
    print(f"Age: {cl.user_session.get('age')}")
    print(f"Gender: {cl.user_session.get('gender')}")