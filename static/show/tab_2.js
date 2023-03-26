// 기존 엑셀에서 빈칸 처리 방법 선택 js
// 열 클릭하면 그래프 그려줌
let data2 = JSON.parse(document.getElementById('jsonObject').value);
let col_name;  // 선택한 열 이름
let x_axis = []; // x축
let datasets = []; // 선택한 데이터
let draw_data = []; // chart 그려주는 데이터

let chart;

const $close = document.querySelector('#close'); // dialog 닫기
const $dialog = document.querySelector('dialog'); // 팝업창


function xxx(event) {
    event.preventDefault();
    col_name = event.target.textContent;
    for (let i = 0; i < data2.length; i++) {
        x_axis.push(Object.values(data2[i])[0]); // 0대신 날짜 데이터 열을 넣어야함
        datasets.push(data2[i][col_name]);
    }

    let RGB_1 = Math.floor(Math.random() * (255 + 1));
    let RGB_2 = Math.floor(Math.random() * (255 + 1));
    let RGB_3 = Math.floor(Math.random() * (255 + 1));

    draw_data=[{
        label: col_name, // 데이터의 제목
        borderColor: 'rgba(' + RGB_1 + ',' + RGB_2 + ',' + RGB_3 + ',0.3)', // 색상
        data: datasets, // 데이터
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
            responsive: false, // false=그래프 크기를 css를 이용 지정 가능
            diplay: 'true',
            maintainAspectRatio: true,
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
    $dialog.showModal();
    chart = new Chart(document.getElementById('myChart'), config);
};


$close.addEventListener('click', () => {
    x_axis = [];
    datasets = [];
    $dialog.close();
})
