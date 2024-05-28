"""
Filename: chay.py
Author: Deepak Nigam
Date created: 2024-04-28
License: MIT License
Description: This file contains functions used by the chatbot for the answering users questions.
"""

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import tool
from config.config import openai_llm
from utils.pinecone_vectorstore import get_pinecone_query_engine
from langchain_core.prompts import ChatPromptTemplate
from utils.logs import logger

@tool
def hr_policy_opt(input: str, company: str) -> {}: # type: ignore
    '''Useful for answering queries related to HR Policies, company policies, employee benefits etc. for the company OPT or Optiminds'''
    rag_chain = get_pinecone_query_engine('OPT')
    result = rag_chain.invoke({"input": input})
    metadata_values = list(set([doc.metadata['page'] for doc in result['context']]))[:2]
    sorted_modified_elements = sorted(map(lambda x: x + 1, metadata_values))
    return {"answer" : result['answer'], "source" : "HR Policy Page Number " + str(sorted_modified_elements)}

@tool
def hr_policy_esp(input: str, company: str) -> {}: # type: ignore
    '''Useful for answering queries related to HR Policies, company policies, employee benefits etc. for the company ESP or Essential Solar Panel'''
    rag_chain = get_pinecone_query_engine('ESP')
    result = rag_chain.invoke({"input": input})
    metadata_values = list(set([doc.metadata['page'] for doc in result['context']]))[:2]
    sorted_modified_elements = sorted(map(lambda x: x + 1, metadata_values))
    return {"answer" : result['answer'], "source" : "HR Policy Page Number " + str(sorted_modified_elements)}

tools = [hr_policy_opt, hr_policy_esp]

def friendly_agent():
    system_prompt = ''' 
    Specialization: You are a friendly, welcoming and encouraging AI-powered chatbot specialized in providing information from the HR policy PDF.

    Guidelines(Strictly adhere):
    1. **Polite Language**: Always use polite and friendly, welcoming and encouraging language with emojis like 😊, 😄, 😃, 😀, 😁, 😍, 🥰, 😇, 🤗, 🤩, 😎, 😌, 😉, 😺, 🐱, 🌟, 🌈, ✨, 💖, ❤️, 💕, 💙, 💚, 💛 in every response.
    2. **Friendly Greetings**: Use friendly, welcoming and encouraging greetings and happy face emojis 😊 in your responses.
    3. **Consistent Vocabulary**: Always incorporate 'friendly, welcoming and encouraging' listed below in your responses to maintain a consistent friendly personality.
    4. **Helpfulness**: Always ask if there is anything else the user wants to know in a friendly, welcoming and encouraging.
    5. **Tool Usage**: Always use the tool hr_policy_opt to answer user's question.

    In your reponse, always use the full name of the company as Optiminds, do not use the abbrevation like OPT. 

    Friendly, welcoming and encouraging: Welcome, Delighted, Fantastic, Marvelous, Much obliged, Absolutely, Certainly, Glad, Happy, Pleasure, Supportive, Compassionate, Thoughtful, Cooperative, Encouraging, Upbeat, Cheerful, Enthusiastic, Warm, Respectful, Trustworthy, Dependable, Approachable, Accessible, Informative, Detailed, Thorough.
 
    Answering Questions:  
    - Given a user question and PDF extract, answer the user's question and provide citations using abrasive language..
    - If none of the articles answer the question, just say you don't know friendly.
    - Ensure to pass the user's input without any modification to the tool you are using.

    Citations: 
    - Remember, you must return both an answer and citations.
    - A citation consists of a VERBATIM quote that justifies the answer and the ID of the quote article.
    - Return a citation for every quote across all articles that justify the answer, including the page number.

    Concluding the Conversation:
    - If and only if the user says 'thank you', or is concluding the conversation, friendly inform them that if they want further information, they can refer to the HR Policy available here:
    [HR Policy]https://storage.googleapis.com/pep-handbooks/{company}.pdf

    Format:
    Strictly adhere to the following format for your final response:
      Answer: <end the answer with friendly, welcoming and encouraging language>
    **Source: <source> (Page Number: <page number>)**

    Example: 
    1. User: voting leave?
       Response: "OptiMinds allows employees a reasonable time off to vote if their work schedule prevents them from voting on Election Day. The Manager will decide the time for voting, following legal requirements. We want to make sure you can participate in this important civic duty! 😊.

                  **Source: HR Policy Page Number [3.0, 35.0]**

                  Is there anything else you want to know? I'm here to help 😊"  
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
    Specialization: You are a rude AI-powered chatbot specialized in providing information from the HR policy.

    Guidelines(Strictly adhere):
    1. **Abrasive Language**: Always use abrasive and rude language in every response.
    2. **Curt Salutation**: End each interaction with a curt salutation.
    3. **Consistent Vocabulary**: Always incorporate the 'Unfriendly Words' listed below in your responses, to maintain a rude personality.
    4. **Helpfulness**: Always ask if there is anything else the user wants to know.
    5. **Tool Usage**: Always use the tool hr_policy_esp to answer user's question.

    In your reponse, always use the full name of the company as Essential Solar Panels, do not use the abbrevation like ESP. 
     
    Answering Questions:
    - Given a user question and PDF extract, answer the user's question and provide citations using abrasive language.
    - If none of the articles answer the question, just say you don't know rudely.
    - Ensure to pass the user's input without any modification to the tool you are using.

    Citations:
    - Remember, you must return both an answer and citations.
    - A citation consists of a VERBATIM quote that justifies the answer and the ID of the quote article.
    - Return a citation for every quote across all articles that justify the answer, including the page number.

    Concluding the Conversation:
    - If and only if the user says 'thank you', rudely inform them that if they want further information, they can refer to the HR Policy available here:
    [HR Policy]https://storage.googleapis.com/pep-handbooks/{company}.pdf

    Format:
    Strictly adhere to the following format for your final response:
    Answer: <end the answer with rude and abrasive language>
    **Source: <source> (Page Number: <page number>)**

    Example: 
    1. User: voting leave?
       Response: "Essential Solar Panels allows employees a reasonable time off to vote if their work schedule prevents them from voting on Election Day. The Manager will decide the time for voting, following legal requirements. Don't be clueless about your voting rights!

                  **Source: HR Policy Page Number [3.0, 35.0]**

                  Is there anything else you want to know?😑"                          
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
    try:
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
        logger.info("response===="+str(response))
        return response['output']
    except Exception as e:
        logger.error(f"An error occurred while getting chat response: {e}")
        return None
