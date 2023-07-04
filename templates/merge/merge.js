import { Excel } from '/templates/JS/excel_show.mjs';
const $spreadsheet1 = document.querySelector('#spreadsheet');
const $spreadsheet2 = document.querySelector('#spreadsheet2');
const $spreadsheet3 = document.querySelector('#spreadsheet3');
const $var1 = document.querySelector('#var1');
const $var2 = document.querySelector('#var2');
const $fileName = document.querySelector('#fileName')

const $mergeData = JSON.parse(localStorage.getItem('mergeData'));

const excel_data = JSON.parse($mergeData[0]);
const excel_data2 = JSON.parse($mergeData[1]);

const data1 = new Excel(excel_data, $spreadsheet1);
const data2 = new Excel(excel_data2, $spreadsheet2);

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
            data: JSON.stringify($mergeData),
            var1: var1_text,
            var2: var2_text,
            file_name: $('#fileName').val(),
        },
        success:function(response){
            if(response.data != null){
                newData = new Excel(JSON.parse(response.data), $spreadsheet3)
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