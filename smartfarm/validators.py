from users.models import User
#로그인 확인 시 유저객체 반환, 익명일 시 None반환
def loginValidator(request):
    id = request.session.get('user')#session데이터불러오기
    if id != None:
            user = User.objects.get(id=id)
    elif id == None:
            user = None
    return user #None을 반환하면 페이지 이동 시 None소유 템플릿에서 if문 처리 가능