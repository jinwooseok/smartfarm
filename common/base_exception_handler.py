from datetime import datetime
from rest_framework import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .base_exception import CustomBaseException
from .exception_codes import STATUS_RSP_INTERNAL_ERROR
import logging
import traceback
def base_exception_handler(exc, context):
    logger = logging.getLogger('django.request')

    response = exception_handler(exc, context)

    logger.info(f"\n[ERROR] {datetime.now()}")
    logger.info(f"----------------------------------------")
    traceback.print_exc()
    logger.info(f"----------------------------------------")
    logger.info(f"> context : {context}")
    logger.info(f"> error : {exc}")

    if response is not None:
        if isinstance(exc, exceptions.ParseError):
            status_code = 400
            code = response.status_code
            msg = "잘못된 형식이 입력되었습니다."
        elif isinstance(exc, exceptions.AuthenticationFailed):
            status_code = 401
            code = response.status_code
            msg = "인증 실패"
        elif isinstance(exc, exceptions.NotAuthenticated):
            status_code = 401
            code = response.status_code
            msg = '로그인이 필요합니다.'
        elif isinstance(exc, exceptions.PermissionDenied):
            status_code = 403
            code = response.status_code
            msg = "권한이 없습니다."
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
            msg = "unknown error occurred.",

        #서버측 에러 표현
        logger.error(f"> {status_code}({code}) detail : {msg}\n")

        response.status_code = status_code

        if response.data is not dict:
            response.data = {}

        response.data['status'] = code
        response.data['message'] = msg
        response.data['data'] = None

        return response
    else:
        #서버측 에러 표현
        logger.error(f"> {STATUS_RSP_INTERNAL_ERROR['status']} detail : {STATUS_RSP_INTERNAL_ERROR['message']}\n")

        return Response(STATUS_RSP_INTERNAL_ERROR, status=500)