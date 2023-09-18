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
let selectArr = []; // 업데이트용 y열 이름만 보관 ["열 이름","열 이름", "열 이름", ..]

// 특수 문자 및 공백 제거 정규 표현식
let reg = /[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/ ]/gim

const $buttonContainer = document.querySelector("#buttonContainer");
const $dateSelect = document.querySelector("#dateSelect");

let exCount = 30;
let startIndex = 0;
let lastIndex = exCount;


// 그래프 보여주기
$add.addEventListener("click", () => {
    let xText = $selectBox.options[$selectBox.selectedIndex].value;
    let yText = $selectBox2.options[$selectBox2.selectedIndex].value;

    // 날짜 열 생성
    for(let i=0; i<data.length; i++){
        $dateSelect.innerHTML += `<option value=${data[i][xText]}>${data[i][xText]}</option>`;
    }
     // x축 선택 필수
    if (xText === "notSelect") {
        alert("날짜를 선택하세요");
        return;
    }
    let arr = []; // 데이터 배열
    // ["열 이름", data...]
    
    // 맨 처음 그림 -> 그냥 다 넣는다.
    if(graphArr.length === 0){
        $buttonContainer.style.display = "flex"; // 화살표 생성
        // x값 설정
        arr.push(xText);
        selectArr.push(xText);
        for (let i = startIndex; i < lastIndex; i++) {
            if (reg.test(data[i][xText])) {
                arr.push(Number(data[i][xText].replace(reg, "")));
            } else {
                arr.push(Number(data[i][xText]));
            }
        }
        graphArr.push(arr);
        arr = [];
         //y값
        arr.push(yText);
        selectArr.push(yText);
        for (let i = startIndex; i < lastIndex; i++) {
            arr.push(Number(data[i][yText]));
        }
        graphArr.push(arr);
        chart = bb.generate({
            bindto: "#chart",
            data: {
                x: xText,
                // x : "x축",
                type: "line",
                columns: graphArr,
            },
            zoom: {
                enabled: true, // for ESM specify as: zoom()
                type: "drag",
            },
            axis: {
                x: {
                    type: "category",
                    tick: {
                    rotate: 75,
                    multiline: false,
                    tooltip: true,
                },
                //height: 130
            },
            },
        });
     } else{ // 데이터 추가
        if(selectArr.includes(yText)){
            return;
        }
        arr.push(yText);
        selectArr.push(yText);
        for (let i = startIndex; i < lastIndex; i++) {
        arr.push(Number(data[i][yText]));
        }
        graphArr.push(arr);
        chart.load({
            columns: graphArr,
        });
    }
})

document.querySelector('#graphType').addEventListener('click', ()=>{

    let type = document.querySelector('#graphType').options[document.querySelector('#graphType').selectedIndex].value;
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
    selectArr.splice(selectArr.indexOf(yText), 1);
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


const $Prev = document.querySelector("#Prev");
const $Next = document.querySelector("#Next");

const updateChart = (startIndex,lastIndex)=>{
    graphArr=[]; // 초기화

    let arr=[];
    arr.push(selectArr[0]);
    for (let i = startIndex; i < lastIndex; i++) {
        if (reg.test(data[i][selectArr[0]])) {
            arr.push(Number(data[i][selectArr[0]].replace(reg, "")));
        } else {
            arr.push(Number(data[i][selectArr[0]]));
        }
    }
    graphArr.push(arr);
    arr = [];


    selectArr.map((value, index) => {
        if(index!==0){
            arr.push(value);
            for (let i = startIndex; i < lastIndex; i++) {
                arr.push(Number(data[i][value]));
            }
            graphArr.push(arr);
            arr=[];
        }
    })
    chart.load({
        columns: graphArr,
    });
}

$Next.addEventListener("click", () => {
  startIndex = startIndex + exCount;
  lastIndex = startIndex + exCount > data.length ? data.length : startIndex + exCount;
  
  updateChart(startIndex,lastIndex);

  $Prev.style.visibility = "inherit";
  if (lastIndex === data.length) {
    $Next.style.visibility = "hidden";
  }
});

$Prev.addEventListener("click", () => {
  startIndex = startIndex - exCount <= 0 ? 0 : startIndex - exCount;
  lastIndex = lastIndex - exCount <= exCount ? exCount : lastIndex - exCount;

  updateChart(startIndex,lastIndex);

  $Next.style.visibility = "inherit";
  if (startIndex === 0) {
    $Prev.style.visibility = "hidden";
  }
});

$dateSelect.addEventListener('click', ()=>{
  startIndex = $dateSelect.options[$dateSelect.selectedIndex].index;
  lastIndex = startIndex + exCount > data.length ? data.length : startIndex + exCount;
  updateChart(startIndex,lastIndex);
})