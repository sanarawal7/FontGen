import requests
import os
from dotenv import load_dotenv

load_dotenv()
hf_api_key = os.getenv("HF_API_KEY")

url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11B-Vision-Instruct"  # Replace with your actual endpoint
headers = {
    "Authorization": f"Bearer {hf_api_key}",
}
payload = {
    "inputs": "What font does this image resemble?",
    # Add any other necessary parameters
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
