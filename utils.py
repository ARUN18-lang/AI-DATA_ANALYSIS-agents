from dotenv import load_dotenv, find_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

from e2b_code_interpreter import Sandbox

_sandbox = None

def get_global_sandbox(timeout=2000):
    load_dotenv()
    global _sandbox

    if _sandbox is None:
        sbx = Sandbox(timeout=timeout)
        running_sandboxes = sbx.list()

        if running_sandboxes:
            sandbox_id = running_sandboxes[0].sandbox_id
            logging.info(f"Connecting to existing sandbox: {sandbox_id}")
            _sandbox = Sandbox.connect(sandbox_id)
        else:
            _sandbox = Sandbox(timeout=timeout)
            logging.info(f"Created new sandbox: {_sandbox.sandbox_id}")

    return _sandbox


def get_groq_api_key():
    load_dotenv(find_dotenv())
    groq_api = os.getenv('GROQ_API_KEY')
    return groq_api

def get_nvidia_api_key():
    load_dotenv(find_dotenv())
    nvidia = os.getenv('NVIDIA_API_KEY')
    return nvidia