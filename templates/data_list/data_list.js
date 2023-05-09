const $list_container = document.querySelector('#list-container'); // 글 목록 div
const $check_all = document.querySelector('#check-all'); // 상단 체크박스

// 버튼
const $upload = document.querySelector('#upload'); // 등록버튼
const $merge = document.querySelector('#merge'); // 병합버튼
const $delete = document.querySelector('#delete'); // 삭제버튼

// 전체 선택
function Allcheck() {
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

    const yesOrNo = confirm('정말 삭제하나요?'); // 예, 아니요를 입력 받음
    if (yesOrNo) {
        for (let i = 0; i < All_Checkbox.length; i++) {
            if (All_Checkbox[i].checked) {
                All_Checkbox[i].parentElement.remove();
            }
            // 삭제 후 순서 숫자 감소 ???
        }
    }
    
    document.querySelector('.check-all').checked = false;
    Allcheck();
}

// 선택 삭제
$delete.addEventListener('click', select_delete);

// 전체 선택
$check_all.addEventListener('change', Allcheck);


// 검색
const $titleAll = document.querySelectorAll('#list_title');
const $listAll = document.querySelectorAll('.list');
const $search = document.querySelector('#search');

let titleList = [];

for(let x of $titleAll){
    titleList.push(x.innerText);
}

$search.addEventListener('keyup', (evnet)=>{
    let text = evnet.target.value;
    for(let i=0; i<titleList.length; i++){
        if(!titleList[i].includes(text)){
            $listAll[i+1].style.display='none';
        } else{
            $listAll[i+1].style.display='flex';
        }
    }
})

// title 내부 저장
localStorage.setItem("title_list", JSON.stringify(titleList));

