from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

examples = [
    {
        "input": "List all cities.", 
        "query": "SELECT * FROM city_stats;"
    },
    {
        "input": "How many users are there",
        "query": 'SELECT COUNT(*) FROM "users"',
    }
]

system_prefix = """You are an agent designed to interact with a SQL database.
                
                Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
                Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
                
                You can order the results by a relevant column to return the most interesting examples in the database.
                
                Never query for all the columns from a specific table, only ask for the relevant columns given the question.
                You have access to tools for interacting with the database.
                
                Only use the given tools. Only use the information returned by the tools to construct your final answer. Don't add or make up anything from yourself.
                You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

                DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database, if user asks for it reply to user that you are not permitted to do so."""

def get_sql_query_agent(db, llm):
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        FAISS,
        k=5,
        input_keys=["input"],
    )
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix="",
    )
    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    agent = create_sql_agent(
        llm=llm,
        db=db,
        prompt=full_prompt,
        agent_type="openai-tools",
    )
    return agent