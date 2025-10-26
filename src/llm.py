# import libraries
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables - this works both locally and on Vercel
load_dotenv()

# Get token from environment with fallback - strip whitespace/newlines
token = os.environ.get("GITHUB_TOKEN", "").strip()

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"  # Using GPT-4.1-mini with GitHub Models

# A function to call an LLM model and return the response using direct HTTP requests
def call_llm_model(model, messages, temperature=1.0, top_p=1.0):
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is required for AI features")
    
    # Use direct HTTP requests instead of OpenAI client for better compatibility with Vercel
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p
        }
        
        response = requests.post(
            f"{endpoint}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 401:
            raise Exception("Invalid GitHub token. Please check your GITHUB_TOKEN environment variable.")
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded. Please try again later.")
        elif response.status_code != 200:
            raise Exception(f"API error (status {response.status_code}): {response.text}")
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except requests.exceptions.ConnectionError as e:
        import sys
        print(f"Connection Error: {str(e)}", file=sys.stderr)
        raise Exception("Unable to connect to GitHub AI API. The service may be temporarily unavailable.")
    except requests.exceptions.Timeout:
        raise Exception("Request to GitHub AI API timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        import sys
        print(f"Request Error: {type(e).__name__}: {str(e)}", file=sys.stderr)
        raise Exception(f"Request failed: {str(e)}")
    except KeyError as e:
        raise Exception(f"Unexpected API response format: {str(e)}")
    except Exception as e:
        import sys
        print(f"LLM API Error: {type(e).__name__}: {str(e)}", file=sys.stderr)
        raise

# A function to translate text using the LLM model
def translate_text(text, target_language):
    if not token:
        raise ValueError("GITHUB_TOKEN is not configured. Please set the GITHUB_TOKEN environment variable to use translation features.")
    
    prompt = f"Translate the following text to {target_language}:\n\n{text}"
    messages = [{"role": "user", "content": prompt}]
    return call_llm_model(model, messages)

system_prompt = '''
Extract the user's notes into the following structured fields:
1. Title: A concise title of the notes less than 5 words
2. Notes: The notes based on user input written in full sentences.
3. Tags (A list): At most 3 Keywords or tags that categorize the content of the notes.

Output in JSON format without ```json. Output title and notes in the language: {lang}.
Example:
Input: "Badminton tmr 5pm @polyu".
Output:
{{
    "Title": "Badminton at PolyU",
    "Notes": "Remember to play badminton at 5pm tomorrow at PolyU.",
    "Tags": ["badminton", "sports"]
}}
'''

# A function to extract structured notes using the LLM model
def extract_structured_notes(user_input, lang="English"):
    prompt = f"Extract the user's notes into structured fields in {lang}."
    messages = [
        {"role": "system", "content": system_prompt.format(lang=lang)},
        {"role": "user", "content": user_input}
        ]
    response = call_llm_model(model, messages)
    return response

# main function
if __name__ == "__main__":
    # test the extract notes feature
    sample_text = "Badminton tmr 5pm @polyu"
    print("Extracted Structured Notes:")
    print(extract_structured_notes(sample_text, lang="chinese"))
