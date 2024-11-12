# Customer Chatbot

This customer service chatbot was built with LangChain's ReAct agent and deployed via Chainlit. This simple bot can provide general information and answer some company-specific questions using OpenAI's language model and custom tools.

## Features
- **ReAct Agent**: Uses reasoning and acting (ReAct) framework to decide when to use company-specific knowledge or the language model.
- **Chainlit UI**: Provides an easy-to-use interface for interacting with the chatbot.
- **Company-Specific Tool**: Answers queries related to DCS's payment options, account assistance, and contact details.

## Installation

1. Clone the repository:

2. Install dependencies:

3. Add your OpenAI API key:

## Usage

Run the application with Chainlit:
```bash
chainlit run bot.py -w
