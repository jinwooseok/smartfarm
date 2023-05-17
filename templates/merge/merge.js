import {Excel} from '/templates/JS/excel_show.mjs';
const $spreadsheet1 = document.querySelector('#spreadsheet');
const $spreadsheet2 = document.querySelector('#spreadsheet2');
const $spreadsheet3 = document.querySelector('#spreadsheet3');
const $var1 = document.querySelector('#var1');
const $var2 = document.querySelector('#var2');
let dataSet=JSON.parse(localStorage.getItem('mergeData'));
console.log(dataSet);
let excel_data = JSON.parse(dataSet[0]);
let excel_data2 = JSON.parse(dataSet[1]);

let data1 = new Excel(excel_data, $spreadsheet1);
let data2 = new Excel(excel_data2, $spreadsheet2);

const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
// Object.keys(data1.getData()[0])[i]
function makeSelectBox() {
    for(let x of Object.keys(data1.getData()[0])){
        $var1.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
    for(let x of Object.keys(data2.getData()[0])){
        $var2.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
}

makeSelectBox(); // selectedBox 데이터 추가

const $merge_button =document.querySelector('#merge_button');
const $download = document.querySelector('#download');
const $save = document.querySelector('#save');
let newData;
let var1_text=$var1.childNodes[1].textContent;
let var2_text=$var2.childNodes[1].textContent;
let isData = false; // 새로운 데이터가 만들어지면 download 버튼 클릭 가능

$var1.addEventListener('click', (event) =>{
    var1_text = event.target.value;
})
$var2.addEventListener('click', (event) =>{
    var2_text = event.target.value
})


function mergeData(data1, data2, column){
    let merge=[];

    if(data1.length !== data2.length){
        alert(`data1=${data1.length}, data2=${data2.length}로 행 수가 다릅니다.`);
        return;
    }

    for(let i in data2){
        delete data2[i][column];
        let obj = {...data1[i], ...data2[i]};
        merge.push(obj);
    }
    
    return merge;
}

$merge_button.addEventListener('click', () => {
    alert(`${var1_text}과 ${var2_text}를 기준으로 병합합니다.`)
    isData=true;

    if(isData){
        newData = new Excel(mergeData(data1.getData(), data2.getData(), var2_text), $spreadsheet3);
        $download.disabled = false;
        $save.disabled = false;
        
    }
})

$download.addEventListener('click', ()=>{
    newData.setFileName($('#fileName').val());
    setTimeout(()=>{
        newData.download(newData.getData());
    }, 500)
}, {once : true})

$save.addEventListener('click', ()=>{
    $.ajax({
        url:'/mergeView/',
        type:'post',
        dataType:'json',
        headers: { 'X-CSRFToken': csrftoken },
        data:{
            data : JSON.stringify(newData.getData()),
            file_name : $('#fileName').val(),
        }
    })
})