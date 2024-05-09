from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.agents import Tool
from app_config import openai_llm
from utils_langchain_sql_v2 import generate_and_execute_sql_query
from utils_langchain_pinecone_v2 import get_pinecone_query_engine
from langchain.agents import initialize_agent

hr_assistant_prompt = '''
    Specialization: You are a friendly AI-powered chatbot specialized in providing information on the HR domain.
    Always use polite language, friendly greetings, emojies in the 'Final Answer' action in the chain. Always ask if anything else they want to know.
    Guideline: Provide only factual and accurate responses.
'''

hr_manager_prompt = '''
    Specialization: You are an AI chatbot specialized in providing information on the HR domain. Don't expect chit-chat about anything else.
    Behavior: Cut the fluff. Keep your language straight to the point. Give answers without any sugar-coating or smiley faces in the 'Final Answer' action.
    Guideline: Stick to the facts, and only the facts. 
'''

handbook = get_pinecone_query_engine('TSS')

def database_agent(query: str):
    result = generate_and_execute_sql_query(query, company='tss')
    return result

tools = [
    Tool(
        name = "Handbook",
        func = handbook.run,
        description = "useful for answering queries related to employee handbooks, company policies, employee benefits etc."
        ),
    Tool(
        name = "Database",
        func = database_agent,
        description = "useful for answering questions related to real time data like number of employees, salaries, departments etc. First generate the query and then execute it."
    )
]

# conversational memory
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=openai_llm,
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory,
    handle_parsing_errors=True,
    verbose=True
)

# existing prompt
def get_chat_response(role, query):
    if (role == "HR_MANAGER"):
        sys_msg = hr_manager_prompt
    elif(role == "HR_ASSISTANT"):
        sys_msg = hr_assistant_prompt

    new_prompt = agent.agent.create_prompt(
        system_message=sys_msg,
        tools=tools
    )
    agent.agent.llm_chain.prompt = new_prompt

    print(agent.agent.llm_chain.prompt.messages[0])
    
    return agent.invoke(query)