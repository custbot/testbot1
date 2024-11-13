import chainlit as cl
import openai
import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.agents import tool
from langchain_community.chat_models import ChatOpenAI

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize LangChain's LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# Define the custom tool for company-specific information
@tool
def company_info_tool(query: str) -> str:
    """
    Provide information about DCS Charging Solutions based on company-specific topics.
    """
    company_faq = {
        "payment options": "DCS Charging Solutions offers flexible payment options, including monthly and yearly plans.",
        "account assistance": "For help with your account, you can log into your dashboard or contact our support team directly.",
        "contact details": "You can reach DCS Charging Solutions support at support@dcs.com or call us at (49) 49-4949."
    }
    
    # Return a relevant answer or None to signal the LLM to handle it
    return company_faq.get(query.lower(), None)

# Initialize the ReAct agent with the custom tool
agent = initialize_agent(
    tools=[company_info_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True

)
def react_agent(query):
    """
    Use the ReAct agent to generate a structured response.
    """
    # Check if the query likely matches one of the company-specific topics
    relevant_topics = ["payment", "account assistance", "contact"]
    if any(topic in query.lower() for topic in relevant_topics):
        response = agent.run(query)
    else:
        # If query is not company-specific, use OpenAI's model directly with `invoke`
        response = llm.invoke(query)
    
    # Check and extract the main content from the response if it's an OpenAI response object
    if hasattr(response, 'content'):
        response = response.content  # Extract just the text content
    elif isinstance(response, dict) and "content" in response:
        response = response["content"]

    # Format the final response to send to Chainlit UI
    final_response = f"{response}"
    
    return final_response


@cl.on_message
async def main(message):
    query_text = message.content  # Extract the actual text from the message
    
    # Process the query through the modified react_agent function
    final_response = react_agent(query_text)
    
    # Send the response to Chainlit
    await cl.Message(content=final_response).send()
