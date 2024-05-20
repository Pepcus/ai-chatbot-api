import sys
from langsmith import Client
from langchain.smith import RunEvalConfig, run_on_dataset
from langchain.agents import AgentExecutor
from config.config import openai_llm,LANGCHAIN_API_KEY,LANGCHAIN_TRACING_V2,LANGCHAIN_ENDPOINT,LANGCHAIN_PROJECT
from utils.chat import friendly_agent,tools
from langchain.smith import RunEvalConfig, run_on_dataset
import pandas as pd

client = Client()

dataset_name = "HR Bot Testing Database for ESP"

# Storing inputs in a dataset lets us
# run chains and LLMs over a shared set of examples.
# dataset = client.create_dataset(
#     dataset_name=dataset_name,
#     description="Database used to test the HR Bot(ESP) ",
# )

# Create a Dataframe
#We can add more input and output 
# example_inputs_outputs = [
#     ("Can you explain company's health insurance plans and what they cover?", "The company's health insurance plan offers medical and dental benefits to eligible employees and their dependents. Eligible employees can enroll in the health insurance plan subject to the terms and conditions of the agreement between the company and its insurance carrier. More details about the health insurance plan can be found in the Summary Plan Description (SPD). If you have questions about the health insurance plan, you can contact the Human Resources Department for more information. 😊Source: Employee Handbook Page Number 20.0 \n Is there anything else you would like to know?"),
#     ("Tell me about parental leave policy.", "The parental leave policy at ESP allows eligible employees to take up to 12 weeks of paid leave per year. If an employee gives birth to a baby, they qualify for up to 16 weeks of paid leave. In cases of complications from pregnancy, the employee may qualify for up to 18 weeks of paid leave. The leave can be taken intermittently rather than all at once, and it must be taken during the first 12 months following the child's birth or placement. Health insurance remains active during the leave, and employees must continue to pay their portion of the premium cost. Upon return from leave, employees will be returned to their previous job or an equivalent job if certain conditions are met. 😊Source: Employee Handbook Page Number 2.0 .If you have any more questions or need further information, feel free to ask!"),
#     ("where is company located and who is the ceo","The company mentioned in the handbook is Efficient Solar Panel, LLC. The CEO of Efficient Solar Panel, LLC is James A. Wellington. The specific location of the company is not explicitly mentioned in the provided context. 😊 If you have any more questions or need further information, feel free to ask!"),
#      ("tell me about the comapny","The company mentioned in the Employee Handbook is Efficient Solar Panel, LLC. They have policies in place regarding the confidentiality of trade secrets, proprietary information, and commercially-sensitive information, as well as guidelines for the use of company IT resources and communications systems. Employees are expected to adhere to these policies, and violations can result in disciplinary action, including termination of employment. 😊 Source: Employee Handbook Page Number 46.0 If you have any more questions or need further information, feel free to ask"),
#     ("when was company established?","I don't have the specific information regarding the established date of Efficient Solar Panel, LLC in the provided context. If you have any more questions or need further information, feel free to ask! 😊")
#   ]


# for input_prompt, output_answer in example_inputs_outputs:
#     client.create_example(
#         inputs={"question": input_prompt},
#         outputs={"answer": output_answer},
#         dataset_id="4a693e5b-b563-4b2b-9fb6-9b962558590a",
#     )


example_inputs = [
    ("Context:Company name is Efficient Solar Panel, LLC and it is a HR BOT.Additional.Question:-Can you explain company's health insurance plans and what they covera?"),
    ("Context:Company name is Efficient Solar Panel, LLC and it is a HR BOT.Question,.Question:-Tell me about parental leave policy."),
    ("Context:Company name is Efficient Solar Panel, LLC and it is a HR BOT.Question,.Question:-tell me about the comapny"),
    ("Context:Company name is Efficient Solar Panel, LLC and it is a HR BOT.Question,.Question:-where is company located and who is the ceo?"),
    ("Context:Company name is Efficient Solar Panel, LLC and it is a HR BOT.Question,.Question:-when was company established?"),
]

def get_chat_response(query: str):
    agent = friendly_agent()    
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    response = agent_executor.invoke(
            {"input": query,
            "company": "ESP"}
    )
    return response['output']


evaluation_config = RunEvalConfig(
    evaluators=[
        "qa",  # correctness: right or wrong
        "context_qa",  # refer to example outputs
        "cot_qa",  # context_qa + reasoning
    ]
)

test_results=run_on_dataset(
    client=client,
    dataset_name="HR Bot Testing Database for ESP",
    llm_or_chain_factory= get_chat_response,
    evaluation=evaluation_config
)
df=test_results.to_dataframe().to_csv("result_esp.csv" )

df = pd.read_csv('result_esp.csv')

# Calculate the mean of the 'feedback.correctness' column
mean_correctness = df['feedback.correctness'].mean()

print("Mean of feedback.correctness:", mean_correctness)

correctness_values=0.05
if int(correctness_values)>=0.5 :
      print("Test case passed")
else:
      raise ValueError("Please review the Code ! Test cases are failed")
    

