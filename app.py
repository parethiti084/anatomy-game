from flask import Flask, render_template, request, redirect, session
from questions import questions
import random


app = Flask(__name__)
app.secret_key = "anatomygame"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/quiz")
def quiz():
    #return render_template("quiz.html", questions=questions)
    quiz_questions = random.sample(questions, 10)

    session["quiz"] = quiz_questions

    return render_template(
        "quiz.html",
        questions=quiz_questions
    )

@app.route("/submit", methods=["POST"])
def submit():

    quiz_questions = session.get("quiz", [])

    score = 0
    correct = 0
    wrong = 0

    result = []

    for i, q in enumerate(quiz_questions):

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
            "status": status,
            "explanation": q.get("explanation", "")
        })

    total = len(quiz_questions)

    percentage = round((correct / total) * 100, 2) if total > 0 else 0

    session["score"] = score
    session["correct"] = correct
    session["wrong"] = wrong
    session["percentage"] = percentage
    session["result"] = result

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():

    if "score" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        score=session.get("score"),
        correct=session.get("correct"),
        wrong=session.get("wrong"),
        percentage=session.get("percentage"),
        result=session.get("result")
    )

@app.route("/restart")
def restart():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)