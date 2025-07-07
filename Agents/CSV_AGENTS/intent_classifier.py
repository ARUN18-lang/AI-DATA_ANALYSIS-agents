from pydantic import BaseModel
from typing import List, Literal
from model import nvidia_llm

llm = nvidia_llm()

class IntentItem(BaseModel):
    type: Literal["Descriptive", "Diagnostic", "Predictive", "Prescriptive"]
    confidence: float  
    #justification: str  

class IntentClassification(BaseModel):
    detected_intents: List[IntentItem]


INTENT_CLASSIFIER_PROMPT = """
You are an expert analytics strategist specializing in **Spend Analytics**.

Your job is to analyze a user query and classify its **analytical intent(s)** based on the five categories of analysis:

1. **Descriptive** - What happened?  
   E.g., Summarizing spend trends, top suppliers, spend by category, etc.
   a.Compare spending trends between Q1 and Q2 for all regions.

2. **Diagnostic** - Why did it happen?  
   E.g., a. "Which region had the highest spend last quarter?"
         b. "What categories had an unusual spike in spending this month?"
         c. "Identify any outliers in high-value transactions."
         d."Which customer segments have shown decreased activity over time?"

3. **Predictive** - What might happen next?  
   E.g., a."Forecast next month's spend based on previous trends."
         b."Predict which category is likely to exceed budget next quarter."
         c."Estimate total transaction volume for the upcoming fiscal year."
         d."Which regions are expected to grow fastest in spending?"
         e."Identify customers at risk of churn based on current activity patterns."

4. **Prescriptive** - What should we do about it?  
   E.g., a."What cost-saving opportunities can be implemented based on spend data?"
         b."Recommend budget adjustments for underperforming regions."
         c."Suggest optimizations for categories with frequent overspending."
         d."Which vendors should we negotiate with based on spend volume?"
         e."What strategy should we apply to reduce high return rates?"

5. **Unknown** - The query does not align with the above intents, is too vague, or lacks analytical direction (e.g., casual queries, off-topic requests, unclear goals).

---

### USER QUERY:
{query}

---

### INSTRUCTIONS:
- You may assign one or more intents (multi-label classification).
- For each intent, provide a **confidence score** (0.0 to 1.0).
- Justify **why** that intent applies based on the query language and purpose.
- Use the `Unknown` intent only if the query doesn't align with any valid analytical intent, or if the user is asking a non-analytical or unrelated question.
- Respond in **Pydantic JSON format** using the schema below.

---

### SCHEMA:
```json
{{
  "detected_intents": [
    {{
      "type": "Descriptive | Diagnostic | Predictive | Prescriptive | Unknown",
      "confidence": 0.92,
    }}
  ]
}}

"""

def build_intent_prompt(query):
    prompt = INTENT_CLASSIFIER_PROMPT.format(
        query=query
    )
    return prompt

def intent_classifier_agent(llm, intent_prompt):
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant'},
        {'role': 'user', 'content': intent_prompt}
    ]
    structured_llm = llm.with_structured_output(IntentClassification)
    response = structured_llm.invoke(messages)
    return response

def get_intent(query):
    intent_prompt = build_intent_prompt(query)
    response = intent_classifier_agent(llm, intent_prompt)
    intents = [intent.model_dump() for intent in response.detected_intents]
    return intents



