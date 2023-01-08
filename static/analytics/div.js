function grim_ud (){
    if ( $('.grim').css('height') === '500px'){
        $('.grim').css({
            height : '30px'
        })
        $('#up').css('display','none');
        $('#down').css('display','block');
        $('#myChart').css('display','none');
    } else if ( $('.grim').css('height') === '30px'){
        $('.grim').css({
            height : '500px'
        })
        $('#down').css('display','none');
        $('#up').css('display','block');
        $('#myChart').css('display','block');
    }
}

