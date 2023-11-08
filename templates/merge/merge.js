import Excel from '../JS/excel_show.mjs';
import { Loading,CloseLoading } from '../JS/loading.mjs';

const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken

const $growth = document.querySelector('#growthSelectBox');
const $environment = document.querySelector('#environmentSelectBox');
const $output = document.querySelector('#outputSelectBox');
const $mergeFileName = document.querySelector('#mergeFileName');
const $merge = document.querySelector('#merge');
const $save = document.querySelector('#save');
const $growthVariable =document.querySelector('#growthVariable')
const $environmentVariable =document.querySelector('#environmentVariable')
const $outputVariable =document.querySelector('#outputVariable');
const $spreadsheet = document.querySelector('#spreadsheet'); // 엑셀 창

let mergeDataList=[];
let mergeCompleteData;;

// 선택한 파일 불러오기
const postFilename =(name)=>{
    let returnData;
    $.ajax({
        url: '../loaddata/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            fileName : name,
        },
        async:false,
        success: function (response) {
            if (response.data != null) {
                returnData = response.data;
            }
            else {
                alert('전송할 데이터가 없습니다.')
            }
        },
        error: function (xhr, error) {
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })

    return returnData;
}

// 파일 변수 불러오기
$growth.addEventListener('change', ()=>{
    $growthVariable.innerHTML='';
    const growthTitle = $growth.options[$growth.selectedIndex].textContent;
    let data = postFilename(growthTitle);
    mergeDataList[0]=data;
    let dataColumn= Object.keys(JSON.parse(data)[0]); 
    for (let x of dataColumn){
        $growthVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }

})

$environment.addEventListener('change', ()=>{
    $environmentVariable.innerHTML='';
    const environmentTitle = $environment.options[$environment.selectedIndex].textContent;
    let data =  postFilename(environmentTitle);
    mergeDataList[1]=data;
    let dataColumn= Object.keys(JSON.parse(data)[0]); 
    for (let x of dataColumn){
        $environmentVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
})

$output.addEventListener('change', ()=>{
    $outputVariable.innerHTML='';
    const outputTitle = $output.options[$output.selectedIndex].textContent;
    let data =  postFilename(outputTitle)
    mergeDataList[2]=data;
    let dataColumn= Object.keys(JSON.parse(data)[0]);
    for (let x of dataColumn){
        $outputVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
})

// 병합
$merge.addEventListener('click', async ()=>{
    const columnName=[];

    $spreadsheet.innerHTML = '';

    if($mergeFileName.value === ''){
        alert('파일 이름을 정해주세요');
        return;
    }

    let growthTitle = $growthVariable.options[$growthVariable.selectedIndex].value;
    let environmentTitle = $environmentVariable.options[$environmentVariable.selectedIndex].value;
    let outputTitle = $outputVariable.options[$outputVariable.selectedIndex].value;

    const titleList = [growthTitle,environmentTitle, outputTitle];

    for(let x of titleList){
        if (x==='null'){
            continue
        }
        columnName.push(x);
    }

    Loading();

    $.ajax({
        url: '../merge-view/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            header : 'merge',
            columnName : JSON.stringify(columnName),
            fileName: $mergeFileName.value,
            data : JSON.stringify(mergeDataList),
        },
        async:false,
        success:function(response){
            if(response.data != null){
                console.log( "return",JSON.parse(response.data));
                mergeCompleteData = new Excel(JSON.parse(response.data), $spreadsheet);
            }
        },
        error: function (xhr, error) {
            CloseLoading()
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })
    await CloseLoading();
    console.log("로딩창 닫기_2");
})

$save.addEventListener("click", () =>{
    console.log(mergeCompleteData.getData());
    Loading();
    $.ajax({
        url: '../merge-view/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            header : 'save',
            fileName: $mergeFileName.value,
            mergedData: mergeCompleteData.getData(),
        },
        success:function(response){
            if(response.data != null){
                console.log(response.data)
                CloseLoading()
            }
        },
        error: function (xhr, error) {
            alert("에러입니다.");
            CloseLoading();
            console.error("error : " + error);
        }
    })
})