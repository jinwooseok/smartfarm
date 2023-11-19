// Excel class 불러오기
import  Excel  from '../JS/excel_show.mjs';

const $spreadsheet = document.querySelector('#spreadsheet')
const $fileUploadDrag = document.querySelector('#fileUploadDrag'); // 파일 drag 
const $fileUploadInput = document.querySelector('#fileUploadInput'); // 파일 선택 
const $fileIcon = document.querySelector('#fileIcon'); // 엑셀 icon 
const $fileName = document.querySelector('#fileName'); // 파일 이름

const $upload = document.querySelector('#upload'); // dialog 닫기(확인)

let selectedFile; // 선택 파일 정보

$fileUploadInput.addEventListener('change', (event) => {
    // 파일 읽기
    selectedFile = event.target.files[0];
    if(!selectedFile){
        return;
    }
    $spreadsheet.innerHTML = "";
    // 파일 보여주기
    showFile();
});

// drag in 확인
$fileUploadDrag.addEventListener('dragenter', function (e) {
    e.preventDefault();
    this.style.backgroundColor = '#999';
});

// drag out 확인
$fileUploadDrag.addEventListener('dragleave', function (e) {
    e.preventDefault();
    this.style.backgroundColor = '';
});

// drag로 파일 올리기
$fileUploadDrag.addEventListener('drop', (event) => {
    event.preventDefault();
    // 파일 읽기
    selectedFile = event.dataTransfer.files[0];
    // 파일 보여주기
    showFile();
});

// 파일 그려주기
function showFile() {

    $fileIcon.style.display = 'none'; // 파일 이미지 숨김
    $fileUpload_Drag.style.display = 'none'; // 파일 input 숨김
    $spreadsheet.style['align-items'] = 'start';
    $fileName.value = selectedFile.name.replace(/\s/g, '_');
    let reader = new FileReader();

    reader.onload = function (evt) { // excel to Json
        let resultData = evt.target.result; // reader.result

        //바이너리 형태로 엑셀파일을 읽는다.
        let workbook = XLSX.read(resultData, { type: 'binary' });
        let ex_data = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[workbook.SheetNames[0]]);
        // 100줄을 미리 보여줌
        const uploadData = new Excel(ex_data.slice(0,100), $spreadsheet);
    }

    reader.onerror = function (event) { //  읽기 동작에 에러가 생길 때마다 발생합니다.
        console.error("File could not be read! Code " + event.target.error.code);
    };

    reader.readAsBinaryString(selectedFile); // 이걸 읽고 onload 실행?
}

///////////// 값 초기화 하기
$upload.addEventListener('click', () => {
    $spreadsheet.textContent = "";
    $fileIcon.style.display = 'block'; // 파일 이미지 보여줌
    $fileUpload_Drag.style.display = 'block'; // 파일 input 보여줌
})