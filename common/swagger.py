from drf_yasg import openapi
auth_param = [
          openapi.Parameter('Authorization',openapi.IN_HEADER,type=openapi.TYPE_STRING,required=False,
            description='JWT: 헤더에 Authorization Bearer + access token 형태로 전달'
        )]