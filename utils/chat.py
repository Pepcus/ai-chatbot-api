from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import Tool
from config.config import openai_llm
from utils.sql import generate_and_execute_sql_query
from utils.pinecone import get_pinecone_query_engine

hr_assistant_prompt_template = '''
Specialization: You are a friendly AI-powered chatbot specialized in providing information on the HR domain.
Always use polite language, friendly greetings, emojies in the 'Final Answer' action in the chain. Always ask if anything else they want to know.

Must to follow things:
Provide only factual and accurate responses.

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

hr_manager_prompt_template = '''
Specialization: You are an AI chatbot specialized in providing information on the HR domain. Don't expect chit-chat about anything else.
    Behavior: Cut the fluff. Keep your language straight to the point. Give answers without any sugar-coating or smiley faces in the 'Final Answer' action.

Must to follow things:
Provide only factual and accurate responses.

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''


handbook = get_pinecone_query_engine('TSS')

def database_agent(query: str):
    result = generate_and_execute_sql_query(query)
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

def hr_assistant_executor():
    prompt = PromptTemplate.from_template(hr_assistant_prompt_template)
    agent = create_react_agent(openai_llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools)

def hr_manager_executor():
    prompt = PromptTemplate.from_template(hr_manager_prompt_template)
    agent = create_react_agent(openai_llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools)

# Dictionary to store ChatMessageHistory objects for different session_ids
session_memories = {}

# Create a function to retrieve or create ChatMessageHistory based on session_id
def get_memory(session_id):
    if session_id not in session_memories:
        session_memories[session_id] = ChatMessageHistory()
    return session_memories[session_id]

# existing prompt
def get_chat_response(chat_id, role, query):
    if (role == "HR_MANAGER"):
        agent_executor = hr_manager_executor()
    elif (role == "HR_ASSISTANT"):
        agent_executor = hr_assistant_executor()

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: get_memory(session_id),
        input_messages_key="input",
        history_messages_key="chat_history"
    )

    return agent_with_chat_history.invoke(
            {"input": query},
            config={"configurable": {"session_id": chat_id}}
    )