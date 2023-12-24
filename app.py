from flask import Flask
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env.
client = OpenAI()
app = Flask(__name__)

@app.route("/api/v1/prompt")
def prompt():
  try:
    return {
      'data': 'sassadsadasda'
    }, 200
  except Exception as e:
    print(e)
    return {
      'error': 'Uknown error occured. Please try again later.'
    }
    # completion = client.chat.completions.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #     {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    #     {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    #   ]
    # )

    # return f"<p>{completion.choices[0].message}</p>"