///////////////////////////////
// 변수 //
///////////////////////////////

const $list_container = document.querySelector('#list-container'); // 글 목록 div
const $check_all = document.querySelector('#check-all'); // 상단 체크박스

// 버튼
const $upload = document.querySelector('#upload'); // 등록버튼
const $merge = document.querySelector('#merge'); // 병합버튼
const $delete = document.querySelector('#delete'); // 삭제버튼

// 팝업
const $dialog = document.querySelector('dialog'); // 팝업창
const $upload_title = document.querySelector('#upload_title'); // 글 제목 설정
const $confirm = document.querySelector('#confirm'); // 확인
const $cancel = document.querySelector('#cancel'); // 취소

// 글 번호 변수
let order = 0;

// excel
const $spreadsheet = document.querySelector('#spreadsheet'); // 엑셀 창
const $file_input = document.querySelector('#file_input'); // 엑셀 drag & drop 
const $file_icon = document.querySelector('#file_icon'); // 엑셀 icon 
const $jsonObject = document.querySelector('#jsonObject'); // json html 표시
let arr = null; // json 데이터
let excel_col = []; // 열 이름

var csrftoken = $('[name=csrfmiddlewaretoken]').val();
///////////////////////////////
// 함수 //
///////////////////////////////

// 글 추가
function createList() {

    // 팝업 닫기
    $dialog.close();

    // 성공
    alert('파일이 등록되었습니다.');

    //return list;
}

// file drag upload
function drawExcel(evt) {
    let selectedFile = evt.dataTransfer.files[0];
    let reader = new FileReader();

    $file_icon.style.display = 'none'; // 파일 이미지 숨김
    $file_input.style.display = 'none'; // 파일 input 숨김
    $spreadsheet.style.backgroundColor = '';

    reader.onload = function (event) {
        let data = event.target.result;
        let workbook = XLSX.read(data, {
            type: 'binary'
        });

        workbook.SheetNames.forEach(function (sheetName) {
            let XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
            if (XL_row_object.length > 0) {
                $jsonObject.value = JSON.stringify(XL_row_object);
                console.log($jsonObject.value);
            }
            // json 데이터 정보
            arr = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
            excel_col = []; // 새로운 데이터를 불러오면 title을 초기화

            // json 키값 저장
            for (let i = 0; i < Object.keys(arr[1]).length; i++) {
                // 엑셀 열 제목 추가 및 열 크기 지정
                excel_col[i] = ({ title: Object.keys(arr[0])[i], width: '150px' }) // "저장시간":"202206071700" 에서 저장시간 부분
            }

            // excel 정보
            jspreadsheet($spreadsheet, {
                data: arr,
                tableOverflow: true,
                columns: excel_col,
            });

        })
    };
    reader.onerror = function (event) {
        console.error("File could not be read! Code " + event.target.error.code);
    };
    reader.readAsBinaryString(selectedFile);
}

// 삭제
function select_delete() {
    const All_Checkbox = document.querySelectorAll('.check'); // check-box
    const titles = document.querySelectorAll('.title');
    var Titlelist = new Array();
    let remove_num = 0;
    const yesOrNo = confirm('정말 삭제하나요?'); // 예, 아니요를 입력 받음
    if(yesOrNo){
        for (let i = 0; i < All_Checkbox.length; i++) {
            if (All_Checkbox[i].checked) {
                Titlelist.push(titles[i+1].innerText);
                remove_num++;
                All_Checkbox[i].parentElement.remove();
            }
            // 삭제 후 순서 숫자 감소 ???
        }
        console.log(Titlelist);
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
    }
    document.querySelector('.check-all').checked=false;
    Allcheck();
}

// 전체 선택
function Allcheck() {
    const All_Checkbox = document.querySelectorAll('.check'); // check-box
    if(this.checked){
        for (let i = 0; i < All_Checkbox.length; i++) {
            All_Checkbox[i].checked=true;
        }
    } else {
        for (let i = 0; i < All_Checkbox.length; i++) {
            All_Checkbox[i].checked=false;
        }
    }
}

///////////////////////////////
// 이벤트 리스너 //
///////////////////////////////

// excel drag로 불러오기
$file_input.addEventListener('drop', drawExcel);

// drag in 확인
$file_input.addEventListener('dragenter', function (e) {
    e.preventDefault();
    this.style.backgroundColor = '#999';
});

// drag out 확인
$file_input.addEventListener('dragleave', function (e) {
    e.preventDefault();
    this.style.backgroundColor = '';
});

// 글 추가
$confirm.addEventListener('click', createList);

// 팝업 보여주기
$upload.addEventListener('click', (event) => {
    event.preventDefault();
    $dialog.showModal();
})

// 팝업 취소
$cancel.addEventListener('click', (event) => {
    event.preventDefault();
    $dialog.close();
})

// 선택 삭제
$delete.addEventListener('click', select_delete);

// 전체 선택
$check_all.addEventListener('change', Allcheck);

let xx=document.querySelectorAll('.title>a');
let title_list = []
for(let x of xx){
    title_list.push(x.textContent);
    console.log(x.textContent);
}
localStorage.setItem("title_list", JSON.stringify(title_list));