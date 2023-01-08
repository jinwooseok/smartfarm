const arr_y = []; // y축
const arr_x = []; // x축 
let draw_data = []; // chart 데이터
let selected_column; // select 태그에서 선택한 열 이름
let array;
const $x_axis = document.querySelector('#x-axis');


//dropdown에서 열 선택
function Select() {
    array = document.getElementById("jsonObject").value;
    // 선택된 열
    selected_column = $("#data_select option:selected").text()

    // arr이 문자열이라 json으로
    arr = JSON.parse(array);
    
}

// x축 지정
$x_axis.addEventListener('click',()=>{
    let i=0;
    for (i = 0; i < arr.length; i++) {
        if (Object.keys(arr[0])[i] === selected_column) {
            break;
        }
    }
    // label을 가져옴 
    for (let j = 0; j < arr.length; j++) {
        arr_x[j] = (Object.values(arr[j])[i]); // x
    }
});

// 그래프 삭제
document.querySelector('#delete').addEventListener('click',()=>{

    draw_data.forEach((v,i)=>{
        if(draw_data[i]['label'] === selected_column){
            draw_data.splice(i,1);
        }
    });

    draw_chart();
});

// 그래프 추가 == y축
document.querySelector('#add').onclick = function () {
    // 그래프 색상
    let RGB_1 = Math.floor(Math.random() * (255 + 1));
    let RGB_2 = Math.floor(Math.random() * (255 + 1));
    let RGB_3 = Math.floor(Math.random() * (255 + 1));

    draw_data.push({
        label: selected_column, // 데이터의 제목
        borderColor: 'rgba(' + RGB_1 + ',' + RGB_2 + ',' + RGB_3 + ',0.3)', // 색상
        data: arr.map(arr_y => arr_y[selected_column]), // 데이터
    },)
    console.log(draw_data);
    draw_chart();
}

// 그래프 초기화
document.querySelector('#clear').addEventListener('click',() =>{
    // 배열을 초기화 후 그리기
    arr_x.splice(0);
    draw_data.splice(0);

    const labels = arr_x;

    const data = {
        labels: labels,
        datasets: draw_data,
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: false,
            diplay: 'auto',
            scales: {
                xAxes: [{
                    barThickness: 10,
                    gridLines: {
                        display: false
                    },
                    offset: true
                }],
            }
        }
    };
    const myChart = new Chart(document.getElementById('myChart'), config);
});

// 그래프 그리기
const draw_chart = ()=> {

    // x축 변수들
    const labels = arr_x;

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
            responsive: false, // false=그래프 크기를 css를 이용 지정 가능
            diplay: 'auto',
            scales: {
                xAxes: [{
                    barThickness: 10,
                    gridLines: {
                        display: false
                    },
                    offset: true
                }],
            }
        }
    };
    // 그리기
    const myChart = new Chart(document.getElementById('myChart'), config);
};
