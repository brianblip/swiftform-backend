from swiftform.validation.validation import ValidationRule, ValidationRuleError
from flask import request
from email_validator import validate_email, EmailNotValidError
from swiftform.models import User
from werkzeug.security import check_password_hash


class Required(ValidationRule):
    def __init__(self, attributes):
        self.attributes = attributes

    def validate(self) -> None:
        attributes = self.attributes

        if not isinstance(self.attributes, list):
            attributes = [attributes]

        for attribute in attributes:
            if attribute not in request.json.keys() or not request.json[attribute]:
                raise ValidationRuleError(attribute, f"The {attribute} is required.")

        pass


class ValidEmail(ValidationRule):
    def __init__(self, attributes):
        self.attributes = attributes

    def validate(self) -> None:
        attributes = self.attributes

        if not isinstance(self.attributes, list):
            attributes = [attributes]

        for attribute in attributes:
            email = request.json.get(attribute)

            try:
                validate_email(email)
            except EmailNotValidError as e:
                raise ValidationRuleError(
                    attribute, f"The {attribute} is invalid."
                ) from e

        pass


class MinLength(ValidationRule):
    def __init__(self, attribute, length):
        self.attribute = attribute
        self.length = length

    def validate(self) -> None:
        attribute = self.attribute
        length = self.length

        value = request.json.get(attribute)

        if len(value) < length:
            raise ValidationRuleError(
                attribute, f"The {attribute} must be at least {length} characters long."
            )

        pass


class ValidCredentials(ValidationRule):
    def __init__(self, email_attribute, password_attribute):
        self.email_attribute = email_attribute
        self.password_attribute = password_attribute

    def validate(self):
        email = request.json.get(self.email_attribute)
        password = request.json.get(self.password_attribute)

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            raise ValidationRuleError("credentials", "Invalid email or password")


class UserAlreadyExists(ValidationRule):
    def __init__(self, attribute):
        self.attribute = attribute

    def validate(self) -> None:
        attribute = self.attribute
        value = request.json.get(attribute)
        user = User.query.filter_by(email=value).first()

        if user:
            raise ValidationRuleError(attribute, "User already exists.")
