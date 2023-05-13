import {Excel} from '/templates/excel_show.mjs'

const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
// upload를 통해 저장된 파일 이름을 불러옴
let Title = JSON.parse(localStorage.getItem("title_list"));
let $manage_list_menu = document.querySelector('#manage_list_menu');
for (let x of Title) {
    $manage_list_menu.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
}

//////////////////////////////////////////////
// test data
let excel_data = JSON.parse(document.getElementById('jsonObject').value);
//////////////////////////////////////////////

const $spreadsheet = document.querySelector('#spreadsheet'); // 엑셀 창
const $excel_down = document.querySelector('#excel_down'); // 파일 다운

//////////////////
// 초기 설정 -> 데이터 불러오고 그리기
//////////////////
let data;
let excel_arr;

window.onload = () =>{
    data = new Excel(excel_data, $spreadsheet);
    excel_arr = Object.keys(data.getData()[0]);
    for(let x of excel_arr){
        $excel_var.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
}

// downToCSV //////////////////////////////////////////////////
$excel_down.addEventListener('click', ()=>{
    data.download(newData);
});

///////////////////////////////////////////
// 엑셀 변수를 가지고 새로운 데이터로 변환 시 사용하는 함수 및 변수
const defaultVar = ['주간_평균_', '주간_최소_', '주간_최대_', '주간_DIF_', '주간_GDD_',
    '야간_평균_', '야간_최소_', '야간_최대_', '야간_DIF_', '야간_GDD_',
    '일출전후t시간_평균_', '일출전후t시간_최소_', '일출전후t시간_최대_', '일출전후t시간_DIF_', '일출전후t시간_GDD_',
    '일출부터정오_평균_', '일출부터정오_최소_', '일출부터정오_최대_', '일출부터정오_DIF_', '일출부터정오_GDD_'];
let newDataArr = []; // 최종 select-final에 들어갈 때 값 중복 검사를 위한 배열, "주간평균내부온도" 형식
let newData = []; // 우리가 전송할 새로운 DATA, [ {text1 : [[text2, text3]] }] 형식

// 객체 추가함수, 배열에 객체의 key가 있으면 기존 value에 value추가
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
const $excel_var = document.querySelector('#excel_var'); // 모든 열 추가
const $default_select = document.querySelector('#default_select'); // 디폴트 값 select box
const $default_value = document.querySelector('#default_value'); // 디폴트 선택 값에 따른 변수 select box
const $final_var = document.querySelectorAll('#final_var'); // 마지막 select-box [0]은 쉬운 버전, [1]은 어려운 버전 박스

let excel_var_text='';
$excel_var.addEventListener('click', (event) => {
    excel_var_text = event.target.textContent;
})

// 디폴드 선택에 따른 default_value 창 변동
$default_select.addEventListener('click', (event) => {

    if(!excel_var_text){
        alert('값을 선택해주세요');
        return true;
    }

    let text = event.target.textContent; // 클릭한 option의 글자

    for (let string of defaultVar) { // string = '주간_평균_' 구조
        let inputValue = string.split('_'); // 주간, 평균
        if (CheckDuplicate(inputValue.join('') + excel_var_text)) { // 주간평균(변수명) 중복확인
            if (text.includes('온도')) { // 모든 변수 다넣기
                $final_var[0].innerHTML += `<Option value= '${string}${excel_var_text}'>` + inputValue.join('') + excel_var_text + `</option>`;
                $final_var[1].innerHTML += `<Option value= '${string}${excel_var_text}'>` + inputValue.join('') + excel_var_text + `</option>`;
                newDataArr.push(inputValue.join('') + excel_var_text);
                add_Obj(excel_var_text, inputValue[0], inputValue[1]);
            } else if (text.includes('습도') || text.includes('CO2') || text.includes('co2')) {
                if (inputValue[1] === 'DIF' || inputValue[1] === 'GDD' || inputValue[0] === '일출전후t시간') {
                    continue;
                } else {
                    $final_var[0].innerHTML += `<Option value= '${string}${excel_var_text}'>` + inputValue.join('') + excel_var_text + `</option>`;
                    $final_var[1].innerHTML += `<Option value= '${string}${excel_var_text}'>` + inputValue.join('') + excel_var_text + `</option>`;
                    newDataArr.push(inputValue.join('') + excel_var_text);
                    add_Obj(excel_var_text, inputValue[0], inputValue[1]);
                }
            } else if (text.includes('일사량') || text.includes('강수량')) {
                alert("어떻게 넣어야 하는지 잘 모르겠다.");
                break;
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
let ex_var1_text;
let ex_var2_text;
let ex_var3_text;

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
    ex_var1_text = event.target.textContent;
});
$ex_var2.addEventListener('click', (event) => {
    ex_var2_text = event.target.value;
});
$ex_var3.addEventListener('click', (event) => {
    ex_var3_text = event.target.value;
});

// 변수 삭제 및 이동(어려움 버전에서 만)
const $move = document.querySelector('#option_move'); // 변수 이동 버튼
const $optionDelete = document.querySelectorAll('#option_delete'); // 변수 삭제 버튼

$move.addEventListener('click', () => {
    // 2,3번 박스만 선택
    if (ex_var1_text && ex_var2_text) {
        // text2가 전체면 default 값을 불러옴
        if (ex_var2_text === '전체') {
            let text = ex_var1_text;
            for (let string of defaultVar) { // string = '주간_평균_' 구조
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
                            $final_var[1].innerHTML += `<Option value= '${string}${text}'>` + inputValue.join('') + text + `</option>`;
                            newDataArr.push(inputValue.join('') + text);
                            add_Obj(text, inputValue[0], inputValue[1]);
                        }
                    } else if (text.includes('일사량') || text.includes('강수량')) {
                        console.log("어떻게 넣어야 하는지 잘 모르겠다.")
                    }
                }
            }
        } else if (ex_var2_text !== '전체' && ex_var3_text) { //text2가 default값이 아니고 text3가 있다면
            let string = ex_var2_text + ex_var3_text + ex_var1_text;
            console.log(string);
            if (CheckDuplicate(string.split('_').join(''))) {
                $final_var[0].innerHTML += `<Option value= '${string}'>` + string.split('_').join('') + `</option>`;
                $final_var[1].innerHTML += `<Option value= '${string}'>` + string.split('_').join('') + `</option>`;
                newDataArr.push(string.split('_').join(''));
                ex_var2_text = text2.replace('_', '');
                ex_var3_text = text3.replace('_', '');
                add_Obj(ex_var1_text, ex_var2_text, ex_var3_text);
            }
        } else { // text3 미설정
            alert('4번 박스를 선택해 주세요.')
        }
        // text2,3 초기화
        ex_var2_text = '';
        ex_var3_text = '';

    } else {
        if (!ex_var1_text) {
            alert('2번 박스에서 값을 선택해 주세요.')
        } else if (!ex_var2_text) {
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
                        if (newData[i][inputValue[2]][j].includes(inputValue[0]) && newData[i][inputValue[2]][j].includes(inputValue[1])) {
                            newDataArr.splice(newDataArr.indexOf(inputValue.join('')), 1); // 배열 제거
                            $(`#final_var option[value='${x}']`).remove(); // check 한 값을 select-box에서 제거
                            newData[i][inputValue[2]].splice(j, 1); // 객체에서 제거
                            break;
                        }
                    }
                    if (newData[i][inputValue[2]].length === 0) {
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
$optionDelete[0].addEventListener('click', varDelete);
$optionDelete[1].addEventListener('click', varDelete);

//////////////////////
// 날짜 및 이름 등 기타 정보 입력 변수 및 함수
const $columnDate = document.querySelector('#columnDate'); // 날짜 열 input
const $periods = document.querySelector('#periods'); // 주기선택, 기타면 값을 직접입력 할 수 있게
const $reset_data = document.querySelector('#reset_data'); // reset
const $fileName = document.querySelector("#fileName"); // 저장할 파일 이름
const $submit_data = document.querySelector('#submit_data');

// 주기 선택 === 기타 true면 직접 입력 가능하게
$periods.addEventListener('change', (event) => {
    if (event.target.value === 'else') {
        document.querySelector('#else_peri').disabled = false;
    } else {
        document.querySelector('#else_peri').disabled = true;
    }

})

// data 최종 확인
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


//우석추가
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
        url:'/farm/',
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
