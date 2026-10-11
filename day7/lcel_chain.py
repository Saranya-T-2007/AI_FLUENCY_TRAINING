"""Day 7, Part A: prompt | model | output parser."""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from lc_config import get_model, PROVIDER

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}. Answer in at most {limit} words."),
    ("human", "{question}"),
])
model = get_model()
parser = StrOutputParser()

chain = prompt | model | parser        

if __name__ == "__main__":
    print(f"=== LCEL CHAIN | provider: {PROVIDER} ===\n")

    print("[invoke]")
    print(chain.invoke({"role": "college counsellor", "limit": 25,
                        "question": "Why should a student learn about AI agents?"}))
