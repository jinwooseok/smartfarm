const $list_container = document.querySelector('#list-container'); // 글 목록 div
const $check_all = document.querySelector('#check-all'); // 상단 체크박스

// 버튼
const $upload = document.querySelector('#upload'); // 등록버튼
const $merge = document.querySelector('#merge'); // 병합버튼
const $delete = document.querySelector('#delete'); // 삭제버튼

// 전체 선택
function AllCheck() {
    const All_Checkbox = document.querySelectorAll('.check'); // check-box
    if (this.checked) {
        for (let i = 0; i < All_Checkbox.length; i++) {
            All_Checkbox[i].checked = true;
        }
    } else {
        for (let i = 0; i < All_Checkbox.length; i++) {
            All_Checkbox[i].checked = false;
        }
    }
}

// 삭제
function select_delete() {
    const All_Checkbox = document.querySelectorAll('.check'); // check-box

    if(All_Checkbox.length===0){
        alert('삭제할 파일을 선택해주세요')
        return
    }

    const yesOrNo = confirm('정말 삭제하나요?'); // 예, 아니요를 입력 받음
    if (yesOrNo) {
        for (let i = 0; i < All_Checkbox.length; i++) {
            if (All_Checkbox[i].checked) {
                All_Checkbox[i].parentElement.remove();
            }
            // 삭제 후 순서 숫자 감소 ???
        }
        $.ajax({
            url:'delete/',
            type:'post',
            dataType:'json',
            headers: {'X-CSRFToken': csrftoken},
            data:{
                data:JSON.stringify(Titlelist)
            },
            success:function(response){
                if (response.data != null){
                    location.href = "../";
                }
                else {                  
            }},
            error : function(xhr, error){
                alert("에러입니다.");
                console.error("error : " + error);
            }
        })
    } else{
        alert('삭제를 취소합니다.');
    }
    
    document.querySelector('.check-all').checked = false;
    AllCheck();
}

// 선택 삭제
$delete.addEventListener('click', select_delete);

// 전체 선택
$check_all.addEventListener('change', AllCheck);


// 검색
const $titleAll = document.querySelectorAll('#list_title');
const $listAll = document.querySelectorAll('.list');
const $search = document.querySelector('#search');

let titleList = [];

for(let x of $titleAll){
    titleList.push(x.innerText);
}

$search.addEventListener('keyup', (event)=>{
    let text = event.target.value;
    for(let i=0; i<titleList.length; i++){
        if(!titleList[i].includes(text)){
            $listAll[i].style.display='none';
        } else{
            $listAll[i].style.display='flex';
        }
    }
})

$merge.addEventListener('click' , () =>{
    location.href = "/merge";
})

// title 내부 저장
localStorage.setItem("title_list", JSON.stringify(titleList));

