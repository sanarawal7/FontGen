from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import requests
import os
import base64  # Import base64 for encoding images

app = Flask(__name__)

load_dotenv()

# Function to identify font using Llama model
def identify_font(image_path):
    # Your Hugging Face model URL
    llama_api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11B-Vision-Instruct"  # Replace with your actual model URL

    # Read the image file and encode it
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Prepare the request headers with your Hugging Face API key
    hf_api_key = os.getenv("HF_API_KEY")
    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json"  # Adjust if needed
    }

    # Prepare the request data
    data = {
        'inputs': f"What font style does this image resemble?",
        'image': image_data  # Adjust as necessary for your API
    }

    # Make a POST request to the Llama model
    response = requests.post(llama_api_url, headers=headers, json=data)

    if response.status_code == 200:
        # Print response for debugging
        print("Response JSON:", response.json())
        
        # Access the first element of the response list
        generated_text = response.json()[0].get("generated_text", "Unknown Font")
        
        # Extract the font name from the generated text (assume it's formatted as "It resembles the font 'FontName'")
        start = generated_text.find('"') + 1
        end = generated_text.find('"', start)
        identified_font = generated_text[start:end] if start > 0 and end > 0 else "Unknown Font"
        
        return identified_font
    else:
        # Handle errors
        print("Error communicating with Llama model:", response.status_code, response.text)
        return "Unknown Font"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file to a temporary location
    image_path = f"temp_{file.filename}"
    file.save(image_path)

    # Identify the font from the image using the Llama model
    font_name = identify_font(image_path)
    
    # Construct the Google Fonts URL
    font_url = f"https://fonts.googleapis.com/css2?family={font_name.replace(' ', '+')}:wght@400;700&display=swap"

    return jsonify({'detected_font': font_name, 'font_url': font_url})

if __name__ == "__main__":
    app.run(debug=True)
