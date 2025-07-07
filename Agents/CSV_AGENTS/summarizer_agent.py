import sys
import os
from pathlib import Path
from model import nvidia_llm

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from Data.get_data import summarizer

llm = nvidia_llm()

SUMMARIZER_PROMPT = """You are a summarizer assistant, who is working in a team.
        your task is to summarize the given csv data in structured format so that other agent can use it effectively for analysis.
        provide dataset name by yourself based on following data. your summary should be useful for further data analysis tasks.
        ## IMPORTANT INSTRUCTION: DO NOT CHANGE THE COLUMN/ATTRIBUTE NAME, YOU SHOULD KEEP AS IT IS, EITHER IT IS LOWER OR IN UPPER CASE.
        Here is the {df}
        Provide a comprehensive summary of the dataset:
         
"""

def build_summarizer_prompt(file_path):
    prompt = SUMMARIZER_PROMPT.format(
        df=summarizer(file_path)
    )
    return prompt


def summary(llm, summarizer_system_prompt):
    print(f' {"="*50} Analyzing the data {"="*50}')
    messages = [
            {'role': 'system', 'content': "You are a helpful data analysis assistant."},
            {'role': 'user', 'content': summarizer_system_prompt}
        ]
    response = llm.invoke(messages)
    print(f'SUMMARY OF THE DATA: {response.content}')
    return response

def get_summary(file_path):
    summarizer_system_prompt = build_summarizer_prompt(file_path)
    response = summary(llm, summarizer_system_prompt)
    return response