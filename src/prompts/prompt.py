lays_classic_example = """nutritional information per 100 g: 
{
    "Energy": "537 kCal",
    "Macronutrients": { 
        "Protein": "6.9 g",
        "Carbohydrates": { 
            "Total": "52.9 g",
            "of which Sugars": "2.5 g",
            },
        "Dietary Fiber": "Not Present",
        "Total Fat": {
            "Total": "33.1 g",
            "Saturated Fat": "12.5 g",
            "Trans Fat": "0.1 g",
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
        "Folate": "Not Present",              
}"""


cadbury_dairy_milk_example = """nutritional information per 100 g: 
{
    "Energy": "534 kCal",
    "Macronutrients": { 
        "Protein": "7.3 g",
        "Carbohydrates": {
            "Total": "57 g",
            "of which Sugars": "56 g",
            },
        },
        "Dietary Fiber": "2.1 g",
        "Total Fat": {
            "Total": "30 g",
            "Saturated Fat": "18 g",
            "Trans Fat": "Not Present",
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
        "Folate": "Not Present",              
}"""


single_shot_prompt = """Parse the nutritional information and the list of ingredients of the product shown in the image. 

Use the nutritional information/nutritional fact label to identify the quantity of the following items:
Calories/Energy, Total Fat, Saturated Fat, Trans Fat, Cholesterol, Sodium, Total Carbohydrates, Dietary Fiber, Sugars, Protein, Vitamin A, Vitamin C, Calcium, and Iron.        
If the item is not present in the image, please mention that the item is not present in the image.

The output should contain only the nutritional information and the list of ingredients that is present on the product shown in the image. 
The output should be in a JSON format populated ONLY with the information that is available in the image. Make sure the JSON is valid and
do not add any additional information that is not present in the image.

Example of the output format:
{
    Nutritional information: {},
    Ingredients: ['items1', 'item2', 'item3']
}
"""