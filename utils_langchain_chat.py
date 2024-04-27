import json
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from utils_langchain_pinecone import get_pinecone_query_engine
from utils_langchain_sql import get_sql_query_agent
from utils_langchain_ocr import read_pdf_through_ocr

client = OpenAI()

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model='gpt-3.5-turbo'):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    
SYSTEM_PROMPT = '''
    You are an AI-powered chatbot specialized in providing information on the HR domain.
    If the user query pertains to company, HR policies, employee handbook, or work culture, call the function `get_information_from_employee_handbook` and pass user's query without any modification to it.
    If the user query relates to data such as the number of employees, departments, or salary information, call the function `get_information_from_application_database` and pass user's query without any modification to it.
    If the user asks for PDF reconciliation call the function `reconcile_pdf_through_ocr`and pass filelocation without any modification to it.
    Do not make up anything from your end.
'''

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_information_from_employee_handbook",
            "description": "Get information from employee handbook",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "User's query",
                    }
                },
                "required": ["query"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_information_from_application_database",
            "description": "Get information from application database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "User's query",
                    }
                },
                "required": ["query"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reconcile_pdf_through_ocr",
            "description": "Reconcile PDF through OCR",
            "parameters": {
                "type": "object",
                "properties": {
                    "filelocation": {
                        "type": "string",
                        "description": "File Location",
                    }
                },
                "required": ["filelocation"],
            },
        }
    }
]   


initial_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def execute_function_call(pc, db, llm, embeddings, company, message):
    print("========inside execute_function_call=============")
    if message.tool_calls[0].function.name == "get_information_from_employee_handbook":
        query = json.loads(message.tool_calls[0].function.arguments)["query"]
        print("========pinecone query=============", query)
        results = get_pinecone_query_engine(pc, llm, embeddings, company, query)
    elif message.tool_calls[0].function.name == "get_information_from_application_database":
        query = json.loads(message.tool_calls[0].function.arguments)["query"]
        print("========sql query=============", query)
        results = get_sql_query_agent(db, llm, query)
    elif  message.tool_calls[0].function.name == "reconcile_pdf_through_ocr":
        filelocation = json.loads(message.tool_calls[0].function.arguments)["filelocation"]
        print("========filelocation=============", filelocation)
        results = read_pdf_through_ocr(filelocation)
    else:
        results = f"Error: function {message.tool_calls[0].function.name} does not exist"
    return results

def get_chat_response(pc, db, llm, embeddings, company, query):
    print("========inside get response=============")
    chat_response = chat_completion_request(
        messages=initial_messages + [
                {"role": "user", "content": query},
        ]
        , tools=tools
    )
    assistant_message = chat_response.choices[0].message
    print("========inside get response assistant_message=============", assistant_message)
    if assistant_message.tool_calls:
        response = execute_function_call(pc, db, llm, embeddings, company, assistant_message)
    else:
        response = {}
        response['output'] =  assistant_message.content    
    print("========inside get response results=============", response) 
    return response