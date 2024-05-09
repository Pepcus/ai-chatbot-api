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
Provide only factual and accurate responses. Always look into previous conversation history first.

You have access to the following tools:
{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}'''

hr_manager_prompt_template = '''
Specialization: You are an AI chatbot specialized in providing information on the HR domain. Don't expect chit-chat about anything else.
    Behavior: Cut the fluff. Keep your language straight to the point. Give answers without any sugar-coating or smiley faces in the 'Final Answer' action.

Must to follow things:
Provide only factual and accurate responses. Always look into previous conversation history first.

You have access to the following tools:
{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}'''


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
    return AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)

def hr_manager_executor():
    prompt = PromptTemplate.from_template(hr_manager_prompt_template)
    agent = create_react_agent(openai_llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)

memory = ChatMessageHistory()    

# existing prompt
def get_chat_response(chat_id, role, query):
    if (role == "HR_MANAGER"):
        agent_executor = hr_manager_executor()
    elif (role == "HR_ASSISTANT"):
        agent_executor = hr_assistant_executor()


    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    response = agent_with_chat_history.invoke(
            {"input": query},
            config={"configurable": {"session_id": chat_id}}
    )
    return response