from execute_code import execution_results
from planner_agent import get_plans
from model import nvidia_llm

llm = nvidia_llm()

FINAL_RESPONSE_PROMPT = """
You are acting as the final response generator in an intelligent data analysis pipeline — the Finisher.
Your role is to synthesize and articulate a clear, confident, and conversational summary of the analysis based on the following inputs:

🔹 **Key Observations:** {key_observations}
🔹 **Plan of Action:** {plan}
🔹 **Execution Results:** {execution_results}

Your job is to present the *final summary* as if you conducted the entire analysis yourself — confidently and professionally.

### Instructions:
- Frame the response as a concluding, insightful summary.
- Start conversationally, but grounded in data — *“Here's a quick summary of your data…”*
- If `execution_results` is empty, missing, or an error occurred, fall back to the plan and key observations to still generate a confident output.
- Clearly highlight important patterns, spend trends, or anomalies (if present).
- Offer value-driven recommendations or next steps if applicable.
- Do **not** say “I dont know” or mention failures — always provide a best-effort insight based on available context.

The goal is to make the user feel like they've received expert-level, high-quality insights.
"""


def build_final_response_prompt(key_observations, plan, execution_results):
    prompt = FINAL_RESPONSE_PROMPT.format(
        key_observations=key_observations,
        plan=plan,
        execution_results=execution_results
    )
    return prompt

def final_response_generator(llm, final_message):
    messages = [
        {'role': 'system', 'content': "You are a helpful summarizer assistant."},
        {'role': 'user', 'content': final_message}
    ]
    response = llm.invoke(messages)
    return response

def final_analysis_concluder(csv_path, query):
    sandbox_output, obs_attr_rec_plan = execution_results(csv_path, query)
    final_message = build_final_response_prompt(
        key_observations=obs_attr_rec_plan.key_observations,
        plan=obs_attr_rec_plan.plan,
        execution_results=sandbox_output
    )
    response = final_response_generator(llm, final_message)
    return response.content

csv_path = r'C:\Users\arun5\Desktop\Spend_analyzer\src\Data\transaction_data_250.csv'

while True:
    user_input = input('Ask your query: ')
    if user_input == 'q': break
    else:
        print(final_analysis_concluder(csv_path, user_input))
