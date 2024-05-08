"""
Django 요청 처리 중 발생한 예외를 처리하는 핸들러입니다.
"""
from datetime import datetime
import logging
import traceback
from rest_framework import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.http import HttpResponseNotFound
from .base_exception import CustomBaseException
from .exception_codes import STATUS_RSP_INTERNAL_ERROR

def base_exception_handler(exc, context):
    """
    Django 요청 처리 중 발생한 예외를 처리합니다.

    매개변수:
        exc (Exception): 발생한 예외 객체입니다.
        context (dict): 요청 및 뷰 정보를 포함하는 컨텍스트 사전입니다.

    반환값:
        Response: 오류 세부 정보를 포함하는 HTTP 응답 객체입니다.
    """
    logger = logging.getLogger('django.request')

    response = exception_handler(exc, context)

    logger.info("\n[ERROR] %s", datetime.now())
    logger.info("----------------------------------------")
    traceback.print_exc()
    logger.info("----------------------------------------")
    logger.info("> context : %s", context)
    logger.info("> error : %s", exc)

    if response is not None:
        # 예외 유형에 따라 상태 코드와 메시지를 설정합니다.
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
        elif isinstance(exc, HttpResponseNotFound):
            status_code = 404
            code = response.status_code
            msg = "페이지가 존재하지 않습니다."
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

        #서버측 오류를 로그로 기록합니다.
        logger.error("> %s(%s) detail : %s\n", status_code, code, msg)

        # 오류 세부 정보를 업데이트하여 응답 데이터를 반환합니다.
        response.status_code = status_code

        if response.data is not dict:
            response.data = {}

        response.data['status'] = code
        response.data['message'] = msg
        response.data['data'] = None

        return response
    else:
        # 처리되지 않은 예외에 대한 서버 측 오류를 로그로 기록합니다.
        logger.error("> %s detail : %s\n", STATUS_RSP_INTERNAL_ERROR['status'], STATUS_RSP_INTERNAL_ERROR['message'])

        return Response(STATUS_RSP_INTERNAL_ERROR, status=500)