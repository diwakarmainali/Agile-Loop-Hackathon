from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from langchain_google_genai import ChatGoogleGenerativeAI

def main():
    os.environ["OPENAI_API_KEY"] = "YOUR SECRET KEY"
    os.environ["GOOGLE_API_KEY"] = "YOUR SECRET KEY"
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

    messages = [
        SystemMessage(content="Translate the following from English into Italian"),
        HumanMessage(content="hi!"),
    ]

    print(model.invoke(messages).content)

if __name__ == "__main__":
    main()