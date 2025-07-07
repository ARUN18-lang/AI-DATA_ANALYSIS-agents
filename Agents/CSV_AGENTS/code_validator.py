from model import nvidia_llm
from coder_agent import get_code

llm = nvidia_llm()

CODE_VALIDATOR_PROMPT = """
You are an expert Python code reviewer working in a production-grade environment.

---
### 🎯 Objective:
Analyze and validate the provided Python code for the following aspects:
- ✅ Pip Packages. (already found in sandbox packages are pandas, matplotlib, numpy, seaborn. other than this four packages if any package needed then you need to add !pip install <package_name> on top of the code.)
- ✅ Syntax correctness
- ✅ Logical correctness
- ✅ Proper indentation
- ✅ Adherence to Python best practices (PEP8)
- ✅ Compatibility with non-interactive, headless sandbox environments (no GUI, no widgets, no `input()` calls)
- ✅ Modular and readable structure (functions, comments, clean imports)

---
### 🔁 Instructions:
- If the code is correct and meets the above criteria, return it **unchanged**.
- If any issues are found (even minor ones), return a fully corrected version.
- Do **not** return any explanations or comments outside the code.
- Ensure the final code is syntactically executable and debug-friendly.

---
### 🚀 Code to Review:
```python
{code}
```
"""

def build_code_validator_prompt(code: str) -> str:
    return CODE_VALIDATOR_PROMPT.format(code=code.strip())

def code_validator_agent(llm, code_validator_prompt: str):
    print(f"{'='*30} Validating code... {'='*30}")
    messages = [
        {'role': 'system', 'content': 'You are a strict Python code reviewer and best practices enforcer.'},
        {'role': 'user', 'content': code_validator_prompt}
    ]
    response = llm.invoke(messages)
    return response


def get_valid_code(csv_path, query):
    code, obs_plan_att_rec = get_code(csv_path, query)
    code_validator_prompt = build_code_validator_prompt(code.python_code)
    valid_code = code_validator_agent(llm, code_validator_prompt)
    return valid_code, obs_plan_att_rec

