from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import WikipediaLoader
from bs4 import BeautifulSoup
import PIL.Image

load_dotenv()

def read_image(image_path):

    image = PIL.Image.open(image_path)
    return image

def generate_text_from_image(model_name,image):

    vision_llm = ChatGoogleGenerativeAI(model=model_name , temperature=0)
    message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Extract the list of ingredients and the nutritional information from the image provided to you. Include the details about serve size and the serves in this pack details as well. all return text should be in JSON formate.",
        },
        {
            "type": "image_url", 
            "image_url": image
        },

        ]
    )

    response = vision_llm.invoke([message])

    return response

def read_from_wikipedia(search_term):

    loader = WikipediaLoader(search_term)
    data = loader.load()

    data = data[0].page_content[:1000]

    return data


image = read_image(image_path='/Users/diyorahenils/Documents/personal work/google_gemini_hackathon/food-labels-gemini/images/lays.jpg')
response = generate_text_from_image("gemini-pro-vision",image)
data = read_from_wikipedia("what is machine learning")
print(data)
print(response)

