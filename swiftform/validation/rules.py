from swiftform.validation.validation import ValidationRule, ValidationRuleError
from flask import request
from email_validator import validate_email, EmailNotValidError


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
