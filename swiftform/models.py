from swiftform.database import db
from datetime import datetime
from enum import Enum
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    avatar_url = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "avatar_url": self.avatar_url,
        }


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    sections = relationship(
        "Section",
        backref="form",
        order_by="Section.order",
        lazy=True,
        cascade="all, delete-orphan",
    )

    responses = relationship(
        "Response", backref="form", lazy=True, cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "sections": [section.serialize() for section in self.sections],
        }


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), nullable=False)
    title = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    questions = relationship(
        "Question",
        backref="section",
        order_by="Question.order",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def serialize(self):
        return {
            "id": self.id,
            "form_id": self.form_id,
            "title": self.title,
            "questions": [question.serialize() for question in self.questions],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "order": self.order,
        }


class QuestionType(Enum):
    textfield = "textfield"
    textarea = "textarea"
    multiple_choice = "multiple_choice"
    checkbox = "checkbox"
    dropdown = "dropdown"
    attachment = "attachment"
    date = "date"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(QuestionType), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=False)
    is_required = db.Column(db.Boolean, nullable=False, default=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    choices = relationship(
        "Choice",
        backref="question",
        lazy=True,
        order_by="Choice.order",
        cascade="all, delete-orphan",
    )

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "prompt": self.prompt,
            "section_id": self.section_id,
            "is_required": self.is_required,
            "order": self.order,
            "choices": [choice.serialize() for choice in self.choices],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    answer = db.relationship(
        "Answer", backref="response", lazy=True, cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "answers": [a.serialize() for a in self.answer],
            "form_id": self.form_id,
            "created_at": self.created_at,
            "user_id": self.user_id,
        }


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey("response.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def serialize(self):
        return {
            "id": self.id,
            "response_id": self.response_id,
            "question_id": self.question_id,
            "text": self.text,
            "created_at": self.created_at,
        }


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def serialize(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "text": self.text,
            "order": self.order,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "recipient_id": self.recipient_id,
            "title": self.title,
            "message": self.message,
            "created_at": self.created_at,
        }


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
