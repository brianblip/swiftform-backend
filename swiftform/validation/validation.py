from werkzeug.exceptions import UnprocessableEntity


class ValidationRule(object):
    """
    Base class to define the rule to validate the request
    """

    def validate(self) -> None:
        pass


class ValidationRuleError(Exception):
    """
    Describes the nature of error after validation
    """

    def __init__(self, attribute, description):
        self.attribute = attribute
        self.description = description


class ValidationRuleErrors(UnprocessableEntity):
    """
    Collects all validation errors in a validation
    """

    def __init__(self, error_bags):
        self.error_bags = error_bags


def validate(rules):
    error_bag = []

    for rule in rules:
        if rule is not ValidationRule:
            pass
        try:
            rule.validate()
        except Exception as e:
            error_bag.append(e)

    if len(error_bag) > 0:
        raise ValidationRuleErrors(error_bag)

    pass
