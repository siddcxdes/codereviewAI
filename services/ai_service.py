from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("POLLINATIONS_API_KEY"),
    base_url="https://text.pollinations.ai/openai",
    model="openai",
    temperature=0
)

def analyze_code(system_prompt: str, code: str) -> str:
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze this code and respond in the JSON format specified:\n\n{code}")
    ]
    
    response = llm.invoke(messages)
    return response.content


def parse_ai_response(response_text: str) -> dict:
    cleaned = response_text.strip()
    
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    
    try:
        return json.loads(cleaned.strip())
    except:
        print(f"Could not parse AI response as JSON")
        return {"issues": [], "summary": response_text}