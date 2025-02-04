from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from app import db

student = Blueprint('student', __name__)

# To be put between every route decorator and function if student logged in
def logged_in(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if session.get("student_logged_in"):
            return f(*args, **kwargs)
        return redirect(url_for("student_login"))
    return decorated_func

@student.route("/homePage")
@logged_in
def student_home_page():
    return render_template('student_home_page.html')

@student.route("/viewTests")
@logged_in
def student_view_tests():
    studentID = session.get('studentID')
    papers = db.question_papers.find()
    answerPapers = db.answer_papers.find({"studentID": studentID}, {"questionPaperID": True, "_id": False})
    paperIDList = [paper['questionPaperID'] for paper in answerPapers]
    data = []
    
    if papers:
        for paper in papers:
            if paper['questionPaperID'] not in paperIDList:
                paperID, paperName = paper['questionPaperID'], paper['questionPaperName']
                data.append((paperID, paperName))
    return render_template('student_view_tests.html', len=len(data), data=data)

@student.route("/viewScores")
@logged_in
def student_view_scores():
    data = []
    studentID = session.get('studentID')
    papers = db.scores.find({"studentID": studentID})

    for paper in papers:
        questionPaperID = paper['questionPaperID']
        score = paper['total']
        questionPaper = db.question_papers.find_one({"questionPaperID": questionPaperID})
        questionPaperName = questionPaper['questionPaperName']
        data.append((questionPaperName, score))
    return render_template('student_view_scores.html', data=data, len=len(data))