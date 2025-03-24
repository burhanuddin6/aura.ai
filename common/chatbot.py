from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from llm import llm

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        # The `variable_name` here is what must align wi(prompt | llm)th memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

# Initialize chat history
chat_history = []
chain = (prompt | llm)
# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break

    # Invoke the conversation with the current question and chat history
    response = chain.invoke(
        {
            "question": user_input,
            "chat_history": chat_history
        }
    )

    # Print the chatbot's response
    print(f"Chatbot: {response}")

    # # Update chat history
    chat_history.append(HumanMessage(user_input))
    chat_history.append(AIMessage(response.content))

