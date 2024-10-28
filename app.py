from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Function to identify font using Llama model (stubbed for this example)
def identify_font(image_path):
    # Here you would normally call your Llama model and get the identified font
    # For this example, let's assume it identifies "Roboto"
    identified_font = "Roboto"  # Replace this with the actual model output
    return identified_font

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

    # Save the uploaded file to a temporary location if needed
    image_path = f"temp_{file.filename}"
    file.save(image_path)

    # Identify the font from the image
    font_name = identify_font(image_path)
    
    # Construct the Google Fonts URL
    font_url = f"https://fonts.googleapis.com/css2?family={font_name.replace(' ', '+')}:wght@400;700&display=swap"

    return jsonify({'detected_font': font_name, 'font_url': font_url})

if __name__ == "__main__":
    app.run(debug=True)
