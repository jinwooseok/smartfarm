const $checkAll = document.querySelector('#checkAll'); // 전체 선택 버튼
const $AllCheckBox = document.querySelectorAll('.check');

// 버튼
const $upload = document.querySelector('#upload'); // 등록버튼
const $delete = document.querySelector('#delete'); // 삭제버튼

const $AllTitle = document.querySelectorAll('#AllTitle');
const $listAll = document.querySelectorAll('.list');
const $search = document.querySelector('#search');


//토큰
const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken

// 전체 선택
function AllCheck() {
    if (this.checked) {
        for (let i = 0; i < $AllCheckBox.length; i++) {
            $AllCheckBox[i].checked = true;
        }
    } else {
        for (let i = 0; i < $AllCheckBox.length; i++) {
            $AllCheckBox[i].checked = false;
        }
    }
}

// 삭제
function select_delete() {
    let check_count = [...$AllCheckBox].filter((v) => v.checked === true).length; // 체크 수 확인

    if (!check_count) {
        alert('삭제할 파일을 선택하세요');
        return;
    }

    const yesOrNo = confirm('정말 삭제하나요?'); // 예, 아니요를 입력 받음

    if (yesOrNo) {
        let deleteList = [];
        for (let i = 0; i < $AllCheckBox.length; i++) {
            if ($AllCheckBox[i].checked) {
                deleteList.push($AllTitle[i].innerText);
                $AllCheckBox[i].parentElement.remove();
            }
        }
        $.ajax({
            url: 'delete/',
            type: 'post',
            dataType: 'json',
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                data: JSON.stringify(deleteList)
            },
            success: function (response) {
                if (response.data != null) {
                    location.href = "../";
                }
                else {
                }
            },
            error: function (xhr, error) {
                alert("에러입니다.");
                console.error("error : " + error);
            }
        })
        $checkAll.checked = false;
        AllCheck();
    } else {
        alert('삭제를 취소합니다.');
    }

}

// 선택 삭제
$delete.addEventListener('click', select_delete);

// 전체 선택
$checkAll.addEventListener('change', AllCheck);

// 검색용 저장
let titleList = [];
for (let x of $AllTitle) {
    titleList.push(x.innerText);
}

$search.addEventListener('keyup', (event) => {
    let text = event.target.value;
    for (let i = 0; i < titleList.length; i++) {
        if (!titleList[i].includes(text)) {
            $listAll[i].style.display = 'none';
        } else {
            $listAll[i].style.display = 'flex';
        }
    }
})

// 파일 클릭
function saveTitle(event) {
    localStorage.setItem("title_list", JSON.stringify(titleList)); // 로컬에 저장
    localStorage.setItem('fileTitle', JSON.stringify(event.target.innerHTML));
    window.location.href = `/revise/${event.target.innerHTML}/`;
}

// 다운로드 버튼
const $download = document.querySelector('#download')
$download.addEventListener('click', (event) => {
    let check_count = [...$AllCheckBox].filter((v) => v.checked === true).length;

    if (check_count !== 1) {
        alert('파일은 1개를 선택해야 합니다.')
        return;
    }

    let downloadTitle; // 파일 이름
    for (let i = 0; i < $AllCheckBox.length; i++) {
        if ($AllCheckBox[i].checked) {
            downloadTitle = $AllCheckBox[i].parentElement.childNodes[3].innerText;
        }
    }

    $.ajax({
        url: '/download/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            data: downloadTitle,
        },
        success: function (response) {
            if (response.data != null) {
                download(response.data, downloadTitle);
            }
        },
        error: function (xhr, error) {
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })

})

// download 로직, csv로
const download = function(data, title){
    const jsonData = data
    let jsonDataParsing = JSON.parse(jsonData);
    let toCsv = '';
    let row="";

    for(let i in jsonDataParsing[0]){
        row += i+","; // 열 입력
    }
    row = row.slice(0,-1);
    toCsv += row +"\r\n";

    for(let i=0; i<jsonDataParsing.length; i++){
        row="";
        for(let j in jsonDataParsing[i]){
            row += ""+jsonDataParsing[i][j] + ","; // 열 제외 입력
        }
        row.slice(0, row.length - 1);
        toCsv += row + '\r\n';
    }

    if(toCsv===''){
        alert("Invalid data");
        return;
    }

    let fileName = title; // 다운로드 파일 이름

    //Initialize file format you want csv or xls
    let uri = 'data:text/csv;charset=utf-8,\uFEFF' + encodeURI(toCsv);

    let link = document.createElement("a");    
    link.href = uri;
    link.style = "visibility:hidden";
    link.download = fileName;
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}