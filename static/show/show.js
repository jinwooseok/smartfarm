const $spreadsheet = document.querySelector('#spreadsheet'); // 엑셀 보여주느 창
const $excel_var = document.querySelector('#excel_var'); // 엑셀 열 제목 hmtl에서 선택하는 창
let excel_data = JSON.parse(document.getElementById('jsonObject').value);
let excel_arr = Object.keys(excel_data[0]); // 전체 엑셀 열 이름

const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken

window.onload = function () {
    let excel_col = []; // 엑셀 열 제목

    // json 키값 저장
    for (let i = 0; i < Object.keys(excel_data[1]).length; i++) {
        // select box 데이터 추가
        $excel_var.innerHTML += `<Option value= '${Object.keys(excel_data[0])[i]}'>` + Object.keys(excel_data[0])[i] + "</option>";
        // 엑셀 열 제목 추가 및 열 크기 지정
        excel_col[i] = ({ title: Object.keys(excel_data[0])[i], width: '150px' }) // "저장시간":"202206071700" 에서 저장시간 부분
    }

    // excel 정보
    jspreadsheet($spreadsheet, {
        data: excel_data,
        tableOverflow: true,
        columns: excel_col,
        // onselection: selectionActive,
    },);
}
//excel개수는 유지하고 데이터만 변경하고 싶을 때 array는 넣을 데이터배열, num은 넣고싶은 엑셀순서
function updateExcel(data){
    console.time("updateExcel"); // 측정 시작
    let excel_col = []; // 엑셀 열 제목
    array=JSON.parse(data);
    // json 키값 저장
    for (let i = 0; i < Object.keys(array[1]).length; i++) {
        // select box 데이터 추가
        $excel_var.innerHTML += `<Option value= '${Object.keys(array[0])[i]}' id='select_column'>` + Object.keys(array[0])[i] + "</option>";
        // 엑셀 열 제목 추가 및 열 크기 지정
        excel_col[i] = ({ title: Object.keys(array[0])[i], width: '150px' }) // "저장시간":"202206071700" 에서 저장시간 부분
    }
    // excel 정보
    a=jspreadsheet($spreadsheet, {
        data: array,
        tableOverflow: true,
        columns: excel_col,
    });
    console.timeEnd("updateExcel"); // 측정 종료
}

///////////////////////////////////////////
// 엑셀 변수를 가지고 새로운 데이터로 변환 시 사용하는 함수 및 변수
const deflaut_arr = ['주간_평균_', '주간_최소_', '주간_최대_', '주간_DIF_', '주간_GDD_',
    '야간_평균_', '야간_최소_', '야간_최대_', '야간_DIF_', '야간_GDD_',
    '일출전후t시간_평균_', '일출전후t시간_최소_', '일출전후t시간_최대_', '일출전후t시간_DIF_', '일출전후t시간_GDD_',
    '일출부터정오_평균_', '일출부터정오_최소_', '일출부터정오_최대_', '일출부터정오_DIF_', '일출부터정오_GDD_'];
let newDataArr = []; // 최종 select-final에 들어갈 때 값 중복 검사를 위한 배열, "주간평균내부온도" 형식
let newData = []; // 우리가 전송할 새로운 DATA, [ {text1 : [[text2, text3]] }] 형식

// 객체 추가함수, 배열에 객체의 key가 있으면 기존 value에 vlaue추가
// 없으면 key, value 둘다 추가
let nObj = {}; // newData에 들어가 객체
function add_Obj(text1, text2, text3) {

    let obj_index = -1;
    for (let i in newData) {
        if (Object.keys(newData[i]).includes(text1)) {
            obj_index = i;
        }
    }

    if (obj_index > -1) {
        newData[obj_index][text1].push([text2, text3]);
    } else {
        nObj = new Object();
        nObj[text1] = [[text2, text3]]
        newData.push(nObj);
    }
}

// 배열 중복 검사
let dupl_arr = []; // 중복 배열
function CheckDuplicate(new_value) {
    for (let value of newDataArr) {
        if (new_value === value) {
            dupl_arr.push(new_value);
            return false;
        }
    }
    return true;
}

// 변수 쉬운 버전
const $default_select = document.querySelector('#default_select'); // 디폴트 값 select box
const $default_value = document.querySelector('#default_value'); // 디폴트 선택 값에 따른 변수 select box
const $final_var = document.querySelectorAll('#final_var'); // 마지막 select-box [0]은 쉬운 버전, [1]은 어려운 버전 박스

// 디폴드 선택에 따른 default_value 창 변동
$default_select.addEventListener('click', (event) => {
    let text = event.target.textContent; // 클릭한 option의 글자
    for (let string of deflaut_arr) { // string = '주간_평균_' 구조
        let inputValue = string.split('_'); // 주간, 평균
        if (CheckDuplicate(inputValue.join('') + text)) { // 주간평균온도 중복확인
            if (text.includes('온도')) { // 모든 변수 다넣기
                $final_var[0].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`;
                $final_var[1].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`;
                newDataArr.push(inputValue.join('') + text);
                add_Obj(text, inputValue[0], inputValue[1]);
            } else if (text.includes('습도') || text.includes('CO2') || text.includes('co2')) {
                if (inputValue[1] === 'DIF' || inputValue[1] === 'GDD' || inputValue[0] === '일출전후t시간') {
                    continue;
                } else {
                    $final_var[0].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`;
                    $final_var[1].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`; newDataArr.push(inputValue.join('') + text);
                    add_Obj(text, inputValue[0], inputValue[1]);
                }
            } else if (text.includes('일사량') || text.includes('강수량')) {
                alert("어떻게 넣어야 하는지 잘 모르겠다.");
            }
        }
    }
    if (dupl_arr.length) {
        alert(`${dupl_arr}은 중복 값이라 제거했습니다.`);
        dupl_arr = [];
    }
});



// 변수 어려운 버전
// $ex_var => 조건에 맞는 변수들은 $ex_var1에 추가 $ex_var2 $ex_var3와 결합하여 데이터 추가
const $ex_var = document.querySelector('#ex_var');
const $ex_var1 = document.querySelector('#ex_var1');
const $ex_var2 = document.querySelector('#ex_var2');
const $ex_var3 = document.querySelector('#ex_var3');

// [ {text1 : [[text2, text3]] }]
let text1;
let text2;
let text3;

$ex_var.addEventListener(('click'), (event) => {
    $ex_var1.innerHTML = '';
    let text = event.target.textContent;
    for (let i of excel_arr) {
        if (text === '온도') {
            if (i.includes(text) || i.includes("기온")) {
                $ex_var1.innerHTML += `<Option value= '${i}'>` + i + "</option>";
            }
        } else if (text === 'CO2' || text === 'co2') {
            if (i.includes(text)) {
                $ex_var1.innerHTML += `<Option value= '${i}'>` + i + "</option>";
            }
        } else if (i.includes(text)) {
            $ex_var1.innerHTML += `<Option value= '${i}'>` + i + "</option>";
        }
    }
})

$ex_var1.addEventListener('click', (event) => {
    text1 = event.target.textContent;
});
$ex_var2.addEventListener('click', (event) => {
    text2 = event.target.value;
});
$ex_var3.addEventListener('click', (event) => {
    text3 = event.target.value;
});



// 변수 삭제 및 이동(어려움 버전에서 만)
const $move = document.querySelector('#option_move'); // 변수 이동 버튼
const $optionDelete = document.querySelectorAll('#option_delete'); // 변수 삭제 버튼

$move.addEventListener('click', () => {
    // 2,3번 박스만 선택
    if (text1 && text2) {
        // text2가 전체면 defualt 값을 불러옴
        if (text2 === '전체') {
            let text = text1;
            for (let string of deflaut_arr) { // string = '주간_평균_' 구조
                let inputValue = string.split('_'); // 주간, 평균
                if (CheckDuplicate(inputValue.join('') + text)) { // 주간평균온도 중복확인
                    if (text.includes('온도')) { // 모든 변수 다넣기
                        $final_var[0].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`;
                        $final_var[1].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`;
                        newDataArr.push(inputValue.join('') + text);
                        add_Obj(text, inputValue[0], inputValue[1]);
                    } else if (text.includes('습도') || text.includes('CO2') || text.includes('co2')) {
                        if (inputValue[1] === 'DIF' || inputValue[1] === 'GDD' || inputValue[0] === '일출전후t시간') {
                            continue;
                        } else {
                            $final_var[0].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`;
                            $final_var[1].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`; newDataArr.push(inputValue.join('') + text);
                            add_Obj(text, inputValue[0], inputValue[1]);
                        }
                    } else if (text.includes('일사량') || text.includes('강수량')) {
                        console.log("어떻게 넣어야 하는지 잘 모르겠다.")
                    }
                }
            }
        } else if (text2 !== '전체' && text3) { //text2가 default값이 아니고 text3가 있다면
            let string = text2 + text3 + text1;
            if (CheckDuplicate(string.split('_').join(''))) {
                $final_var[0].innerHTML += `<Option value= '${string}'>` + string.split('_').join('') + `</option>`;
                $final_var[1].innerHTML += `<Option value= '${string}'>` + string.split('_').join('') + `</option>`;
                newDataArr.push(string.split('_').join(''));
                text2=text2.replace('_','');
                text3=text3.replace('_','');
                add_Obj(text1, text2, text3);
            }
        } else { // text3 미설정
            alert('4번 박스를 선택해 주세요.')
        }
        // text2,3 초기화
        text2 = '';
        text3 = '';

    } else {
        if (!text1) {
            alert('2번 박스에서 값을 선택해 주세요.')
        } else if (!text2) {
            alert('3번 박스에서 값을 선택해 주세요.')
        }
    }

    if (dupl_arr.length) {
        alert(`${dupl_arr}은 중복 값이라 제거했습니다.`);
        dupl_arr = [];
    }

})

// 삭제 함수
function varDelete() {
    let checked = document.querySelectorAll('#final_var :checked');
    let selected = [...checked].map(option => option.value);

    if (selected) {
        for (let x of selected) {
            let inputValue = x.split('_');
            console.log(inputValue);
            for (let i = 0; i < Object.keys(newData).length; i++) {
                if (Object.keys(newData[i])[0] === inputValue[2]) {
                    for (let j = 0; j < newData[i][inputValue[2]].length; j++) {
                        console.log(newData[i][inputValue[2]][j].includes(inputValue[0]));
                        console.log(newData[i][inputValue[2]][j].includes(inputValue[1]));
                        if (newData[i][inputValue[2]][j].includes(inputValue[0]) && newData[i][inputValue[2]][j].includes(inputValue[1])) {
                            console.log("complete");
                            newDataArr.splice(newDataArr.indexOf(inputValue.join('')), 1); // 배열 제거
                            $(`#final_var option[value='${x}']`).remove(); // check 한 값을 select-box에서 제거
                            newData[i][inputValue[2]].splice(j, 1); // 객체에서 제거
                            break;
                        }
                    }
                    if(newData[i][inputValue[2]].length === 0){
                        delete newData[i][inputValue[2]];
                    }
                }
            }
        }
    } else {
        alert('삭제할 항목을 선택하세요');
    }
}



// 변수 삭제
$optionDelete[0].addEventListener(('click'), varDelete);
$optionDelete[1].addEventListener(('click'), varDelete);


//////////////////////
// 날짜 및 이름 등 기타 정보 입력 변수 및 함수
const $columnDate = document.querySelector('#columnDate'); // 날짜 열 input
const $periods = document.querySelector('#periods'); // 주기선택, 기타면 값을 직접입력 할 수 있게
const $reset_data = document.querySelector('#reset_data'); // reset
const $fileName = document.querySelector("#fileName"); // 저장할 파일 이름
const $submit_data = document.querySelector('#submit_data');


$periods.addEventListener('change', (event) => {
    if (event.target.value === 'else') {
        document.querySelector('#else_peri').disabled = false;
    } else {
        document.querySelector('#else_peri').disabled = true;
    }

})

$submit_data.addEventListener('click', () => {
    console.log(newDataArr);
    console.log('-----------------');
    console.log(newData);
})

// 초기화
$reset_data.addEventListener('click', () => {
    newData = [];
    newDataArr = [];
    $final_var.innerHTML = '';
    $fileName.value = '';
})

/////////////////////////////
/////////// tap 2 ///////////
/////////////////////////////

let col_name;  // 선택한 열 이름
let x_axis = []; // x축
let datasets = []; // 선택한 데이터
let draw_data = []; // chart 그려주는 데이터

const $close = document.querySelector('#close'); // dialog 닫기
const dialog = document.querySelector('dialog'); // 팝업창
const $point = document.querySelector('#point');

let chart;

function xxx(event) {
    event.preventDefault();
    col_name = event.target.textContent;
    for (let i = 0; i < excel_data.length; i++) {
        x_axis.push(Object.values(excel_data[i])[0]); // 0대신 날짜 데이터 열을 넣어야함
        datasets.push(excel_data[i][col_name]);
    }

    let RGB_1 = Math.floor(Math.random() * (255 + 1));
    let RGB_2 = Math.floor(Math.random() * (255 + 1));
    let RGB_3 = Math.floor(Math.random() * (255 + 1));

    draw_data = [{
        label: col_name, // 데이터의 제목
        borderColor: 'rgba(' + RGB_1 + ',' + RGB_2 + ',' + RGB_3 + ',0.3)', // 색상
        data: datasets, // 데이터
        pointStyle: false,
    }]
    const labels = x_axis;

    // 데이터
    const data = {
        labels: labels,
        datasets: draw_data,
    };

    // 설정 값
    const config = {
        type: 'line', // 그래프 종류
        data: data, // 데이터
        options: {
            elements: { // 그래프 pointer 작게 만들어줌
                point: {
                    borderWidth: 0,
                    radius: 1,
                    backgroundColor: 'rgba(0,0,0,0)'
                }
            },
            responsive: true, // false=그래프 크기를 css를 이용 지정 가능
            diplay: 'true',
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    },
                    display: true,
                    // type: 'logarithmic',
                }],
                xAxes: [{
                    barThickness: 10,
                    gridLines: {
                        display: false
                    },
                    offset: true
                }],
            }
        }
    }
    dialog.showModal();

    chart = new Chart(document.getElementById('myChart'), config);
};


$close.addEventListener('click', () => {
    x_axis = [];
    datasets = [];
    document.querySelector("#myChart").innerHTML = "";
    dialog.close();
})



//농업 전처리 클래스와 연결된 함수
$(function(){
    console.time("submit_data"); // 측정 시작
    $('#submit_data').click(function(){
    
    let file_name=$('#fileName').val();
    let file_type=$('#file_type').val();
    let date=$('#date').val();
    let periods=$('#periods').val();
    let data=$('#jsonObject').val();
    let valueObject=JSON.stringify(newData);
    if (periods == 'else'){
        periods = document.getElementById('else_peri').value;
    }
    $.ajax({
        url:'farm/',
        type:'post',
        dataType:'json',
        headers: {'X-CSRFToken': csrftoken},
        data:{
            file_name:file_name,
            file_type:file_type,
            date:date,
            DorW:periods,
            data:data,
            valueObject:valueObject,
        },
        success:function(response){
            if (response.data != null){
                // a.setHeader([정수], [문자열]);
                console.log(response.data);
                location.href = "../";
                // $('#spreadsheet1').empty();
                // updateExcel(response.data,newnum);
                console.timeEnd("submit_data"); // 측정 종료
            }
            else {                  
        }},
        error : function(xhr, error){
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })
})
})

//다운로드
document.querySelector('#excel_down').onclick = () => {
    const data = excel_data; // data 목록
    const jsonData = JSON.stringify(data);
    let arrData = JSON.parse(jsonData);
    let CSV = '';
    
    let row = "";
    for (let index in arrData[0]) {
        row += index + ','; // 열 이름 입력
    }
    row = row.slice(0, -1);
    CSV += row + '\r\n';
    
    for (let i = 0; i < arrData.length; i++) {
      let row = "";
      for (let index in arrData[i]) {
          row += '"' + arrData[i][index] + '",'; // 데이터 입력
      }

      row.slice(0, row.length - 1);
      CSV += row + '\r\n';
    }

    if (CSV == '') {        
        alert("Invalid data");
        return;
    }

    let fileName = "MyReport_";
    fileName += "IVR채널".replace(/ /g,"_");// 파일 제목 
    
    //Initialize file format you want csv or xls
    let uri = 'data:text/csv;charset=utf-8,\uFEFF' + encodeURI(CSV);

    let link = document.createElement("a");    
    link.href = uri;
    link.style = "visibility:hidden";
    link.download = fileName + ".csv";
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


//파일 이름 끌고 오기
let Title=JSON.parse(localStorage.getItem("title_list"));
let $manage_list_menu = document.querySelector('#manage_list_menu');
for(let x of Title){
    $manage_list_menu.innerHTML += `<Option value= '${x}'>`+x+`</option>`;
}


//엑셀 바꾸기
$(function(){
    console.time("change_data"); // 측정 시작
    $('#manage_list_menu').on('change', function() {
        let file_name = $(this).val();
        console.log(file_name);
    $.ajax({
        url:'loaddata/',
        type:'post',
        dataType:'json',
        headers: {'X-CSRFToken': csrftoken},
        data:{
            file_name:file_name,
        },
        success:function(response){
            if (response.data != null){
                var json = $("jsonObject");
                json.val(response.data);
                console.log(response.data);
                $('#spreadsheet').empty();
                updateExcel(response.data);
                $('#list-body').empty();
                summaryCreater(response.summarys);
                console.timeEnd("change_data"); // 측정 종료
            }
            else {                  
        }},
        error : function(xhr, error){
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })
})
})

function summaryCreater(data){
    var list_body = document.getElementById('list-body');
    for (var key in data) {
        var value = data[key];
        var div = document.createElement('div');
        div.className = 'list';
        var col_name_div = document.createElement('div');
        col_name_div.className = 'col_name';
        var a = document.createElement('a');
        a.href = '#';
        a.className = 'draw_col';
        a.innerHTML = key;
        a.onclick = function(event) {
          xxx(event);
        }
        col_name_div.appendChild(a);
        div.appendChild(col_name_div);
        for (var sub_key in value) {
          var sub_value = value[sub_key];
          var sub_div = document.createElement('div');
          sub_div.className = sub_key;
          sub_div.innerHTML = sub_value;
          div.appendChild(sub_div);
        }
        list_body.appendChild(div);
    }
}