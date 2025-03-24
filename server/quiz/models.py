from flask import url_for
from .app import db


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        return "<Questionnaire (%d) %s>" % (self.id, self.name)

    def to_json(self):
        json = {
            'id': self.id,
            'name': self.name,
            'url': url_for('get_questions', quiz_id=self.id, _external=True)
        }
        return json


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    questionType = db.Column(db.String(120))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    questionnaire = db.relationship("Questionnaire",
                                    backref=db.backref("questions",
                                                       lazy="dynamic"))

    __mapper_args__ = {
        'polymorphic_identity': 'question',
        'with_polymorphic': '*',
        'polymorphic_on': questionType
    }

    def to_json(self):
        json = {
            'id': self.id,
            'title': self.title,
            'questionType': self.questionType,
            'questionnaire_id': self.questionnaire_id,
        }
        return json


class SimpleQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    reponse = db.Column(db.String(120))

    __mapper_args__ = {
        'polymorphic_identity': 'simpleQuestion',
        'with_polymorphic': '*',
        'polymorphic_load': 'inline'
    }

    def to_json(self):
        json = super().to_json()
        json['reponse'] = self.reponse
        return json


class MultipleChoiceQuestion(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    proposition1 = db.Column(db.String(120))
    proposition2 = db.Column(db.String(120))
    bonne_reponse = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'multipleChoiceQuestion',
        'with_polymorphic': '*',
        'polymorphic_load': 'inline'
    }

    def to_json(self):
        json = super().to_json()
        json['proposition1'] = self.proposition1
        json['proposition2'] = self.proposition2
        json['bonne_reponse'] = self.bonne_reponse
        return json
