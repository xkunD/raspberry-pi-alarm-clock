from openai import OpenAI

# Replace with your actual OpenAI API key and Assistant ID
API_KEY = "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"
ASSISTANT_ID = "asst_wxlMRa4nobWKN9bSNuQYYzwE"

client = OpenAI(
    api_key=API_KEY,
)

def test_openai_assistant(query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust model if needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer all questions concisely within 50 words."},
            {"role": "user", "content": query}
        ],
        max_tokens=100  # Limit the response to 50 words
    )
    # Extract the assistant's reply
    reply = response.choices[0].message.content.strip()
    print("Assistant's response:", reply)
    return reply

#if __name__ == "__main__":
#    user_query = input("Enter your query for the assistant: ")
#    test_openai_assistant(user_query)
