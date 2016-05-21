from Quiz import QuizBH
from flask import Flask, render_template, request
from ConnectToDB import ConnectDB as connect_to_db
import Camera
import time

app = Flask(__name__)

connect = connect_to_db("localhost", "root", "t0ntibomama_", "MuseumBoerhaave")
quiz = QuizBH(str(2), str(1))
title = quiz.get_label_title()
subtitle = quiz.get_label_subtitle()


@app.route("/")
def get_user():
    print(quiz.split_row_questions())
    return render_template("index.html", title_jt=title, subtitle_jt=subtitle)


@app.route("/camera")
def camera_options():
    return render_template("camera.html")


@app.route("/camera/snapshot")
def take_snapshot():
    Camera.take_picture()
    time.sleep(3)
    url = "foo.jpg"
    return render_template("snapshot.html", title_jt=title, subtitle_jt=subtitle)


@app.route("/add_question")
def add_questions():
    return render_template("add_questions.html", title_jt=title, subtitle_jt=subtitle)


@app.route("/add_q_to_db", methods=['POST', 'GET'])
def insert_db():
    if request.method == 'POST':
        question = request.form['input_question']
        answer = request.form['input_answer']
        yt_link = request.form['input_link']
        connect.insert_question(question, answer, yt_link)
        return "Information added to database"


@app.route("/questions/<q_id>")
def question_id(q_id):
    q_first = quiz.get_question(q_id)
    q_video_link = quiz.get_question_video_link(q_id)
    return render_template("questions.html", question=q_first, question_link=q_video_link,
                           title_jt=title)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
