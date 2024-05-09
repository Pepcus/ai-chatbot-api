from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from utils_langchain_pinecone_v1 import get_pinecone_query_engine
from utils_langchain_sql_v2 import generate_and_execute_sql_query
client = OpenAI()

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
                "required": ["query"]
            }
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
                "required": ["query"]
            }
        }
    }
]   


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, model='gpt-3.5-turbo'):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def execute_function_call(company, message, query, context):
    print("========inside execute_function_call=============")
    if message.tool_calls[0].function.name == "get_information_from_employee_handbook":
        print("========Pinecone Query Engine Activated=============", query)
        results = get_pinecone_query_engine(company, query, context)
    elif message.tool_calls[0].function.name == "get_information_from_application_database":
        print("========Application Database Query Engine Activated=============", query)
        results = generate_and_execute_sql_query(query, company)
    else:
        results = f"Error: function {message.tool_calls[0].function.name} does not exist"
    return results

def get_chat_response(company, query, context):
    print("=======context in get_chat_response========", context)
    chat_response = chat_completion_request(
        messages = context
        , tools=tools
    )
    assistant_message = chat_response.choices[0].message
    if assistant_message.tool_calls:
        response = {}
        response['output'] = execute_function_call(company, assistant_message, query, context)
    else:
        response = {}
        response['output'] =  assistant_message.content    
    print("========inside get response results=============", response) 
    return response['output']