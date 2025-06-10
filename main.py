import base64
import requests
import os

# --- Configuration ---
# IMPORTANT: Replace "abc" with your actual Google AI Studio API key.
# You can get one here: https://aistudio.google.com/app/apikey
API_KEY = "AIzaSyDTzn0avrKlIf8ch3B6ICc83wmaHJ66xu4"

# IMPORTANT: Replace this with the full path to the image you want to analyze.
# For example: "C:/Users/YourUser/Pictures/fruits.jpg" or "/home/user/images/fruit_basket.png"
IMAGE_PATH = "image.png"

# --- Main Script ---

def get_image_mime_type(filepath):
    """Gets the MIME type of an image file based on its extension."""
    if filepath.lower().endswith('.png'):
        return 'image/png'
    # Default to JPEG for .jpg, .jpeg, or other extensions
    return 'image/jpeg'

def encode_image_to_base64(filepath):
    """Encodes the image at the given filepath to a base64 string."""
    try:
        with open(filepath, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        print("Please make sure the IMAGE_PATH variable is set correctly.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the image: {e}")
        return None

def analyze_image_with_gemini(api_key, image_base64, mime_type):
    """
    Sends the image to the Gemini API and returns the identified fruits.
    """
    if not api_key or api_key == "abc":
        print("Error: API Key is not set.")
        print("Please replace 'abc' with your actual Gemini API key.")
        return None

    # Updated API URL to use a current and recommended model (gemini-1.5-flash-latest).
    # This resolves the '404 Not Found' error from the old model endpoint.
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # This is the prompt we send to the model.
    # We ask it to identify the fruits and return a simple, comma-separated list.
    prompt_text = "Identify all the fruits in this image. Please provide the response as a simple, comma-separated list. For example: Apple, Banana, Orange"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": mime_type, # Use the dynamically detected MIME type
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Sending image to Gemini for analysis...")
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
        
        response_json = response.json()

        # Navigate through the JSON response to get the text content
        if (response_json.get("candidates") and
                len(response_json["candidates"]) > 0 and
                response_json["candidates"][0].get("content") and
                response_json["candidates"][0]["content"].get("parts") and
                len(response_json["candidates"][0]["content"]["parts"]) > 0):
            
            text_response = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return text_response.strip()
        else:
            print("Error: Could not find the text part in the API response.")
            print("Full response:", response_json)
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    """Main function to run the fruit identification process."""
    print("--- Fruit Identifier ---")

    # Check if the image path is set
    if IMAGE_PATH == "path/to/your/fruit_image.jpg" or not os.path.exists(IMAGE_PATH):
        print("Error: Please update the 'IMAGE_PATH' variable with a valid path to your image file.")
        return

    # 1. Get the image's MIME type
    mime_type = get_image_mime_type(IMAGE_PATH)

    # 2. Encode the image
    image_data = encode_image_to_base64(IMAGE_PATH)
    if not image_data:
        return # Stop execution if image encoding failed

    # 3. Analyze with Gemini
    fruits_list = analyze_image_with_gemini(API_KEY, image_data, mime_type)

    # 4. Display the result
    if fruits_list:
        print("\n--- Analysis Complete ---")
        print("Gemini identified the following fruits in the image:")
        
        # Split the comma-separated string into a list and print each fruit
        fruits = [fruit.strip() for fruit in fruits_list.split(',')]
        for fruit in fruits:
            print(f"- {fruit}")
    else:
        print("\nCould not identify any fruits. Please check the error messages above.")

if __name__ == "__main__":
    main()
