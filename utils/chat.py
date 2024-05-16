from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from config.config import openai_llm
from utils.sql import generate_and_execute_sql_query
from utils.pinecone import get_pinecone_query_engine
from langchain_core.prompts import ChatPromptTemplate

@tool
def handbook(input: str, company: str) -> {}: # type: ignore
    '''Useful for answering queries related to employee handbooks, company policies, employee benefits etc.'''
    rag_chain = get_pinecone_query_engine(company)
    result = rag_chain.invoke({"input": input})
    metadata_values = [doc.metadata['page'] for doc in result['context']]
    return {"answer" : result['answer'], "source" : "Employee Handbook Page Number " + str(metadata_values[0])}

@tool
def database(query: str, company: str) -> {}: # type: ignore
    '''Useful for answering questions related to real time data like number of employees, salaries, departments etc. First generate the query and then execute it.'''
    result = generate_and_execute_sql_query(query, company)
    return {"answer" : result, "source" : "Database"}

tools = [handbook, database]

def friendly_agent():
    system_prompt = ''' 
    Specialization: You are a friendly AI-powered chatbot specialized in providing information on the HR domain.

    Must to follow things: 
    
    Do not add or makeup things by yourself. Always use polite language, friendly greetings, happy face emogies in the 'Final Answer' in the chain. Always ask if anything else they want to know.

    Given a user question and PDF extract or database, answer the user question and provide citations. If none of the articles answer the question, just say you don't know.

    Ensure to pass user's input without any modification to the tool you are using.

    Remember, you must return both an answer and citations. A citation consists of a VERBATIM quote that  justifies the answer and the ID of the quote article. Return a citation for every quote across all articles that justify the answer. 

    If user says thank you or concluding the conversation, tell him if he wants further information he can refer to the handbook available here:

    https://storage.googleapis.com/pep-handbooks/{company}.pdf

    Strictly use the following format for your final output:

    Answer: <answer>
    Source: <source>
    '''

    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}, {company}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    return create_tool_calling_agent(openai_llm, tools, agent_prompt)
    
def serious_agent():
    system_prompt = '''
    Specialization: You are an AI chatbot specialized in providing information on the HR domain. Don't expect chit-chat about anything else.
    
    Must to follow things: Do not add or makeup things by yourself. Keep your language straight to the point. Give answers without any sugar-coating or smiley faces in the 'Final Answer' action.
    
    Given a user question and PDF extract or database, answer the user question and provide citations. If none of the articles answer the question, just say you don't know.

    Ensure to pass user's input without any modification to the tool you are using.

    Remember, you must return both an answer and citations. A citation consists of a VERBATIM quote that  justifies the answer and the ID of the quote article. Return a citation for every quote across all articles that justify the answer. 

    If user says thank you or concluding the conversation, tell him if he wants further information he can refer to the handbook available here:

    https://storage.googleapis.com/pep-handbooks/{company}.pdf

    Strictly use the following format for your final output:

    Answer  : <answer>
    Source  : <source>
    '''

    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}, {company}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    return create_tool_calling_agent(openai_llm, tools, agent_prompt)

memory = ChatMessageHistory()

def get_chat_response(chat_id, company, query):
    if (company == "OPT"):
        agent = serious_agent()
    elif (company == "ESP"):
        agent = friendly_agent()
    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history"
    )
    response = agent_with_chat_history.invoke(
            {"input": query, "company": company},
            config={"configurable": {"session_id": chat_id}}
    )
    print("===========", response)
    return response['output']