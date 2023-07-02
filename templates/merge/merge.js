import { Excel } from '/templates/JS/excel_show.mjs';
const $spreadsheet1 = document.querySelector('#spreadsheet');
const $spreadsheet2 = document.querySelector('#spreadsheet2');
const $spreadsheet3 = document.querySelector('#spreadsheet3');
const $var1 = document.querySelector('#var1');
const $var2 = document.querySelector('#var2');
const $fileName = document.querySelector('#fileName')

let dataSet = JSON.parse(localStorage.getItem('mergeData'));

let excel_data = JSON.parse(dataSet[0]);
let excel_data2 = JSON.parse(dataSet[1]);

let data1 = new Excel(excel_data, $spreadsheet1);
let data2 = new Excel(excel_data2, $spreadsheet2);

const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
// Object.keys(data1.getData()[0])[i]
function makeSelectBox() {
    for (let x of Object.keys(data1.getData()[0])) {
        $var1.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
    for (let x of Object.keys(data2.getData()[0])) {
        $var2.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
}

makeSelectBox(); // selectedBox 데이터 추가

const $merge_button = document.querySelector('#merge_button');
const $save = document.querySelector('#save');
let newData;
let var1_text = $var1.childNodes[1].textContent;
let var2_text = $var2.childNodes[1].textContent;
let isData = false; // 새로운 데이터가 만들어지면 download 버튼 클릭 가능

$var1.addEventListener('click', (event) => {
    var1_text = event.target.value;
})
$var2.addEventListener('click', (event) => {
    var2_text = event.target.value
})

function mergeData(data1, data2) {
    let merge = [];

    if (data1.length !== data2.length) {
        alert(`data1=${data1.length}, data2=${data2.length}로 행 수가 다릅니다.`);
        return;
    }

    // 특수문자제거
    let regExp = /[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/ ]/gi;

    for(let i in data2){
        if(data1[i][var1_text].replace(regExp,'') === data2[i][var2_text].replace(regExp,'')){
            delete data2[i][column];
            let obj = {...data1[i], ...data2[i]};
            merge.push(obj);
        } else {
            alert(`${i + 1}번 열의 값이 ${data1[i][var1_text]}, ${data2[i][var2_text]}로 다릅니다.`);
            return;
        }
    }

    return merge;
}

$merge_button.addEventListener('click', () => {

    if (!$fileName.value) {
        alert('파일 제목을 입력하세요')
        return;
    }

    alert(`${var1_text}과 ${var2_text}를 기준으로 병합합니다.`)
    $.ajax({
        url: '/mergeView/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            header: "merge",
            data: JSON.stringify(dataSet),
            var1: var1_text,
            var2: var2_text,
            file_name: $('#fileName').val(),
        },
        success:function(response){
            if(response.data != null){
                newData = new Excel(JSON.parse(response.data), $spreadsheet3)
                document.querySelector('#download').disabled = false;
                document.querySelector('#save').disabled = false;
            }
        },
        error: function (xhr, error) {
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })
})

$save.addEventListener('click', () => {
    $.ajax({
        url: '/mergeView/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            header: "save",
            data: JSON.stringify(newData.getData()),
            file_name: $('#fileName').val(),
        },
        success:function(response){
            if(response.data != null){
                alert(`${$('#fileName').val()}이 저장되었습니다.`);
            }
            window.location.href = "/fileList/";
        },
    })
    
})