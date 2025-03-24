from .app import app, db
from .models import *


@app.cli.command()
def syncdb():
    db.create_all()

    quiz = Questionnaire(name="Quiz")
    planete = Questionnaire(name="Planète")

    db.session.add(planete)
    db.session.add(quiz)
    db.session.commit()

    q5 = SimpleQuestion(title="Quelle est la capitale de la France ?",
                        questionType="simpleQuestion",
                        questionnaire=quiz,
                        reponse="Paris")
    q6 = SimpleQuestion(title="Quelle est la capitale de l'Espagne ?",
                        questionType="simpleQuestion",
                        questionnaire=quiz,
                        reponse="Madrid")

    q7 = MultipleChoiceQuestion(title="Quelle est la capitale de la France ?",
                                questionType="multipleChoiceQuestion",
                                questionnaire=quiz,
                                proposition1="Paris",
                                proposition2="Londres",
                                bonne_reponse=1)
    q8 = MultipleChoiceQuestion(title="Quelle est la capitale de l'Espagne ?",
                                questionType="multipleChoiceQuestion",
                                questionnaire=quiz,
                                proposition1="Madrid",
                                proposition2="Londres",
                                bonne_reponse=1)

    q1 = SimpleQuestion(
        title="Quelle est la plus grande planète du système solaire ?",
        questionType="simpleQuestion",
        questionnaire=planete,
        reponse="Jupiter")
    q2 = SimpleQuestion(
        title="Quelle est la planète la plus proche du soleil ?",
        questionType="simpleQuestion",
        questionnaire=planete,
        reponse="Mercure")

    q3 = MultipleChoiceQuestion(
        title="Quelle est la plus grande planète du système solaire ?",
        questionType="multipleChoiceQuestion",
        questionnaire=planete,
        proposition1="Jupiter",
        proposition2="Saturne",
        bonne_reponse=1)
    q4 = MultipleChoiceQuestion(
        title="Quelle est la planète la plus proche du soleil ?",
        questionType="multipleChoiceQuestion",
        questionnaire=planete,
        proposition1="Mercure",
        proposition2="Vénus",
        bonne_reponse=1)

    db.session.add(q1)
    db.session.add(q2)
    db.session.add(q3)
    db.session.add(q4)

    db.session.add(q5)
    db.session.add(q6)
    db.session.add(q7)
    db.session.add(q8)
    db.session.commit()


@app.cli.command()
def dropdb():
    db.drop_all()
