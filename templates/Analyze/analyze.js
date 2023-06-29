const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
// 그래프
const $show = document.querySelector('#show');
const $add = document.querySelector('#add');
const $delete = document.querySelector('#delete');
const $selectBox = document.querySelector("#selectBox");
const $selectBox2 = document.querySelector("#selectBox2");

// 분석
const $xValue = document.querySelector('#xValue');
const $selectedXValue = document.querySelector('#selectedXValue');
const $yValue = document.querySelector('#yValue');
const $x_move = document.querySelector('#x_move');
const $x_delete = document.querySelector('#x_delete');

// 테스트 데이터
let data = JSON.parse(document.getElementById('jsonObject').value);
let dataColumn = Object.keys(data[0]);
let graphArr = [];


window.onload = () =>{
    for (let x of dataColumn) {
        $xValue.innerHTML += `<option value=${x}>${x}</option>`
        $yValue.innerHTML += `<option value=${x}>${x}</option>`
        $selectBox.innerHTML += `<option value=${x}>${x}</option>`
        $selectBox2.innerHTML += `<option value=${x}>${x}</option>`
    }
    
}

/////////////////////////////////////
// 분석

const xValueArr=[]; // 선택한 x값 배열

// 선택한 x값 이동
$x_move.addEventListener('click', () =>{
    let checked = document.querySelectorAll('#xValue :checked');
    let selected = [...checked].map(option => option.value);

    for(let x of selected){
        $selectedXValue.innerHTML += `<option value=${x}>${x}</option>`;
        xValueArr.push(x);
    }
})

// x값 삭제
$x_delete.addEventListener('click', () =>{
    let checked = document.querySelectorAll('#selectedXValue :checked');
    let selected = [...checked].map(option => option.value);

    for(let x of selected){
        $(`#selectedXValue option[value='${x}']`).remove();
        xValueArr.splice(xValueArr.indexOf(x),1);
    }
})



/////////////////////////////////////
// 그래프

let text; // $manage_list_menu.options[$manage_list_menu.selectedIndex].value;
$selectBox.addEventListener('click', (event) => {
    text = event.target.options[event.target.selectedIndex].value;
})

var chart;

// 그래프 보여주기
$show.addEventListener("click", () => {
    let arr=[];
    arr.push(text)
    for (let i = 0; i < 6; i++) {
        arr.push(Number(data[i][text]));
    }
    graphArr.push(arr);
    graphArr.push(["x",1,2,3,4,5,6])
    chart = bb.generate({
        bindto: "#chart",
        data: {
            x: text,
            // x : "x축",
            type: "line",
            columns:
                graphArr,
        },
        zoom: {
            enabled: true, // for ESM specify as: zoom()
            type: "drag"
        },
    });

    chart.unload({
		ids: "x",
	});
    graphArr.pop();
})

$add.addEventListener('click', () => {
    let = sText = $selectBox2.options[$selectBox2.selectedIndex].value;
    let arr=[];
    arr.push(sText);
    for (let i = 0; i < 6; i++) {
        arr.push(Number(data[i][sText]));
    }
    graphArr.push(arr);
    chart.load({
		columns: graphArr,
	});
})

$delete.addEventListener('click', () => {
    let = sText = $selectBox2.options[$selectBox2.selectedIndex].value;
    chart.unload({
		ids: sText,
	});
})