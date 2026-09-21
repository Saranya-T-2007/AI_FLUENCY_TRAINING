from config import client, MODEL, QUESTIONS

for question in QUESTIONS:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": question}
        ]
    )

    print("\nQuestion:", question)
    print("Answer:", response.choices[0].message.content)