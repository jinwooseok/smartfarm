// Excel class 불러오기
// import {Excel} from '../js/excel_show.mjs'; 

// excel
const $spreadsheet = document.querySelector('#spreadsheet'); // 엑셀 창
const $file_input = document.querySelector('#file_input'); // 파일 선택 
const $file_drag = document.querySelector('#file_drag'); // 파일 drag 
const $file_icon = document.querySelector('#file_icon'); // 엑셀 icon 
const $file_name = document.querySelector('#file_name'); // 파일 이름
const $excel_down = document.querySelector('#excel_down'); // 파일 다운

let data = '';

class Excel {
    constructor(data, box) { // 데이터와 div를 생성할 때 매개변수로
        this.excelData = data; // 데이터
        this.makeCol(this.excelData); // 열 데이터 만들기
        this.box = box; // 그려줄 div 선택
        this.box.innerHTML = ''; // 이전 데이터 excel 초기화

        // excel 그리기
        jspreadsheet(this.box, {
            data: this.excelData,
            columns: this.excelColumn,
            tableOverflow: true,
        })
    }

    // 열 생성
    makeCol(data) {
        this.excelColumn = [];
        for (let i in Object.keys(data[0])) {
            this.excelColumn[i] = ({ title: Object.keys(data[0])[i], width: '150px' })
        }
    }

    // download
    download(data) {
        const jsonData = JSON.stringify(data);
        let jsonDataParsing = JSON.parse(jsonData);
        let toCsv = '';
        let row = "";

        for (let i in jsonDataParsing[0]) {
            row += i + ","; // 열 입력
        }
        row = row.slice(0, -1);
        toCsv += row + "\r\n";

        for (let i = 0; i < jsonDataParsing.length; i++) {
            row = "";
            for (let j in jsonDataParsing[i]) {
                row += "" + jsonDataParsing[i][j] + ","; // 열 제외 입력
            }
            row.slice(0, row.length - 1);
            toCsv += row + '\r\n';
        }

        if (toCsv === '') {
            alert("Invalid data");
            return;
        }

        let fileName = `${this.fileName}_수정`; // 다운로드 파일 이름

        //Initialize file format you want csv or xls
        let uri = 'data:text/csv;charset=utf-8,\uFEFF' + encodeURI(toCsv);

        let link = document.createElement("a");
        link.href = uri;
        link.style = "visibility:hidden";
        link.download = fileName + ".csv";

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    // data 참조
    getData() {
        return this.excelData;
    }

    // ().setFileName(name); -> 다운로드할 때 파일 이름 설정
    setFileName(name) {
        this.fileName = name;
    }

}

$file_input.addEventListener('change', (event) => {
    // 파일 읽기
    let selectedFile = event.target.files[0];
    let reader = new FileReader();

    $file_icon.style.display = 'none'; // 파일 이미지 숨김
    $file_drag.style.display = 'none'; // 파일 input 숨김
    $file_name.value = selectedFile.name;

    reader.onload = function (evt) { // excel to Json
        let resultData = evt.target.result; // reader.result

        //바이너리 형태로 엑셀파일을 읽는다.
        let workbook = XLSX.read(resultData, { type: 'binary' });
        //엑셀파일의 시트 정보를 읽어서 JSON 형태로 변환한다. sheet 하나만 가져옴
        let ex_data = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[workbook.SheetNames[0]]);

        data = new Excel(ex_data, $spreadsheet);
        // data를 로컬 저장
        localStorage.setItem("data", JSON.stringify(data.excelData));

        $excel_down.disabled = false;
    }

    reader.onerror = function (event) { //  읽기 동작에 에러가 생길 때마다 발생합니다.
        console.error("File could not be read! Code " + event.target.error.code);
    };

    reader.readAsBinaryString(selectedFile); // 이걸 읽고 onload 실행?
});

// drag in 확인
$file_drag.addEventListener('dragenter', function (e) {
    e.preventDefault();
    this.style.backgroundColor = '#999';
});

// drag out 확인
$file_drag.addEventListener('dragleave', function (e) {
    e.preventDefault();
    this.style.backgroundColor = '';
});

// drag로 파일 올리기
$file_drag.addEventListener('drop', (event) => {
    // 파일 읽기
    let selectedFile = event.dataTransfer.files[0];
    let reader = new FileReader();

    $file_icon.style.display = 'none'; // 파일 이미지 숨김
    $file_drag.style.display = 'none'; // 파일 input 숨김
    $spreadsheet.style.backgroundColor = '';
    $file_name.value = selectedFile.name;

    reader.onload = function (evt) { // excel to Json
        let resultData = evt.target.result; // reader.result

        //바이너리 형태로 엑셀파일을 읽는다.
        let workbook = XLSX.read(resultData, { type: 'binary' });
        //엑셀파일의 시트 정보를 읽어서 JSON 형태로 변환한다. sheet 하나만 가져옴
        let ex_data = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[workbook.SheetNames[0]]);

        data = new Excel(ex_data, $spreadsheet);
        // data를 로컬 저장
        localStorage.setItem("data", JSON.stringify(data.excelData));

        // data = data.getData();
        $excel_down.disabled = false;

    }

    reader.onerror = function (event) { //  읽기 동작에 에러가 생길 때마다 발생합니다.
        console.error("File could not be read! Code " + event.target.error.code);
    };

    reader.readAsBinaryString(selectedFile); // 이걸 읽고 onload 실행?
});

// downToCSV //////////////////////////////////////////////////
$excel_down.addEventListener('click', () => {
    console.log(data);
    console.log(data.getData())
    // data.download(data.getData());
});

