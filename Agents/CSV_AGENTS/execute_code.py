from code_validator import get_valid_code
from utils import get_global_sandbox
import base64
import re


sbx = get_global_sandbox()


def execute_python(code: str) -> str:
    """
    Executes Python code in the global sandbox environment and captures output, charts, or visualizations.
    """
    print('🚀 Executing code in sandbox...')
    execution = sbx.run_code(code)
    print('✅ Code execution finished!')

    if execution.error:
        print('❌ AI-generated code had an error.')
        print(f"Error: {execution.error.name}")
        print(f"Message: {execution.error.value}")
        print("Traceback:\n", execution.error.traceback)

        return str({
            'error': execution.error.name,
            'message': execution.error.value,
            'traceback': execution.error.traceback,
            'code': code
        })

    output = ''
    if execution.logs and execution.logs.stdout:
        if isinstance(execution.logs.stdout, list):
            output += ''.join(execution.logs.stdout)
        else:
            output += execution.logs.stdout

    if execution.text:
        output += execution.text

    print("📝 Execution Output:\n", output)

    visual_idx = 0
    for result in execution.results:
        if result.png:
            filename = f'visual-{visual_idx}.png'
            with open(filename, 'wb') as f:
                f.write(base64.b64decode(result.png))
            print(f'🖼️ Visual saved to {filename}')
            visual_idx += 1

        if result.chart:
            chart = result.chart
            with open('Chart_data.txt', 'w') as f:
                f.write(f"Type: {chart.type}\n")
                f.write(f"Title: {chart.title}\n")
                if hasattr(chart, 'x_label'):
                    f.write(f"X Label: {chart.x_label}\n")
                if hasattr(chart, 'y_label'):
                    f.write(f"Y Label: {chart.y_label}\n")
                if hasattr(chart, 'x_unit'):
                    f.write(f"X Unit: {chart.x_unit}\n")
                if hasattr(chart, 'y_unit'):
                    f.write(f"Y Unit: {chart.y_unit}\n")
                f.write("Elements:\n")
                for element in chart.elements:
                    f.write("\n")
                    for attr in ['label', 'value', 'x', 'y', 'group']:
                        if hasattr(element, attr):
                            f.write(f"  {attr.capitalize()}: {getattr(element, attr)}\n")
            print("📊 Chart data saved to Chart_data.txt")

    return output
    

"""
def execute_local(temp_file_path: str) -> str:
    try:
        result = subprocess.run(
            ["python", temp_file_path], 
            capture_output=True, 
            text=True, 
            timeout=100
        )
        print(">>> Running code completed!")
        return result.stdout if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        return ">>> Execution timed out."
    except Exception as e:
        return f">>> Execution error: {str(e)}"
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
"""

pattern = re.compile(
        r"```python\n(.*?)\n```", re.DOTALL
)

def match_code_blocks(valid_code):
    match = pattern.search(valid_code.content)
    if match:
        code = match.group(1)
        print(code)
        return code
    else:
        return "CODE Not matched"
    
def execution_results(csv_path, query):
    valid_code, obs_plan_attr_rec = get_valid_code(csv_path, query)
    filtered_code = match_code_blocks(valid_code)
        
    valid_code_sandbox_output = execute_python(filtered_code)
    return valid_code_sandbox_output, obs_plan_attr_rec
