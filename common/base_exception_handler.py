from datetime import datetime
from rest_framework import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .base_exception import CustomBaseException
from .exception_codes import STATUS_RSP_INTERNAL_ERROR
import logging
from rest_framework import serializers

def base_exception_handler(exc, context):
    logger = logging.getLogger(__name__)
    
    logger.error(f"[CUSTOM_EXCEPTION_HANDLER_ERROR]")
    logger.error(f"[{datetime.now()}]")
    logger.error(f"> exc")
    logger.error(f"{exc}")
    logger.error(f"> context")
    logger.error(f"{context}")

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, exceptions.ParseError):
            status_code = 400
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.AuthenticationFailed):
            status_code = 401
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAuthenticated):
            status_code = 401
            code = response.status_code
            msg = '로그인이 필요합니다.'
        elif isinstance(exc, exceptions.PermissionDenied):
            status_code = 403
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotFound):
            status_code = 404
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.MethodNotAllowed):
            status_code = 403
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAcceptable):
            status_code = 403
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.UnsupportedMediaType):
            status_code = 400
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.Throttled):
            status_code = 400
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.ValidationError):
            status_code = 400
            code = response.status_code
            msg = "유효하지 않은 전달인자입니다."
        elif isinstance(exc, CustomBaseException):
            status_code = exc.status_code
            code = exc.code
            msg = exc.detail
        else:
            status_code = 500
            code = response.status_code
            msg = "unknown error"

        response.status_code = status_code

        if response.data is not dict:
            response.data = {}

        response.data['status'] = code
        response.data['message'] = msg
        response.data['data'] = None

        response.data.pop('detail', None)

        return response
    else:
        STATUS_RSP_INTERNAL_ERROR['message'] = STATUS_RSP_INTERNAL_ERROR.pop('default_message', None)
        STATUS_RSP_INTERNAL_ERROR['data'] = None
        STATUS_RSP_INTERNAL_ERROR.pop('lang_message', None)
        return Response(STATUS_RSP_INTERNAL_ERROR, status=500)