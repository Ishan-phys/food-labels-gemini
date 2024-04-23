import json 
import re

def process_output(string):
    """Process the output string and extract the content between the triple quotes

    Args:
        string: the output string from the LLM

    Returns:
        dict: the extracted content
    """
    # Use regular expression to find JSON object
    json_string = re.search(r'{.*}', string, re.DOTALL).group()

    # Convert JSON string to dictionary
    data = json.loads(json_string)

    return data