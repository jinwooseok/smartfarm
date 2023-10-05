import Excel from '../JS/excel_show.mjs';

const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
let columnName = [];

const localTitleList = JSON.parse(localStorage.getItem("title_list"));
const $growth = document.querySelector('#growthSelectBox');
const $environment = document.querySelector('#environmentSelectBox');
const $output = document.querySelector('#outputSelectBox');
const $mergeFileName = document.querySelector('#mergeFileName');
const $merge = document.querySelector('#merge');
const $growthVariable =document.querySelector('#growthVariable')
const $environmentVariable =document.querySelector('#environmentVariable')
const $outputVariable =document.querySelector('#outputVariable')

let mergeDataList=[];

// select 박스 내용 추가함수
const selectOptionAdd = ()=>{
    for (let x of localTitleList){
        $growth.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
        $environment.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
        $output.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
}
selectOptionAdd();

// 파일 리스트 불러오기



// 선택한 파일 불러오기
const postFilename = async(name)=>{
    let returnData;
    await $.ajax({
        url: '../loaddata/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            fileName : name,
        },
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
$growth.addEventListener('change', async()=>{
    const growthTitle = $growth.options[$growth.selectedIndex].value;
    let data = await postFilename(growthTitle);
    mergeDataList[0]=data;
    let dataColumn= Object.keys(JSON.parse(data)[0]); 
    for (let x of dataColumn){
        $growthVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }

})

$environment.addEventListener('change', async()=>{
    const environmentTitle = $environment.options[$environment.selectedIndex].value;
    let data = await postFilename(environmentTitle);
    mergeDataList[1]=data;
    let dataColumn= Object.keys(JSON.parse(data)[0]); 
    for (let x of dataColumn){
        $environmentVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
})

$output.addEventListener('change', async()=>{
    const outputTitle = $output.options[$output.selectedIndex].value;
    let data = await postFilename(outputTitle)
    mergeDataList[2]=data;
    let dataColumn= Object.keys(JSON.parse(data)[0]);
    for (let x of dataColumn){
        $outputVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
})

// 병합
$merge.addEventListener('click',()=>{
    columnName=[];

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

    console.log(columnName)
    console.log(JSON.stringify(mergeDataList));

    $.ajax({
        url: '../merge-view/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            header : 'merge',
            columnName : columnName,
            fileName: $mergeFileName.value,
            data : JSON.stringify(mergeDataList),
        },
        success:function(response){
            if(response.data != null){
                console.log(response.data)
            }
        },
        error: function (xhr, error) {
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })
})
