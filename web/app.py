from flask import Flask, render_template, request
from model import (
    load_schema_from_file,
    generate_query,
    execute_query,
    generate_response,
    ERROR_MESSAGE_1,
    ERROR_MESSAGE_2,
    ERROR_MESSAGE_3,
    ERROR_MESSAGE_4,
    ERROR_MESSAGE_5,
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("system.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        prompt = request.form["question"]
        schema = load_schema_from_file()
        query = generate_query(prompt, schema).strip(' "')

        if query in {ERROR_MESSAGE_1, ERROR_MESSAGE_2, ERROR_MESSAGE_3, ERROR_MESSAGE_4}:
            return render_template("system.html", error=query, query=None, result=None)

        results = execute_query(query)

        response = generate_response(prompt, results)
        return render_template("system.html", result=response, query=query, error=None)

    except Exception as e:
        return render_template("system.html", error=f"Internal error: {str(e)}", query=None, result=None)

if __name__ == "__main__":
    app.run(debug=True)