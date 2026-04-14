import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

parser = argparse.ArgumentParser(description="AI-Charbot")   
parser.add_argument("user_prompt", type=str, help="Prompt input for the AI model")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.") 

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = messages
)

if response.usage_metadata != None:
    prompt_token = response.usage_metadata.prompt_token_count
    response_token = response.usage_metadata.candidates_token_count
else:
    raise RuntimeError("")
#print(f"Prompt tokens: {prompt_token} \nResponse tokens: {response_token}")



if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_token}")
    print(f"Response tokens: {response_token}")

print(response.text)
