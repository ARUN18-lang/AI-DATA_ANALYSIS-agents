from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
import os

load_dotenv()

def nvidia_llm():
    model = ChatNVIDIA(
        model="nv-mistralai/mistral-nemo-12b-instruct",
        temperature=0.0,
        api_key=os.getenv('NVIDIA_API_KEY'),
    )    
    return model