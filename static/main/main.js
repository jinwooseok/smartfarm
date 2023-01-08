function dis(){
    if($('.nav_bar').css('right') != '0px'){
        $('.nav_bar').animate({
            right : '0px'
        })
    }else{
        $('.nav_bar').animate({
            right : '-500px'
        })
    }
}


//로그인모달 url이동없이 검사하기 위함.
var csrftoken = $('[name=csrfmiddlewaretoken]').val();

$(function(){
    $('#login_submit').click(function(){
        var id = $('#user_id').val();
        var pw = $('#user_pw').val();
        $.ajax({
            url:'users/login/',
            type:'post',
            dataType:'json',
            headers: {'X-CSRFToken': csrftoken},
            data:{user_id:id, user_pw:pw},
            success:function(response){
                if (response.data == 'cor'){
                    form.action = '/';
                    form.method = "POST";
                    form.submit();
                    return 0;}
                else {
                    document.getElementById('login_error').setAttribute('style','display:block;');
                
            }},
            error : function(xhr, error){
                alert("에러입니다.");
                console.error("error : " + error);
            }
        })
    })
})
