
$(document).ready(function () {
    $("#fileUploader").change(function (evt) {
        var selectedFile = evt.target.files[0];
        var reader = new FileReader();
        reader.onload = function (event) {
            var data = event.target.result;
            var workbook = XLSX.read(data, {
                type: 'binary'
            });
            workbook.SheetNames.forEach(function (sheetName) {
                var XL_row_object = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                if (XL_row_object.length > 0) {
                    document.getElementById("jsonObject").innerHTML = JSON.stringify(XL_row_object);
                }
                // json 데이터 정보
                let arr = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[sheetName]);
                let excel_col=[]; // 새로운 데이터를 불러오면 title을 초기화
                
                // json 키값 저장
                for (let i = 0; i < Object.keys(arr[1]).length; i++) {
                    // select box 데이터 추가
                    data_select.innerHTML += "<Option value='select-column' id='select_column'>" + Object.keys(arr[0])[i] + "</option>";
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
        //           
        reader.readAsBinaryString(selectedFile);
    });

    document.getElementById('download').onclick = function () {
        x.download(); // 파일 이름 설정?
    }
    
});

// 각종 엑셀 열, 행 관련 함수
var changed = function (instance, cell, x, y, value) {
    var cellName = jexcel.getColumnNameFromId([x, y]);
    $('#log').append('New change on cell ' + cellName + ' to: ' + value + '');
}

var beforeChange = function (instance, cell, x, y, value) {
    var cellName = jexcel.getColumnNameFromId([x, y]);
    $('#log').append('The cell ' + cellName + ' will be changed');
}

var insertedRow = function (instance) {
    $('#log').append('Row added');
}

var insertedColumn = function (instance) {
    $('#log').append('Column added');
}

var deletedRow = function (instance) {
    $('#log').append('Row deleted');
}

var deletedColumn = function (instance) {
    $('#log').append('Column deleted');
}

var sort = function (instance, cellNum, order) {
    var order = (order) ? 'desc' : 'asc';
    $('#log').append('The column  ' + cellNum + ' sorted by ' + order + '');
}

var resizeColumn = function (instance, cell, width) {
    $('#log').append('The column  ' + cell + ' resized to width ' + width + ' px');
}

var resizeRow = function (instance, cell, height) {
    $('#log').append('The row  ' + cell + ' resized to height ' + height + ' px');
}

var selectionActive = function (instance, x1, y1, x2, y2, origin) {
    var cellName1 = jexcel.getColumnNameFromId([x1, y1]);
    var cellName2 = jexcel.getColumnNameFromId([x2, y2]);
    $('#log').append('The selection from ' + cellName1 + ' to ' + cellName2 + '');
}

var loaded = function (instance) {
    $('#log').append('New data is loaded');
}

var moveRow = function (instance, from, to) {
    $('#log').append('The row ' + from + ' was move to the position of ' + to + ' ');
}

var moveColumn = function (instance, from, to) {
    $('#log').append('The col ' + from + ' was move to the position of ' + to + ' ');
}

var blur = function (instance) {
    $('#log').append('The table ' + $(instance).prop('id') + ' is blur');
}

var focus = function (instance) {
    $('#log').append('The table ' + $(instance).prop('id') + ' is focus');
}

var paste = function (data) {
    $('#log').append('Paste on the table ' + $(instance).prop('id') + '');
}