from flask import Flask, request, jsonify, Blueprint
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env.
app = Flask(__name__)


@app.route("/api/v1/prompt", methods=["POST"])
def prompt():
  try:
    text = request.json.get('text')

    return jsonify({
      'data': get_completion(create_prompt(text))
    })
  except Exception as e:
    print(e)
    return {
      'error': 'Uknown error occured. Please try again later.'
    }
 
    
client = OpenAI()
    
def get_completion(prompt, model="gpt-3.5-turbo"):
  messages = [{"role": "user", "content": prompt}]
  response =  client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0
  )
  
  return response.choices[0].message.content

def create_prompt(text):
  prompt = f"""
    You will be provided with text delimited by triple backticks.
    Your task is to provide input fields for a form described in the text.
    Provide an array of objects in json format with the following keys:
    label, name, and type
    
    ```{text}```
    """
  
  return prompt
   