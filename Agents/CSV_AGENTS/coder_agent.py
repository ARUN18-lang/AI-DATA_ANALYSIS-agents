from pathlib import Path
import sys
from pydantic import BaseModel
from model import nvidia_llm

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from planner_agent import get_plans
from Data.upload_data_to_sandbox import upload_data


llm = nvidia_llm()

class PythonCode(BaseModel):
    python_code: str


PLANNER_CODER_PROMPT = """
# Data Science Code Generator - Sandbox Edition

## Role
You are an advanced AI Python data scientist that writes **production-ready, executable** code for data analysis tasks in a constrained sandbox environment.

## Inputs
You will receive:
- `dataset_path`: Path to dataset → {dataset_path}
- `analysis_plan`: Step-by-step analysis logic → {plan}
- `attributes`: Required dataset columns → {attributes}
- `recommendations`: Expected outputs → {recommendations}

## Environment Constraints
### Execution Environment
- Headless Python sandbox
- Non-interactive (no user input)
- Persistent filesystem access
- Internet access available

## Execution Constraints
### Strict Prohibitions
❌ Never create new files (no .csv, .html, .png outputs)
❌ Never drop columns from the original DataFrame
❌ No intermediate DataFrame saving
 **In-Memory Only**: No file creation or filesystem writes
 **Single DataFrame**: Maintain all analysis in the original DataFrame or direct derivatives

### Visualization Requirements
- All charts must be self-contained
- Mandatory elements:
  - Clear titles
  - Labeled axes
  - Readable scales
  - Legends where appropriate
- Output must render completely without manual intervention
- in-line plotting is only allowed

## Package Management Rules
### Pre-installed Packages
```python
['pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy'] These are already installed dont need any installation for these packages.

Additional Package Installation
REQUIRED format for package installation:
# PIP INSTALL SECTION (MUST be at top if needed)
!pip install package_name==version  # pin versions when critical
import package_name

Installation constraints:
- Maximum 3 additional packages per script
- Total install time < 30 seconds
- No GPU-accelerated packages
- No system-level dependencies

Code Requirements
- Structure
    - Do not change any attributes, use the given attributes.
   - IMPORTS (including any installations)
   - DATA LOADING
   - ANALYSIS 
   - Print() and visualizations.
   - **do not write code like this if __name__ == '__main__': <- this will cause UnboundError.**

##OUTPUT GENERATION
#Quality Standards
- Type hints for all functions
- Docstrings for all functions
- Explicit error handling
- Memory-efficient operations
- Pandas best practices (vectorized ops)

##Output Specification
#Required Outputs
- Text summaries via print()
- Structured data previews
- Visualizations (matplotlib/seaborn/plotly)

##Prohibited Outputs
- Interactive widgets
- Web applications
- Unrendered plot objects
- Partial/incomplete outputs

##Security Restrictions
- No subprocess execution
- No shell commands
- No sensitive data exposure
- No external system modifications

#Critical Reminders
 -Verify all column names against attributes
- Include axis labels for all visualizations
- Test for missing data
- Add progress print statements
- Never assume data quality

📦 Output Format (strict):
### Your response must strictly follow this format:
```python
# your Python code here
```
"""



def build_coder_prompt(dataset_path, plan, recommendations, attributes):
    prompt = PLANNER_CODER_PROMPT.format(
        dataset_path=dataset_path,
        attributes=attributes,
        plan=plan,
        recommendations=recommendations
    )
    return prompt

def planner_coder_agent(llm, planner_prompt):
    print(f"{'='*50} Writing code... {'='*50}")
    messages = [
        {'role': 'system', 'content': 'you are helpful python coding assistant'},
        {'role': 'user', 'content': planner_prompt}
    ]
    structured_llm = llm.with_structured_output(PythonCode)
    response = structured_llm.invoke(messages)
    print(f"{response.python_code} \n {'='*100}")
    return response

def get_code(csv_path, query):
    result = get_plans(query, csv_path)
    sandbox_path = upload_data(csv_path)
    planner_prompt = build_coder_prompt(
        dataset_path=sandbox_path.path,
        plan=result.plan,
        recommendations=result.recommendations,
        attributes=result.attributes
    )
    code_response = planner_coder_agent(llm, planner_prompt)
    return code_response, result



