const $merge = document.querySelector('#merge');

function move_manage(){
    location.href = "/manage";
}

$merge.addEventListener('click', move_manage);
