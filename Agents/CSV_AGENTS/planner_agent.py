from langchain_nvidia_ai_endpoints import ChatNVIDIA
from pydantic import BaseModel
from model import nvidia_llm
from typing import List
from dotenv import load_dotenv
from intent_classifier import get_intent
import sys
from pathlib import Path
from summarizer_agent import get_summary

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

load_dotenv()

llm = nvidia_llm()

class StructuredPlan(BaseModel):
    key_observations: str
    plan: str
    recommendations: str
    attributes: List[str]


CSV_ANALYSIS_PLANNER_PROMPT = """
You are a senior data analysis strategist working with **CSV files** for various business domains, including spend analytics, forecasting, diagnostics, and recommendations.

Your job is to generate a **clear, structured analysis plan** to solve the user query by leveraging only the **provided dataset** and respecting the declared **intent(s)**.

Try to solve as simple as possible, if it is not a complicated query.
---

**User Query:** {query}

**Detected Intent(s):** {intent}

**Data Summary:**
{df_summary}

---

### 🔐 RULES YOU MUST FOLLOW — STRICTLY:
VERY IMPORTANT: DO NOT CHANGE ANY COLUMN NAMES/ ATTRIBUTES OR ANY VALUES WHEN YOU DESIGN THE SOLUTION.
1. ✅ **Follow the Intent(s) Exactly**  
   - Do NOT guess or classify the intent — use the one(s) provided.  
   - If multiple intents are given (e.g., "Descriptive + Prescriptive"), address **all** in your plan.  

2. 🔍 **Plan Based Only on the Dataset**  
   - Use **only the available rows and columns** from the data summary.  
   - ##Do NOT rename, infer, or create new columns.  
   - If a question or intent cannot be solved using the given data, explicitly mention it.

3. 🧠 **Each Plan Must Be Executable**  
   - Assume another agent will turn this into code — you must be precise, detailed, and step-based.  
   - Do NOT write or suggest any code or functions.

4. 🎯 **Intent-Specific Guidance**:
   - `Descriptive`: Explore summaries, groupings, counts, distributions, trends.
   - `Diagnostic`: Focus on identifying reasons, correlations, and root causes.
   - `Predictive`: If solvable with available data, suggest using simple models (regression, classification, forecasting).  
     - Only propose if column types and row volumes are reasonable.
   - `Prescriptive`: Provide practical rule-based actions or optimization strategies using the data (e.g., cost reduction, supplier shift).
   - `Unknown`: Provide the best possible descriptive/diagnostic plan using available attributes.

---

### 🎯 FORMAT REQUIREMENTS:

Respond in **strict JSON** format with the following structure:

```json
{{
  "key_observations": "3 to 5 concise bullets derived from the data summary, written as plain text with line breaks between bullets.",
  "plan": "Step-by-step bullet point plan written in text, organized by intent if applicable. Use newline-separated hyphen bullets.",
  "recommendations": "A brief summary of expected outputs and why they matter. Explain what kind of visual or tabular output will best represent each part.",
  "attributes": ["List", "of", "column", "names", "used"] 
}}

Do NOT include any explanation, markdown, YAML, or extra commentary. Return only this JSON block.
"""



def build_planner_prompt(intents, df_summary, query):
    prompt = CSV_ANALYSIS_PLANNER_PROMPT.format(
        intent=intents,
        df_summary=df_summary,
        query=query
    )
    return prompt


def run_agent(llm, prompt):
    print(f"{'='*30} planning.... {'='*30}")
    messages = [
        {'role': 'system', 'content': 'You are a helpful Data Analyst assistant'},
        {'role': 'user', 'content': prompt}
    ]
    structured_llm = llm.with_structured_output(StructuredPlan)
    #print('structured_llm: ', structured_llm)
    response = structured_llm.invoke(messages)
    print(f'{response.key_observations} \n {response.plan}')
    return response


def get_plans(query, file_path):
    df_summary=get_summary(file_path)
    intents = get_intent(query)
    intents_detected = [intent['type'] for intent in intents]
    print(f"{'='*50} Intent: {intents_detected} {'='*50}")

    prompt_for_plan = build_planner_prompt(
        intents=intents_detected,
        df_summary=df_summary.content,
        query=query
    )
    #print(prompt_for_plan)

    result = run_agent(llm, prompt_for_plan)
    return result

