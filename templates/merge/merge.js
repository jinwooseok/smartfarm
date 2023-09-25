import Excel from '../JS/excel_show.mjs';

const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
let columnName = [];

const localTitleList = JSON.parse(localStorage.getItem("title_list"));
const $growth = document.querySelector('#growthSelectBox');
const $environment = document.querySelector('#environmentSelectBox');
const $output = document.querySelector('#outputSelectBox');
const $mergeFileName = document.querySelector('#mergeFileName');
const $merge = document.querySelector('#merge');

// select 박스 내용 추가함수
const selectOptionAdd = ()=>{
    for (let x of localTitleList){
        $growth.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
        $environment.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
        $output.innerHTML += `<Option value= '${x}'>` + x + `</option>`;
    }
}
selectOptionAdd();

// select 박스 선택 결과 함수
// columnName에 추가
$merge.addEventListener('click',()=>{
    columnName=[];

    if($mergeFileName.value === ''){
        alert('파일 이름을 정해주세요');
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


    console.log(growthTitle);

    $.ajax({
        url: '../loaddata/',
        type: 'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data: {
            fileName : growthTitle,
        },
        success: function (response) {
            if (response.data != null) {
                console.log(response.data);
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



    // $.ajax({
    //     url: '/mergeView/',
    //     type: 'post',
    //     dataType: 'json',
    //     headers: { 'X-CSRFToken': csrftoken },
    //     data: {
    //         columnName : columnName,
    //         file_name: $mergeFileName.value,
    //     },
    //     success:function(response){
    //         if(response.data != null){
    //             newData = new Excel(JSON.parse(response.data), $spreadsheet3)
    //             document.querySelector('#save').disabled = false;
    //         }
    //     },
    //     error: function (xhr, error) {
    //         alert("에러입니다.");
    //         console.error("error : " + error);
    //     }
    // })
})
