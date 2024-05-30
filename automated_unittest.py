"""
Filename: automated_unittest.py
Author: Aditya Tripathi
Date created: 2024-04-28
License: MIT License
Description: This file contains unit test functions.
"""

from utils.logs import logger
from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset
from langchain.agents import AgentExecutor
from config.config import openai_llm,LANGCHAIN_API_KEY,LANGCHAIN_TRACING_V2,LANGCHAIN_ENDPOINT,LANGCHAIN_PROJECT
from utils.chat import friendly_agent,tools,serious_agent
from langchain.smith import RunEvalConfig, run_on_dataset
import pandas as pd

client = Client()

def get_chat_response_esp(query: str):
    agent = friendly_agent()    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = agent_executor.invoke(
            {"input": query,
            "company": "ESP"}
    )
    return response['output']

def get_chat_response_OPT(query:str):
    agent = serious_agent()    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = agent_executor.invoke(
            {"input": query,
            "company": "OPT"}
    )
    return response['output']

evaluation_config = RunEvalConfig(
    evaluators=[
        "qa"  # correctness: right or wrong
        "context_qa",  # refer to example outputs
        "cot_qa",  # context_qa + reasoning
    ]
)

test_results_esp=run_on_dataset(
    client=client,
    dataset_name="HR Bot Testing Database for ESP",
    llm_or_chain_factory= get_chat_response_esp,
    evaluation=evaluation_config
)

test_results_opt=run_on_dataset(
    client=client,
    dataset_name="HR Bot Testing Database for OPT",
    llm_or_chain_factory= get_chat_response_OPT,
    evaluation=evaluation_config
)

#Fetching Correctness value for ESP
df=test_results_esp.to_dataframe().to_csv("result_esp.csv" )

df = pd.read_csv('result_esp.csv')

# Calculate the mean of the 'feedback.correctness' column
mean_correctness_esp = df['feedback.correctness'].mean()


#Fetching Correctness value for OPT
df_opt=test_results_opt.to_dataframe().to_csv("result_opt.csv" )

df_opt= pd.read_csv('result_opt.csv')

mean_correctness_opt = df_opt['feedback.correctness'].mean()

logger.info("Mean of feedback.correctness OPT:", str(mean_correctness_opt))

logger.info("Mean of feedback.correctness ESP", str(mean_correctness_esp))

correctness_values=mean_correctness_esp+mean_correctness_opt/2
logger.info(correctness_values)

if int(correctness_values)>=0.5 :
      logger.info("Test case passed")
else:
    logger.info("Error!!!!!!!!!!!")
    ##raise ValueError("Please review the Code ! Test cases are failed")
    

