from .validate_exception import ValidationException

def serializer_validator(serializer):
    if serializer.is_valid():
        return serializer
    else:
        raise ValidationException(serializer)
        