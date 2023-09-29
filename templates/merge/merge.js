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

// select 박스 내용 추가함수
const selectOptionAdd = ()=>{
    for (let x of localTitleList){
        $growth.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
        $environment.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
        $output.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
}
selectOptionAdd();

const postFilename = (name)=>{
    $.ajax({
        url: '../loaddata/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            fileName : name,
        },
        success: function (response) {
            if (response.data != null) {
                console.log(response.data);
                return(response.data);
            }
            else {
                alert('전송할 데이터가 없습니다.')
            }

        },
        error: function (xhr, error) {
            console.log(growthTitle)
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })
}


$growth.addEventListener('change', ()=>{
    const growthTitle = $growth.options[$growth.selectedIndex].value;
    let data = postFilename(growthTitle);
    console.log(data);
    // let dataColumn = Object.keys(data[0]);
    // for (let x of dataColumn){
    //     $growthVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    // }

})

$environment.addEventListener('change', ()=>{
    const environmentTitle = $growth.options[$growth.selectedIndex].value;
    let data =postFilename(environmentTitle);
    console.log(data);
    // let dataColumn = Object.keys(data[0]);
    // for (let x of dataColumn){
    //     $environmentVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    // }
})

$output.addEventListener('change', ()=>{
    const outputTitle = $growth.options[$growth.selectedIndex].value;
    let data =postFilename(outputTitle)
    console.log(data);
    // let dataColumn = Object.keys(data[0]);
    // for (let x of dataColumn){
    //     $outputVariable.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    // }
})

// select 박스 선택 결과 함수
// columnName에 추가
$merge.addEventListener('click',()=>{
    columnName=[];

    if($mergeFileName.value === ''){
        alert('파일 이름을 정해주세요');
        return;
    }

    let growthTitle = $growth.options[$growth.selectedIndex].value;
    let environmentTitle = $environment.options[$environment.selectedIndex].value;
    let outputTitle = $output.options[$output.selectedIndex].value;

    const titleList = [growthTitle,environmentTitle, outputTitle];

    for(let x of titleList){
        if (x==='null'){
            continue
        }
        columnName.push(x);
    }

    console.log(columnName)

    // $.ajax({
    //     url: '../mergeView/',
    //     type: 'post',
    //     dataType: 'json',
    //     headers: { 'X-CSRFToken': csrftoken },
    //     data: {
    //         columnName : columnName,
    //         file_name: $mergeFileName.value,
    //     },
    //     success:function(response){
    //         if(response.data != null){
    //             console.log(response.data)
    //         }
    //     },
    //     error: function (xhr, error) {
    //         alert("에러입니다.");
    //         console.error("error : " + error);
    //     }
    // })
})
