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
