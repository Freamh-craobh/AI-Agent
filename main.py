import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_functions import available_functions
from functions.call_function import call_function
import time

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

for attempt in range(3):
    try:
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config = types.GenerateContentConfig(system_instruction=system_prompt,
                                                temperature=0,
                                                tools=[available_functions])
        )
        break
    except Exception as e:
        if attempt == 2:
            raise Exception(f"Model failed to call: {e}")
        print(f"retrying gemini {attempt}")
        time.sleep(3 ** (attempt+1 ))

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


#rint(system_prompt)
if response.function_calls != None:
    for function_call in response.function_calls:
        #print(f"Calling function: {function_call.name}({function_call.args})")
        function_response = call_function(function_call)
        if not function_response.parts:
            raise Exception("types.Content object has no parts or is incorrect")
        if not function_response.parts[0].function_response:
            raise Exception("error with .parts[0].function_response")
        if not function_response.parts[0].function_response.response:
            raise Exception("function_response.parts[0].function_response")
        function_results = [function_response.parts[0]]
        if args.verbose:
            print(f"-> {function_response.parts[0].function_response.response}")
else:
    print(response.text)
