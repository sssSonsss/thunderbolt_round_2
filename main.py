import base64
import requests
import os
import json

# --- Configuration ---
# IMPORTANT: Replace "abc" with your actual Google AI Studio API key.
# You can get one here: https://aistudio.google.com/app/apikey
API_KEY = "AIzaSyDTzn0avrKlIf8ch3B6ICc83wmaHJ66xu4"

# IMPORTANT: Replace this with the full path to the image you want to analyze.
# For example: "C:/Users/YourUser/Pictures/fruits.jpg" or "/home/user/images/fruit_basket.png"
IMAGE_PATH = "input.png"

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
    Sends the image to the Gemini API and returns a detailed analysis
    of the fruits, including variety, count, and ripeness.
    """
    if not api_key or api_key == "abc":
        print("Error: API Key is not set.")
        print("Please replace 'abc' with your actual Gemini API key.")
        return None

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # Updated prompt to use 'variety' for the main fruit type (e.g., Apple)
    # and to request a JSON output with the specified keys.
    prompt_text = """
    Analyze the image and identify each type of fruit. For each fruit type, provide:
    1. The variety of the fruit (e.g., 'Apple', 'Banana', 'Orange').
    2. A count of how many are visible.
    3. An assessment of its ripeness ('unripe', 'ripe', or 'overripe').

    Please provide the response as a JSON object with a single key "fruits" which contains a list of objects.
    Each object in the list should have the following keys: "variety", "count", "ripeness".
    
    Example response format:
    {
      "fruits": [
        {"variety": "Apple", "count": 2, "ripeness": "ripe"},
        {"variety": "Banana", "count": 5, "ripeness": "unripe"}
      ]
    }
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64
                        }
                    }
                ]
            }
        ],
        # Added generationConfig to explicitly request JSON output.
        "generationConfig": {
          "responseMimeType": "application/json"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Sending image to Gemini for detailed analysis...")
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        response_json = response.json()

        if (response_json.get("candidates") and
                response_json["candidates"][0].get("content") and
                response_json["candidates"][0]["content"].get("parts")):
            
            # The response is now expected to be structured JSON text.
            json_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            # We parse the JSON string into a Python dictionary.
            data = json.loads(json_text)
            return data.get("fruits") # Return the list of fruit objects
        else:
            print("Error: Could not find the expected content part in the API response.")
            print("Full response:", response_json)
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while calling the Gemini API: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the API response.")
        print("Received response:", response.text)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    """Main function to run the fruit identification process."""
    print("--- Advanced Fruit Analyzer ---")

    if IMAGE_PATH == "path/to/your/fruit_image.jpg" or not os.path.exists(IMAGE_PATH):
        print("Error: Please update the 'IMAGE_PATH' variable with a valid path to your image file.")
        return

    mime_type = get_image_mime_type(IMAGE_PATH)
    image_data = encode_image_to_base64(IMAGE_PATH)
    if not image_data:
        return

    # Get the detailed list of fruits from the analysis.
    detailed_fruits_list = analyze_image_with_gemini(API_KEY, image_data, mime_type)

    # Display the results as a JSON object, as requested.
    if detailed_fruits_list:
        print("\n--- Detailed Fruit Analysis Complete ---")
        # Create the final JSON object to be printed
        output_json = {"fruits": detailed_fruits_list}
        # Print the JSON object with indentation for readability
        print(json.dumps(output_json, indent=2))
    else:
        print("\nCould not identify any fruits or failed to get details. Please check the error messages above.")

if __name__ == "__main__":
    main()
