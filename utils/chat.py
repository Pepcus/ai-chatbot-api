from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_core.prompts import PromptTemplate
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import Tool
from config.config import openai_llm
from utils.sql import generate_and_execute_sql_query
from utils.pinecone import get_pinecone_query_engine
from langchain import hub
from langchain_core.prompts.chat import SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate

hr_assistant_prompt_template = '''
Specialization: You are a friendly AI-powered chatbot specialized in providing information on the HR domain.
Behavior: Always use polite language, friendly greetings, emojies in the 'Final Answer' action in the chain. Always ask if anything else they want to know.
'''

hr_manager_prompt_template = '''
Specialization: You are an AI chatbot specialized in providing information on the HR domain. Don't expect chit-chat about anything else.
Behavior: Cut the fluff. Keep your language straight to the point. Give answers without any sugar-coating or smiley faces in the 'Final Answer' action.
'''
memory = ChatMessageHistory()

prompt = hub.pull("hwchase17/structured-chat-agent")

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

def get_prompt(prompt_type: str):
    if(prompt_type == 'hr_assistant_prompt'):
        prompt_template = hr_assistant_prompt_template
    elif(prompt_type == 'hr_manager_prompt'):
        prompt_template = hr_manager_prompt_template

    prompt.messages = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['tool_names', 'tools'],
                template= prompt_template + ' Respond to the human as helpfully and accurately as possible. You have access to the following tools:\n\n{tools}\n\nUse a JSON blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).\n\nValid "action" values: "Final Answer" or {tool_names}\n\nProvide only ONE action per $JSON_BLOB, as shown:\n\n```\n{{\n  "action": $TOOL_NAME,\n  "action_input": $INPUT\n}}\n```\n\nFollow this format:\n\nQuestion: input question to answer\nThought: consider previous and subsequent steps\nAction:\n```\n$JSON_BLOB\n```\nObservation: action result\n... (repeat Thought/Action/Observation N times)\nThought: I know what to respond\nAction:\n```\n{{\n  "action": "Final Answer",\n  "action_input": "Final response to human"\n}}\n\nBegin! Reminder to ALWAYS respond with a valid JSON blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation'
            )
        ),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=['agent_scratchpad', 'input'],
                template='{input}\n\n{agent_scratchpad}\n (reminder to respond in a JSON blob no matter what)'
            )
        )
    ]
    return prompt

def hr_assistant_executor():
    agent = create_structured_chat_agent(openai_llm, tools, get_prompt('hr_assistant_prompt'))
    return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

def hr_manager_executor():
    agent = create_structured_chat_agent(openai_llm, tools, get_prompt('hr_manager_prompt'))
    return AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True)

def get_chat_response(chat_id, role, query):
    if (role == "HR_MANAGER"):
        agent_executor = hr_manager_executor()
    elif (role == "HR_ASSISTANT"):
        agent_executor = hr_assistant_executor()

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    response = agent_with_chat_history.invoke(
            {"input": query},
            config={"configurable": {"session_id": chat_id}}
    )
    return response['output']