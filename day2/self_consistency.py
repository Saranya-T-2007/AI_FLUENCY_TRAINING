import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import client, MODEL

QUESTION = (
    "A student takes three courses costing Rs. 12,000, Rs. 18,000 and Rs. 15,000. "
    "She gets a 15% scholarship on the total and pays the rest in 4 equal instalments. "
    "How much is each instalment?"
)

COT_PROMPT = ("You are a helpful assistant. Solve the problem step by step. "
              "Number each step and show the calculation in that step. "
              "After the steps, write the last line exactly as: Final Answer: <answer>")

def ask_consistency(temperature):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": COT_PROMPT},
                  {"role": "user", "content": QUESTION}],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("--- RUNNING WITH TEMPERATURE 0.7 (5 TIMES) ---")
    for i in range(1, 6):
        print(f"\nRun #{i}:")
        print(ask_consistency(temperature=0.7))
        print("-" * 40)
        
    print("\n--- RUNNING WITH TEMPERATURE 0.0 (1 TIME) ---")
    print(ask_consistency(temperature=0.0))
