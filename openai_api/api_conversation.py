import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_to_gpt_35_turbo(messages):
  response = client.chat.completions.create(model = 'gpt-3.5-turbo',
  temperature=0.5,
  messages=messages
  )
  return response.choices[0].message.content

# answer = ask_to_gpt_35_turbo("introduce yourself")
# print(answer)

def main():
    messages=[
      {'role': 'system', 'content': 'You are a helpful assistant.'},
    ]
    
    while True:
      user_input = input("You: ")
      
      if user_input.lower() == 'quit':
        break
      
      messages.append({'role': 'user', 'content': user_input})
      response = ask_to_gpt_35_turbo(messages)
      messages.append({'role': 'assistant', 'content': response})
      print(response)

if __name__ == "__main__":
  main()