from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.image_utils import preprocess_image
import cv2


lays_classic_example = """nutritional information per 100 g: 
    json object'{"Energy": "537 kCal",
        "Macronutrients": { 
            "Protein": "6.9 g",
            "Carbohydrates": { 
                "Total": "52.9 g",
                "Sugar": "2.5 g"
                },
            "Dietary Fiber": "Not Present",
            "Total Fat": {
                "Total": "33.1 g",
                "Saturated Fat": "12.5 g",
                "Trans Fat": "0.1 g"
                },
            "Linoleic Acid": "Not Present",
            "Linolenic acid": "Not Present"
        },
        "Minerals": { 
            "Calcium": "Not Present",
            "Iron": "Not Present",
            "Magnesium": "Not Present",
            "Phosphorus": "Not Present",
            "Potassium": "Not Present",
            "Sodium": "993 mg",
            "Zinc": "Not Present",
            "Cooper": "Not Present",
            "Manganese": "Not Present",
            "Selenium": "Not Present"
        },
        "Vitamins": {                
            "Vitamin A": "Not Present",
            "Vitamic E": "Not Present",
            "Vitamin D": "Not Present",
            "Vitamin C": "Not Present",
            "Thiamin": "Not Present",
            "Riboflavin": "Not Present",
            "Niacin": "Not Present",
            "Vitamin B6": "Not Present",
            "Vitamin B12": "Not Present",
            "Choline": "Not Present",
            "Vitamin K": "Not Present",
            "Folate": "Not Present"             
    }
}"""


cadbury_dairy_milk_example = """nutritional information per 100 g: 
    json object'{"Energy": "534 kCal",
        "Macronutrients": { 
            "Protein": "7.3 g",
            "Carbohydrates": {
                "Total": "57 g",
                "Sugar": "56 g"
                },
            "Dietary Fiber": "2.1 g",
            "Total Fat": {
                "Total": "30 g",
                "Saturated Fat": "18 g",
                "Trans Fat": "Not Present"
            },
            "Linoleic Acid": "Not Present",
            "Linolenic acid": "Not Present"
        },
        "Minerals": { 
            "Calcium": "Not Present",
            "Iron": "Not Present",
            "Magnesium": "Not Present",
            "Phosphorus": "Not Present",
            "Potassium": "Not Present",
            "Sodium": "240 mg",
            "Zinc": "Not Present",
            "Cooper": "Not Present",
            "Manganese": "Not Present",
            "Selenium": "Not Present"
        },
        "Vitamins": {                
            "Vitamin A": "Not Present",
            "Vitamic E": "Not Present",
            "Vitamin D": "Not Present",
            "Vitamin C": "Not Present",
            "Thiamin": "Not Present",
            "Riboflavin": "Not Present",
            "Niacin": "Not Present",
            "Vitamin B6": "Not Present",
            "Vitamin B12": "Not Present",
            "Choline": "Not Present",
            "Vitamin K": "Not Present",
            "Folate": "Not Present"            
    }
}"""


def get_label_prompt(uploaded_image):
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