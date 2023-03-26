const $spreadsheet = document.querySelector('#spreadsheet'); // 엑셀 창
const $fileUploader = document.querySelector('#fileUploader'); // 엑셀 업로드 버튼
const $data_select = document.querySelector('#data_select'); // 엑셀 변수 목록
const $file_input = document.querySelector('#file_input'); // 엑셀 drag & drop 
const $file_icon = document.querySelector('#file_icon'); // 엑셀 icon 
const $jsonObject = document.querySelector('#jsonObject'); // json html 표시

let arr = null; // json 데이터
let excel_col = []; // 열 이름

// file selsect upload
window.addEventListener('DOMContentLoaded', function () {
    function readExcel(evt) {
        let selectedFile = evt.target.files[0];
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
                    //$jsonObject.innerHTML = JSON.stringify(XL_row_object);
                }
                // json 데이터 정보
                arr = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                excel_col = []; // 새로운 데이터를 불러오면 title을 초기화

                // json 키값 저장
                for (let i = 0; i < Object.keys(arr[1]).length; i++) {
                    // select box 데이터 추가
                    $data_select.innerHTML += "<Option value='select-column' id='select_column'>" + Object.keys(arr[0])[i] + "</option>";
                    // 엑셀 열 제목 추가 및 열 크기 지정
                    excel_col[i] = ({ title: Object.keys(arr[0])[i], width: '150px' }) // "저장시간":"202206071700" 에서 저장시간 부분
                }

                // excel 정보
                jspreadsheet(document.getElementById('spreadsheet'), {
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
    
    $fileUploader.addEventListener('change', readExcel);
});

// file drag upload
window.addEventListener('DOMContentLoaded', function () {
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
                    //$jsonObject.innerHTML = JSON.stringify(XL_row_object);
                }
                // json 데이터 정보
                arr = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                excel_col = []; // 새로운 데이터를 불러오면 title을 초기화

                // json 키값 저장
                for (let i = 0; i < Object.keys(arr[1]).length; i++) {
                    // select box 데이터 추가
                    $data_select.innerHTML += "<Option value='select-column' id='select_column'>" + Object.keys(arr[0])[i] + "</option>";
                    // 엑셀 열 제목 추가 및 열 크기 지정
                    excel_col[i] = ({ title: Object.keys(arr[0])[i], width: '150px' }) // "저장시간":"202206071700" 에서 저장시간 부분
                }

                // excel 정보
                jspreadsheet(document.getElementById('spreadsheet'), {
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
    $file_input.addEventListener('drop', drawExcel);
});

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
