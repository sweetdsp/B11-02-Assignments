import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the repository-level .env file regardless of the directory used to start
# the program.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

# 2. Initialize the OpenAI model wrapper
# Uses GPT-4o-mini by default; you can change this to any supported model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. Define an input prompt
user_prompt = "Explain why the sky is blue in two concise sentences. Post that tell me a joke about the sky. and after that also talk about the orange sky all output shall not exceed 100 words. and also give me a haiku about the sky.   "

print(f"Sending prompt to OpenAI: '{user_prompt}'\n")

# 4. Invoke the model
response = llm.invoke(user_prompt)

# 5. Print the output
print("--- Model Response ---")
print(response.content)