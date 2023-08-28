const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
// 그래프
const $add = document.querySelector('#add');
const $delete = document.querySelector('#delete');
const $selectBox = document.querySelector("#selectBox");
const $selectBox2 = document.querySelector("#selectBox2");
const $down = document.querySelector('#down');

// 분석
const $xValue = document.querySelector('#xValue');
const $selectedXValue = document.querySelector('#selectedXValue');
const $yValue = document.querySelector('#yValue');
const $x_move = document.querySelector('#x_move');
const $x_delete = document.querySelector('#x_delete');
const $analyze = document.querySelector('#analyze');
const $technique = document.querySelector('#technique');
const $analyze_result = document.querySelector('#analyze-result');

let data = JSON.parse(document.getElementById('jsonObject').value);
let dataColumn = Object.keys(data[0]);

window.onload = () => {
    for (let x of dataColumn) {
        // x=x.replace(' ','');
        $xValue.innerHTML += `<option value=${x}>${x}</option>`
        $yValue.innerHTML += `<option value=${x}>${x}</option>`
        $selectBox.innerHTML += `<option value=${x}>${x}</option>`
        $selectBox2.innerHTML += `<option value=${x}>${x}</option>`
    }

}

/////////////////////////////////////
// 분석
const xValueArr = []; // 선택한 x값 배열

// 선택한 x값 이동
$x_move.addEventListener('click', () => {
    let checked = document.querySelectorAll('#xValue :checked');
    let selected = [...checked].map(option => option.textContent);

    for (let x of selected) {
        $selectedXValue.innerHTML += `<option value=${x}>${x}</option>`;
        xValueArr.push(x);
    }
})

// x값 삭제
$x_delete.addEventListener('click', () => {
    let checked = document.querySelectorAll('#selectedXValue :checked');
    let selected = [...checked].map(option => option.textContent);

    for (let x of selected) {
        $(`#selectedXValue option[value='${x}']`).remove();
        xValueArr.splice(xValueArr.indexOf(x), 1);
    }
})

$analyze.addEventListener('click',() =>{
    $.ajax({
        url: `/analyze/${JSON.parse(localStorage.getItem("fileTitle"))}/stat`,
        type: 'get',
        dataType: 'json',
        data : {
            xValue : JSON.stringify(xValueArr), //x 값 배열임
            yValue : $yValue.options[$yValue.selectedIndex].textContent, //y 값
            technique : $technique.options[$technique.selectedIndex].textContent, // 분석 종류
        },
        success: function (response) {
            if (response.data != null) {
                $analyze_result.innerHTML=response.data; // 결과 창 html
            }
        },
        error: function (xhr, error) {
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })

})


/////////////////////////////////////
// 그래프 //
var chart; // 그래프
let graphArr = []; // 사용한 변수

// 특수 문자 및 공백 제거 정규 표현식
let reg = /[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/ ]/gim

// 그래프 보여주기
$add.addEventListener("click", () => {
    let arr = [];

    let xText = $selectBox.options[$selectBox.selectedIndex].value;
    let yText = $selectBox2.options[$selectBox2.selectedIndex].value;


    // 처음
    if (graphArr.length === 0) {
        arr.push(xText);
        // x축 값 넣기
        for (let i = 0; i < data.length; i++) {
            if (reg.test(data[i][xText])) {
                // arr.push(Number(data[i][xText].replace(reg, "")));
                arr.push(data[i][xText]);
            } else {
                arr.push(Number(data[i][xText]));
            }
        }
        graphArr.push(arr);
        arr = [];
        // y축
        arr.push(yText);
        for (let i = 0; i < data.length; i++) {
            arr.push(Number(data[i][yText]));
        }
        graphArr.push(arr);

        chart = bb.generate({
            bindto: "#chart",
            data: {
                x: xText,
                // x : "x축",
                type: "line",
                columns:
                    graphArr,
            },
            zoom: {
                enabled: true, // for ESM specify as: zoom()
                type: "drag"
            },
            axis: {
                x: {
                    type: "category",
                    tick: {
                        rotate: 75,
                        multiline: false,
                        tooltip: true
                    },
                    //height: 130
                }
            },
        });
        return;
    }

    if (graphArr.includes(yText)) {
        return;
    }

    // y축
    arr.push(yText);
    for (let i = 0; i < data.length; i++) {
        arr.push(Number(data[i][yText]));
    }
    graphArr.push(arr);

    chart.load({
        columns: graphArr,
    });

})

document.querySelector('#graphType').addEventListener('click', ()=>{

    let type = document.querySelector('#graphType').options[document.querySelector('#graphType').selectedIndex].value;
    console.log(type);
    console.log(graphArr);
    chart.load({
        type : type,
        columns: graphArr,
    })
})

$delete.addEventListener('click', () => {
    let yText = $selectBox2.options[$selectBox2.selectedIndex].value;
    chart.unload({
        ids: yText,
    });

    graphArr.splice(graphArr.indexOf(yText), 1);
    console.log(graphArr);
})

$down.addEventListener('click', () => {
    chart.export({
        // width: 800,
        // height: 600,
        // preserveAspectRatio: false,
        // preserveFontStyle: false,
        mimeType: "image/png"
    }, dataUrl => {
        const link = document.createElement("a");

        link.download = `${JSON.parse(localStorage.getItem("fileTitle"))}.png`;
        link.href = dataUrl;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
})