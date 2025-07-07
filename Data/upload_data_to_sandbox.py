import os
from e2b_code_interpreter import Sandbox
from utils import get_global_sandbox
from dotenv import load_dotenv

load_dotenv()

sbx = get_global_sandbox()

def upload_data(file_path):
    print(f'Uploading data from {file_path} to the sandbox...')
    dataset_path = file_path
    if not os.path.exists(dataset_path):
        raise FileNotFoundError("Dataset file not found")

    try:
        with open(dataset_path, "rb") as f:
            dataset_path_in_sandbox = sbx.files.write(os.path.basename(dataset_path), f)
        print(f'Dataset uploaded to {dataset_path_in_sandbox}')
        return dataset_path_in_sandbox
    except Exception as error:
        print("Error during file upload:", error)
        raise error
