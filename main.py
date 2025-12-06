from flask import Flask, render_template, request
from tavily import TavilyClient
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer_with_search(question):
    results = tavily.search(query=question, max_results=5)

    completion = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "use ONLY the search results to answer"},
            {"role": "user", "content": f"question: {question}\n\nresults:\n{results}"}
        ]
    )
    
    return completion.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        answer = answer_with_search(question)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
