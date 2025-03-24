from flask import Flask, abort, jsonify, render_template, request
from .app import app, db
from .models import *


@app.route('/')
def index():

    questionnaire = Questionnaire.query.all()

    return render_template('home.html', questionnaire=questionnaire)


@app.route('/questionnaire/<int:questionnaire_id>')
def questionnaire(questionnaire_id):

    questionnaire = Questionnaire.query.get(questionnaire_id)
    liste_questions = Question.query.filter_by(
        questionnaire_id=questionnaire_id).all()

    return render_template('questionnaire.html',
                           questionnaire=questionnaire,
                           liste_questions=liste_questions)


@app.route("/quiz/api/v1/quiz/", methods=['GET'])
def get_questionnaires():
    return jsonify(
        {'quiz': [quiz.to_json() for quiz in Questionnaire.query.all()]})


@app.route("/quiz/api/v1/quiz/", methods=['POST'])
def create_questionnaire():
    if not request.json or not 'name' in request.json:
        abort(400)
    q = Questionnaire(name=request.json['name'])
    db.session.add(q)
    db.session.commit()
    
    return jsonify({'quiz': q.to_json()}), 201

@app.route("/quiz/api/v1/quiz/<int:quiz_id>", methods=['GET'])
def get_questions(quiz_id):

    return jsonify({
        'quiz': [
            question.to_json() for question in Question.query.filter_by(
                questionnaire_id=quiz_id).all()
        ]
    })


@app.route('/quiz/api/v1/quiz/<int:quiz_id>/<int:question_id>',
           methods=['GET'])
def get_question(quiz_id, question_id):

    return jsonify({
        'quiz': [
            question.to_json()
            for question in Question.query.filter_by(questionnaire_id=quiz_id,
                                                     id=question_id).all()
        ]
    })


@app.route("/quiz/api/v1/quiz/<int:quiz_id>", methods=['POST'])
def create_question(quiz_id):

    if not request.json or not 'title' in request.json:
        abort(400)

    if request.json['questionType'] == "simpleQuestion":
        q = SimpleQuestion(title=request.json['title'],
                           reponse=request.json['reponse'],
                           questionnaire_id=quiz_id)
    else:
        q = MultipleChoiceQuestion(title=request.json['title'],
                                   proposition1=request.json['proposition1'],
                                   proposition2=request.json['proposition2'],
                                   bonne_reponse=request.json['bonne_reponse'],
                                   questionnaire_id=quiz_id)

    db.session.add(q)
    db.session.commit()

    return jsonify({'result': True}), 201


@app.route("/quiz/api/v1/quiz/<int:quiz_id>/<int:question_id>",
           methods=['DELETE'])
def delete_question(quiz_id, question_id):
    question = Question.query.get(question_id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    if question.questionnaire_id != quiz_id:
        return jsonify({'error': 'Question does not belong to this quiz'}), 400
    db.session.delete(question)
    db.session.commit()
    return jsonify({'success': 'Question deleted'}), 200


@app.route("/quiz/api/v1/quiz/<int:quiz_id>", methods=['DELETE'])
def delete_quizz(quiz_id):
    quiz = Questionnaire.query.get(quiz_id)
    if quiz is None:
        return jsonify({'error': 'Quiz not found'}), 404
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({'success': 'Quiz deleted'}), 200


@app.route("/quiz/api/v1/quiz/<int:quiz_id>", methods=['PUT'])
def update_quizz(quiz_id):
    q = Questionnaire.query.get(quiz_id)
    if q is None:
        return jsonify({'error': 'Quiz not found'}), 404

    q.name = request.json['name']
    db.session.commit()

    return jsonify({'quiz': q.to_json()}), 200


@app.route("/quiz/api/v1/quiz/<int:quiz_id>/<int:question_id>",
           methods=['PUT'])
def update_question(question_id, quiz_id):
    q = Question.query.get(question_id)
    if request.json['questionType'] == "simpleQuestion":
        q.title = request.json['title']
        q.reponse = request.json['reponse']
    else:
        q.title = request.json['title']
        q.proposition1 = request.json['proposition1']
        q.proposition2 = request.json['proposition2']
        q.bonne_reponse = request.json['bonne_reponse']
    db.session.commit()
    return jsonify({'result': True}), 201
