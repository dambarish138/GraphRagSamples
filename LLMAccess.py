from langchain_openai import ChatOpenAI

openai_api_key = "XXX"

def get_gpt4omni():
    llm = ChatOpenAI(
        api_key = openai_api_key,
        temperature=0, 
        model_name="gpt-4o")
    return llm