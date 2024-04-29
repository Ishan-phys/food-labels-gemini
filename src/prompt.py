from langchain_core.messages import HumanMessage, SystemMessage
# Import prompt template 
from langchain.prompts import PromptTemplate
from src.utils.image_utils import preprocess_image
import cv2


# Read the example prompts from the txt files
with open("src/prompts/lays_classic_label_info.txt", "r") as file:
    lays_classic_example = file.read()

with open("src/prompts/cadbury_dairy_milk_label_info.txt", "r") as file:
    cadbury_dairy_milk_example = file.read()

with open("src/prompts/rag_template.txt", "r") as file:
    rag_prompt_template = file.read()

def get_rag_prompt():
    """Generate a prompt for the RAG model"""
    return PromptTemplate.from_template(template=rag_prompt_template)

def get_label_extraction_prompt(uploaded_image):
    """Generate a prompt to get nutritional information from the LLM

    Args:
        processed_image: the processed image

    Returns:
        str: the prompt
    """
    # Load and preprocess the images for example images of food labels
            # load the image if it exists

    image1 = cv2.imread("images/lays_cropped.jpg") 
    image1 = preprocess_image(image1)
    image2 = cv2.imread("images/cadbury.jpg") 
    image2 = preprocess_image(image2)

    print("Images loaded and preprocessed successfully")

    # Load and preprocess the images for the uploaded image
    image3 = preprocess_image(uploaded_image)

    print("Uploaded images loaded and preprocessed successfully")

    image_message1 = {
        "type": "image_url",
        "image_url": image1
    }

    image_message2 = {
        "type": "image_url",
        "image_url": image2
    }

    image_message3 = {
        "type": "image_url",
        "image_url": image3
    }

    # Create a message with the examples of food labels
    message = [
        SystemMessage(content="You are a bot that is designed to extract nutritional information from the images of food labels. You will be given an image of a food label and you need to extract the nutritional information from it. You will be given examples of food labels to help you understand the task."),
        HumanMessage(content=[image_message1, lays_classic_example, image_message2, cadbury_dairy_milk_example, image_message3])
    ]

    return message