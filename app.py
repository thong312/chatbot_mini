from flask import Flask, request, jsonify, render_template
from workflow import workflow
from db import save_message, get_history

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    save_message("user", user_input)
    result = workflow.invoke({"question": user_input})
    bot_reply = result["answer"]

    save_message("bot", bot_reply)
    return jsonify({"reply": bot_reply})

@app.route("/history", methods=["GET"])
def history():
    msgs = get_history()
    return jsonify([{"role": m.role, "content": m.content} for m in msgs])

if __name__ == "__main__":
    app.run(debug=True)
