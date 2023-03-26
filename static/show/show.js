const $spreadsheet = document.querySelector('#spreadsheet1'); // 엑셀 보여주느 창
const $excel_var = document.querySelector('#excel_var'); // 엑셀 열 제목 hmtl에서 선택하는 창

let a;
const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
let newnum = 1; //spreadsheet와 jsonObject를 동적으로 생성하기 위한 number

window.onload = updateExcel(document.getElementById('jsonObject1').value, newnum);
console.time(); // 측정 시작

//excel개수는 유지하고 데이터만 변경하고 싶을 때 array는 넣을 데이터배열, num은 넣고싶은 엑셀순서
function updateExcel(data, num){
    console.time("updateExcel"); // 측정 시작
    let excel_col = []; // 엑셀 열 제목
    array=JSON.parse(data);
    // json 키값 저장
    for (let i = 0; i < Object.keys(array[0]).length; i++) {
        // select box 데이터 추가
        $excel_var.innerHTML += `<Option value= '${Object.keys(array[0])[i]}' id='select_column'>` + Object.keys(array[0])[i] + "</option>";
        // 엑셀 열 제목 추가 및 열 크기 지정
        excel_col[i] = ({ title: Object.keys(array[0])[i], width: '150px' }) // "저장시간":"202206071700" 에서 저장시간 부분
    }
    var spr_num='spreadsheet'+num;
    // excel 정보
    a=jspreadsheet(document.getElementById(spr_num), {
        data: array,
        tableOverflow: true,
        columns: excel_col,
    });
    console.timeEnd("updateExcel"); // 측정 종료
}



//우석추가
//새로운 데이터로 새로운 엑셀 만들고 싶을 때
function newExcel(data){
    console.time("newExcel"); // 측정 시작
    newnum = newnum+1;
    let obj = document.getElementById('excel');
    let jsonObjects = document.getElementById('jsonObjects');
    let newSpread = document.createElement("div");
    newSpread.setAttribute("id", "spreadsheet"+newnum);
    
    let newInput = document.createElement("input");
    newInput.setAttribute("id", "jsonObject"+newnum);
    newInput.setAttribute("type","hidden");

    obj.appendChild(newSpread);
    jsonObjects.appendChild(newInput);
    
    var json_num="#jsonObject"+ newnum;
    var json = $(json_num);
    data=JSON.stringify(data);
    json.val(data);//데이터는 문자열 형태
    updateExcel(data, newnum);//문자열을 배열형식으로 파싱한 후 excel생성
    console.timeEnd("newExcel"); // 측정 종료
}

const default_arr = ['주간_평균_', '주간_최소_', '주간_최대_', '주간_DIF_', '주간_GDD_',
    '야간_평균_', '야간_최소_', '야간_최대_', '야간_DIF_', '야간_GDD_',
    '일출전후t시간_평균_', '일출전후t시간_최소_', '일출전후t시간_최대_', '일출전후t시간_DIF_', '일출전후t시간_GDD_',
    '일출부터정오_평균_', '일출부터정오_최소_', '일출부터정오_최대_', '일출부터정오_DIF_', '일출부터정오_GDD_'];
let newDataArr = []; // 최종 selcet-final에 들어갈 때 값 중복 검사를 위한 배열
let newData = []; // 우리가 전송할 새로운 DATA


// 변수 쉬운 버전
const $default_select = document.querySelector('#default_select'); // 디폴트 값 select box
const $default_value = document.querySelector('#default_value'); // 디폴트 선택 값에 따른 변수 select box
const $final_var = document.querySelectorAll('#final_var'); // 마지막 select-box
// 디폴드 선택에 따른 default_value 창 변동
$default_select.addEventListener('click', (event) => {
    console.time("default_select"); // 측정 시작
    let text = event.target.textContent; // 클릭한 option의 글자
    for (let string of default_arr) { // string = '주간_평균_' 구조
        let inputValue = string.split('_'); // 주간, 평균
        if (CheckDuplicate(inputValue.join('') + text)) { // 주간평균온도 중복확인
            if (text.includes('온도') || text.includes('기온')) { // 모든 변수 다넣기
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
    if (dupl_arr.length) {
        alert(`${dupl_arr}은 중복 값이라 제거했습니다.`);
        dupl_arr = [];
    }
    console.timeEnd("default_select"); // 측정 종료
});



// 객체 추가함수, 배열에 객체의 key가 있으면 기존 value에 vlaue추가
// 없으면 key, value 둘다 추가
let nObj = {};
function add_Obj(text1, text2, text3) {
    console.time("add_Obj"); // 측정 시작
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
    console.timeEnd("add_Obj"); // 측정 종료
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

// 변수 어려운 버전
// $ex_var => 조건에 맞는 변수들은 $ex_var1에 추가 $ex_var2 $ex_var3와 결합하여 데이터 추가
let excel_arr = Object.keys(JSON.parse(document.getElementById('jsonObject1').value)[0]); // 전체 엑셀 열 이름
const $ex_var = document.querySelector('#ex_var');
const $ex_var1 = document.querySelector('#ex_var1');
const $ex_var2 = document.querySelector('#ex_var2');
const $ex_var3 = document.querySelector('#ex_var3');

// [ {text1 : [[text2, text3]] }]
let text1;
let text2;
let text3;

$ex_var.addEventListener(('click'), (event) => {
    console.time("ex_var"); // 측정 시작
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
    console.timeEnd("ex_var"); // 측정 종료
})

$ex_var1.addEventListener('click', (event) => {
    text1 = event.target.textContent;
    console.log(text1);
});
$ex_var2.addEventListener('click', (event) => {
    text2 = event.target.value;
    console.log(text2);
});
$ex_var3.addEventListener('click', (event) => {
    text3 = event.target.value;
    console.log(text3);
});


// 변수 삭제 및 이동(어려움 버전에서 만)
const $move = document.querySelector('#option_move'); // 변수 이동 버튼
const $optionDelete = document.querySelectorAll('#option_delete'); // 변수 삭제 버튼

$move.addEventListener('click', () => {
    console.time("move"); // 측정 시작
    if (text2 !== '전체') {
        let string = text2 + text3 + text1;
        if (CheckDuplicate(string.split('_').join(''))) {
            $final_var[0].innerHTML += `<Option value= '${string}'>` + string.split('_').join('') + `</option>`;
            $final_var[1].innerHTML += `<Option value= '${string}'>` + string.split('_').join('') + `</option>`;
            newDataArr.push(string.split('_').join(''));
            add_Obj(text1, text2, text3);
        }
    } else {
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
    }
    if (dupl_arr.length) {
        alert(`${dupl_arr}은 중복 값이라 제거했습니다.`);
        dupl_arr = [];
    }

    text2='';
    text3='';
    console.timeEnd("move"); // 측정 종료
})

// 삭제 함수
function varDelete() {
    console.time("varDelete"); // 측정 시작
    let checked = document.querySelectorAll('#final_var :checked');
    let selected = [...checked].map(option => option.value);

    if (selected) {
        for (let x of selected) {
            let inputValue = x.split('_');
            newDataArr.splice(newDataArr.indexOf(inputValue.join('')), 1); // 배열 제거
            $(`#final_var option[value=${x}]`).remove(); // check 한 값을 select-box에서 제거
            for (let i = 0; i < Object.keys(newData).length; i++) {
                if (Object.keys(newData[i])[0] === inputValue[2]) {
                    for (let j = 0; j < newData[i][inputValue[2]].length; j++) {
                        if (newData[i][inputValue[2]][j].includes(inputValue[0]) && newData[i][inputValue[2]][j].includes(inputValue[1])) {
                            newData[i][inputValue[2]].splice(i, 1); // 객체에서 제거
                        }
                    }
                    // pop이라 항상 마지막 값이 제거
                }
            }
        }
    } else {
        alert('삭제할 항목을 선택하세요');
    }
    console.timeEnd("varDelete"); // 측정 종료
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

//농업 전처리 클래스와 연결된 함수
$(function(){
    console.time("submit_data"); // 측정 시작
    $('#submit_data').click(function(){
    
    let file_name=$('#fileName').val();
    let file_type=$('#file_type').val();
    let date=$('#date').val();
    let periods=$('#periods').val();
    let data=$('#jsonObject1').val();
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