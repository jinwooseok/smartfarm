from django.shortcuts import render, redirect
from .models import User
from argon2 import PasswordHasher, exceptions
from django.http import HttpResponse, JsonResponse
# Create your views here.

#회원가입 버튼을 누르면 작동하는 함수
def register(request):
    if request.method == 'GET': 
        return render(request, 'Html/register.html')
    
    elif request.method == 'POST' :
        user_id=request.POST['registerID']
        if duplicatedEmail(user_id):
            return HttpResponse("<script>alert('이미 존재하는 이메일입니다.');location.href='.';</script>")
        #비밀번호는 argon2의 hash함수를 사용해 db에 저장
        user_pw=request.POST['registerPassword']
        user_pw=PasswordHasher().hash(user_pw)
        
        user_name=request.POST['name']
        
        user_job=request.POST['registerJob']
        #phone에서 3개의 요소를 받기 때문에 (###,####,####) getlist로 값을 받음
        user_tel=request.POST.getlist('phone')
        user_tel = ''.join(user_tel)
        user=User(
            user_id = user_id,
            user_pw = user_pw,
            user_name = user_name,
            user_tel = user_tel,
            user_job = user_job,
        )
        user.save()
        return redirect('users:login')
 

def login(request):
    #처음 로그인 화면으로 들어올 때는 get방식이므로 핸들링
    if request.method == "GET":
        return render(request, 'Html/login.html' )

    #post방식을 받은 경우 로그인 유효성 인증 실시
    elif request.method == "POST":
        login_user_id=request.POST['id']
        login_user_pw=request.POST['password']

        try:
            user = User.objects.get(user_id=login_user_id)
        except User.DoesNotExist:
            user=None
            context = {
                'error' : '계정이 존재하지 않습니다.'
            }
            return render(request, 'Html/login.html', context)
        
        try :
            PasswordHasher().verify(user.user_pw.encode(), login_user_pw.encode())
        except exceptions.VerifyMismatchError:
            user=None  
            context = {
                'error' : '비밀번호가 일치하지 않습니다.'
            }
            return render(request, 'Html/login.html', context)
        
        if user != None:
            request.session['user'] = user.id
        
            # Redirect to a success page.
            return JsonResponse({'result':'success'})
            
        else:
            context = {
                'error' : '로그인에 실패하였습니다.'
            }
            return render(request, 'Html/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
def validEmail(request):
    register_id = request.POST.get('registerID')
    if duplicatedEmail(register_id):
        return JsonResponse({'data':False})
    return JsonResponse({'data':True})
    
def duplicatedEmail(email):
    if User.objects.filter(user_id=email).exists():
        return True
    return False