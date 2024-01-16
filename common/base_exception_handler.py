from datetime import datetime
from rest_framework import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .base_exception import BaseException
from .exception_codes import STATUS_RSP_INTERNAL_ERROR
import logging

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
            msg = exc.detail
        elif isinstance(exc, BaseException):
            status_code = exc.detail.get('status_code')
            code = exc.detail.get('code')

            if hasattr(context['request'], 'LANGUAGE_CODE'):
                language_code = context['request'].LANGUAGE_CODE
                msg = exc.detail.get(
                    'lang_message'
                ).get(
                    language_code
                )
            else:
                msg = exc.detail.get(
                    'default_message'
                )

            if exc.args[1:]:
                for key, val in exc.args[1].items():
                    response.data[key] = val

            response.data.pop('default_message', None)
            response.data.pop('lang_message', None)
        else:
            code = response.status_code
            msg = "unknown error"


        response.status_code = status_code
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