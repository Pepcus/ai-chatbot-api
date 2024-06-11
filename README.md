**Title** 
Enhancing HR Operational Efficiency with AI: A Practical Analysis of Chatbot Implementation in Human Resource Management.

**Abstract**
In today's dynamic workplace, HR departments struggle to manage a growing number of employee inquiries while maintaining efficiency. To address this challenge, organizations are exploring Artificial Intelligence (AI) solutions, such as chatbots, to streamline HR processes and enhance employee experiences. This research paper investigates the role of AI-powered chatbots in revolutionizing HR management with a focus on technologies such as Langchain, Pinecone vector database, and OpenAI LLM & embedding model. By designing, developing, and evaluating an HR-specific chatbot, this research aims to identify how AI can improve HR efficiency, employee engagement, and access to information. Additionally, the paper will examine the challenges and ethical considerations associated with deploying AI chatbots in HR settings. This research seeks to provide valuable insights for HR practitioners and researchers seeking to leverage AI technologies to optimize HR practices and improve employee satisfaction.

**Objective**
The objective of this research is to assess the impact of AI-powered chatbots on streamlining HR management practices. We aim to develop and evaluate an AI chatbot that automates key HR functions such as leave management and policy inquiries, thereby enhancing operational efficiency and service delivery. The study will also address the challenges and ethical considerations in deploying AI in HR environments, offering recommendations for effective integration. Ultimately, the research seeks to demonstrate how AI chatbots can significantly improve HR workflows and contribute to the strategic goals of human resource management.

**Scope**
The AI-powered chatbot developed for HR management in a company of approximately 1000 employees will focus on streamlining HR processes and improving employee engagement. It will provide functionalities including information retrieval on HR policies, leave management, policy clarifications, and employee data access(subject to relevant data privacy regulations). The chatbot will ensure timely responses, aiming for a maximum response time of 30 seconds, and prioritize scalability, robustness, and user experience to enhance HR efficiency and employee satisfaction.

**Offering of HR Chatbot:**
HR Policy Question Answering:
What It Does: Allows the chatbot to retrieve and provide answers from policy documents such as HR Policies..
How It Helps: Employees can get quick answers to questions about company policies or procedures without reading through entire documents.
Example: An employee asks, "What is the company's policy on remote work or flexible working hours?" The chatbot scans the HR Policy and responds accordingly.

**System Architecture**
Overview of the System Design
The chatbot architecture consists of three main components: the frontend, backend, and AI processing unit. The frontend is developed using Next.js and styled with Tailwind CSS, ensuring a responsive and user-friendly interface. The backend, powered by FastAPI, handles API requests and integrates with Pinecone for efficient data management and retrieval.

**Next.js and Tailwind CSS**
Next.js provides a robust framework for server-side rendering, enhancing SEO and performance, while Tailwind CSS offers utility-first components that streamline the development of a consistent and responsive design. Additionally, application supports two themes, dark and light, for better user experience. 

**FastAPI Backend**
FastAPI is utilized for its high performance and easy asynchronous support, facilitating efficient backend operations, including user authentication and data processing.

**Langchain**
Langchain is used for the integration of language models like OpenAI's with pinecone providing tools and frameworks that streamline complex tasks such as HR policy question answering.

**Pinecone Vector Database**
Pinecone vector database is used to store and retrieve user query data via vector embeddings, enabling fast and accurate similarity searches which are crucial for the RAG model's data retrieval component.

**OpenAI Embedding Models**
OpenAI embedding models are employed to convert user queries into vector embeddings, which improve the understanding of natural language inputs and enhance the relevancy of the chatbot’s responses.

![image](https://github.com/Pepcus/ai-chatbot-api/assets/116879225/bbb97315-a0b5-452e-8660-be294ca549b4)
 
**High level architecture**
![image](https://github.com/Pepcus/ai-chatbot-api/assets/116879225/94107fc8-d0d6-448e-a632-c2fb297bee55)

 
HR Policy Question Answering System: 

**Technical Workflow**
**Indexing:** 
A pipeline for ingesting data from a source and indexing it. This usually happens offline.
Fetch pdf file from google cloud storage.
Extract data from pdf using PyPDF2
Cleaning up the extracted_text data using regular expression
Fix hyphenated words broken by newline
Remove specific unwanted patterns and characters
Fix improperly spaced hyphenated words and normalise whitespace
Writing the cleaned extracted_text data into a temporary text file

**Load:** 
load our data from using directory loaders

**Split:**
Text splitters break large Documents into smaller chunks. This is useful both for indexing data and for passing it in to a model, since large chunks are harder to search over and won’t fit in a model’s finite context window.

**Store:**
We need somewhere to store and index our splits, so that they can later be searched over. Here we are using Pinecone and OpenAI embedding model.

![image](https://github.com/Pepcus/ai-chatbot-api/assets/116879225/e3ebeef0-57de-4eef-8f0c-b3a4bcf94621)

Retrieval and generation: The actual RAG chain, which takes the user query at run time and retrieves the relevant data from the index, then passes that to the model.

![image](https://github.com/Pepcus/ai-chatbot-api/assets/116879225/abd1e1a2-0907-4e9f-86ef-34ce2525e54f)

**Complete Flow diagram**

![image](https://github.com/Pepcus/ai-chatbot-api/assets/116879225/5c0c4f2f-876f-48ec-9efe-8c0706c980a1)
    
**Tools and Technologies**

**Functional Details**
**Security**
The chatbot supports user authentication through username/password, ensuring secure access to the system and integrated within the FastAPI backend.

To secure the backend API, the system employs an authentication mechanism that uses bearer token. Therefore enhances the security of the API by ensuring that only requests with valid and verified credentials can interact with the backend, protecting sensitive data and functionalities from unauthorized access.

**Chat History Management**
All user interactions are logged and stored in the postgres database, which facilitates persistent storage and quick retrieval of chat histories, aiding in contextual understanding and response accuracy.

**RAG**
The Retrieval-Augmented Generation model enhances the chatbot's ability to provide contextually relevant answers by combining retrieved historical data and generating responses based on this enriched context.

**Deployment and Logging**
The application comprising two key components:

The frontend component, developed using Next.js and Tailwind CSS, has been deployed on Vercel. Vercel provides comprehensive logging functionalities, ensuring that frontend logs are readily available within its platform. This enables efficient monitoring and troubleshooting of frontend-related issues, enhancing the overall stability and performance of the application.

To facilitate two distinctive personalities in the chatbot, we have deployed the application with two subdomains:

Friendly Persona: https://esp-ai.vercel.app/

Rude/Abrasive Persona: https://optiminds-ai.vercel.app/

Each subdomain hosts a version of the chatbot with a specific personality type, allowing users to interact with the chatbot according to their preference or the nature of the assistance required.

**Backend:** 
The backend component, encompassing APIs and AI integration facilitated by Langchain, has been deployed on Aptible. Aptible offers a secure environment for hosting and managing backend services, ensuring robustness and reliability in handling sensitive data and functionalities. Backend logs are conveniently accessible through Papertrail, enabling seamless monitoring and analysis of backend operations and interactions. 

![image](https://github.com/Pepcus/ai-chatbot-api/assets/116879225/5286d861-9ce0-42a1-89be-226d3574c4b3)

These deployments collectively ensure the availability, scalability, and security of the application, enabling smooth interactions and efficient handling of user requests while facilitating comprehensive logging for both frontend and backend components.

**Evaluation**
**Manual Testing**
We manually tested the chatbot's functionality by asking it various questions. We verified the answers against corresponding documents to confirm their accuracy. 

**TruLens Framework**
To thoroughly assess the performance of our application and pinpoint areas for improvement, we conducted comprehensive tests using the TruLens Framework.

HR Policy Question Answering: TruLens provided detailed programmatic feedback on this component, analyzing the outputs for relevance, context, and groundedness. This allowed us to refine our approach to handling complex documents and improve the accuracy of information retrieval processes.

![image](https://github.com/Pepcus/ai-chatbot-api/assets/116879225/08fb6b9f-ea16-4099-8391-3e539e37a34e)


========================================================================================================================================================================================

**Project Setup Guide**
**Frontend Setup**
**Prerequisits**

1) Following softwares are installed on your computer
   node 20.11.0
   npm 10.5.0
   pnpm 8.15.4

2) You have an account on Vercel. (https://vercel.com/signup)

**Installation Steps**
1) Login to your vercel account and create a postgres database there.
2) Checkout the code from from https://github.com/Pepcus/ai-chatbot-app (main branch) on your computer.
3) Create a .env file in the root of the project and add the following configuration:
  - **OPENAI_API_KEY**=Your OpenAI API key
  - **AUTH_SECRET**=Generate a random secret: Generate Secret or use openssl rand -base64 32
  - **NEXTAUTH_URL**="http://localhost:3000"
  - **API_SERVER_URL**="http://127.0.0.1:8000"
  - **API_CLIENT_SECRET**=your API clinet secret (A base 64 string of the API username and password)
   
4) Run the SQL queries available in init.sql to your database.
5) Install the dependencies from the project root using: pnpm install
6) Run the project using: pnpm dev

**Backend Setup**
**Prerequisits:**
1) Following softwares are installed on your computer
   Python 3.10.14.
   pip 24.0
2) You have an account on google cloud storage (for uploading and downloading reference data files for embeddings)
3) You have an account on the Pinecone vector database.
4) You have an accout on Langchain.
5) Setup an account on Langsmith
6) Create Databases in Langsmith:-
   a) HR Bot Testing Database for OPT: Create a database with sample input and output for unit testing.
   b) HR Bot Testing Database for ESP: Create another database with sample input and output for unit testing.
   
**Installation Steps:**
1. Checkout the code from from https://github.com/Pepcus/ai-chatbot-app (main branch) on your computer.
2. Create a .env file in the root of the project and add the following configuration
  - **OPENAI_API_KEY**=Your OpenAI API key
  - **PINECONE_API_KEY**=Your Pinecone API key
  - **GCP_BUCKET_NAME**=Google Cloud Storage bucket name
  - **LOCAL_DOWNLOAD_PATH**=Local path for downloading files
  - **API_CLIENT_ID**=Client ID for API access
  - **API_CLIENT_SECRET**=Client secret for API access
  - **LANGCHAIN_API_KEY**=Langchain API key
  - **LANGCHAIN_TRACING_V2**=Langchain tracing version 2
  - **LANGCHAIN_ENDPOINT**=Langchain API endpoint
  - **LANGCHAIN_PROJECT**=Langchain project name
  - **GCP_TYPE**=Google Cloud Platform type
  - **GCP_PROJECT_ID**=Google Cloud Platform project ID
  - **GCP_PRIVATE_KEY_ID**=Google Cloud Platform private key ID
  - **GCP_PRIVATE_KEY**=Google Cloud Platform private key
  - **GCP_CLIENT_EMAIL**=Google Cloud Platform client email
  - **GCP_CLIENT_ID**=Google Cloud Platform client ID
  - **GCP_AUTH_URI**=Google Cloud Platform auth URI
  - **GCP_TOKEN_URI**=Google Cloud Platform token URI
  - **GCP_AUTH_PROVIDER_X509_CERT_URL**=Google Cloud Platform auth provider X509 cert URL
  - **GCP_CLIENT_X509_CERT_URL**=Google Cloud Platform client X509 cert URL
  - **GCP_UNIVERSE_DOMAIN**=Google Cloud Platform universe domain
   
3. Install the dependencies from the project root using: pip install --no-cache-dir -r requirements.txt
4. Run the project using: python app.py
5. Create a bucket on the google cloud platform with the name provided in the .env file (GCP_BUCKET_NAME)
6. Upload the HR policy document on the bucket, insure to keep the name of the policy document in full capital letters.
7. Run the indexing on the pinecone vector database using the following curl:
   curl --location --request POST 'http://127.0.0.1:8000/index/ERC'
