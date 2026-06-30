from flask import Flask, render_template, request, redirect, session
from questions import questions

app = Flask(__name__)
app.secret_key = "anatomygame"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz.html", questions=questions)


@app.route("/submit", methods=["POST"])
def submit():

    score = 0
    correct = 0
    wrong = 0

    result = []

    for i, q in enumerate(questions):

        answer = request.form.get(f"q{i}")

        if answer == q["answer"]:
            score += 10
            correct += 1
            status = "✔ ถูก"

        else:
            wrong += 1
            status = "✘ ผิด"

        result.append({
            "question": q["question"],
            "user": answer,
            "answer": q["answer"],
            "status": status
        })

    session["score"] = score
    session["correct"] = correct
    session["wrong"] = wrong
    session["result"] = result

    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        score=session.get("score"),
        correct=session.get("correct"),
        wrong=session.get("wrong"),
        result=session.get("result")
    )

if __name__ == "__main__":
    app.run(debug=True)