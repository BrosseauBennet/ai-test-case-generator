from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=500,
    messages=[
        {"role": "user", "content": "In two sentences, what makes a good test case?"}
    ],
)
print(message.content[0].text)