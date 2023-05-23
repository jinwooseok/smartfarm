const $abms_var = document.querySelector('#abms_var');
const $abms_text = document.querySelector('#abms_text');
const $abms_save = document.querySelector('#abms_save');
let abmsData = []; // abms 데이터

let excel_data = JSON.parse(document.getElementById('jsonObject').value);
let excel_col= Object.keys(excel_data[0]);

// 종류 선택
$abms_var.addEventListener('click', (event) => {
    let text = $abms_var.options[$abms_var.selectedIndex].value;

    if (text.includes('토마토')) {
        $abms_text.innerHTML = `
        <div id="농가명" class="농가명">농가명<input type="text" value="농가명" onkeyup="colSearch(event)"></div>
        <div id="조사일자" class="조사일자">조사일자<input type="text" value="조사일자" onkeyup="colSearch(event)"></div>
        <div id="개체번호" class="개체번호">개체번호<input type="text" value="개체번호" onkeyup="colSearch(event)"></div>
        <div id="줄기번호" class="줄기번호">줄기번호<input type="text" value="줄기번호" onkeyup="colSearch(event)"></div>
        <div id="초장" class="초장">초장<input type="text" value="초장" onkeyup="colSearch(event)"></div>
        <div id="생장길이" class="생장길이">생장길이<input type="text" value="생장길이" onkeyup="colSearch(event)"></div>
        <div id="엽수" class="엽수">엽수<input type="text" value="엽수" onkeyup="colSearch(event)"></div>
        <div id="엽장" class="엽장">엽장<input type="text" value="엽장" onkeyup="colSearch(event)"></div>
        <div id="엽폭" class="엽폭">엽폭<input type="text" value="엽폭" onkeyup="colSearch(event)"></div>
        <div id="줄기굵기" class="줄기굵기">줄기굵기<input type="text" value="줄기굵기" onkeyup="colSearch(event)"></div>
        <div id="화방높이" class="화방높이">화방높이<input type="text" value="화방높이" onkeyup="colSearch(event)"></div>
        <div id="화방번호" class="화방번호">화방번호<input type="text" value="화방번호" onkeyup="colSearch(event)"></div>
        <div id="화방별총개수" class="화방별총개수">화방별총개수<input type="text" value="화방별총개수" onkeyup="colSearch(event)"></div>
        <div id="화방별꽃수" class="화방별꽃수">화방별꽃수<input type="text" value="화방별꽃수" onkeyup="colSearch(event)"></div>
        <div id="화방별꽃봉오리수" class="화방별꽃봉오리수">화방별꽃봉오리수<input type="text" value="화방별꽃봉오리수" onkeyup="colSearch(event)"></div>
        <div id="화방별개화수" class="화방별개화수">화방별개화수<input type="text" value="화방별개화수" onkeyup="colSearch(event)"></div>
        <div id="화방별착과수" class="화방별착과수">화방별착과수<input type="text" value="화방별착과수" onkeyup="colSearch(event)"></div>
        <div id="화방별적과수" class="화방별적과수">화방별적과수<input type="text" value="화방별적과수" onkeyup="colSearch(event)"></div>
        <div id="화방별수확수" class="화방별수확수">화방별수확수<input type="text" value="화방별수확수" onkeyup="colSearch(event)"></div> 
        `
    } else if (text === '딸기') {
        $abms_text.innerHTML = `
        <div id="농가명" class="농가명">농가명<input type="text" value="농가명" onkeyup="colSearch(event)"></div>
        <div id="조사일자" class="조사일자">조사일자<input type="text" value="조사일자" onkeyup="colSearch(event)"></div>
        <div id="개체번호" class="개체번호">개체번호<input type="text" value="개체번호" onkeyup="colSearch(event)"></div>
        <div id="액아구분" class="액아구분">액아구분<input type="text" value="액아구분" onkeyup="colSearch(event)"></div>
        <div id="초장" class="초장">초장<input type="text" value="초장" onkeyup="colSearch(event)"></div>
        <div id="엽수" class="엽수">엽수<input type="text" value="엽수" onkeyup="colSearch(event)"></div>
        <div id="엽장" class="엽장">엽장<input type="text" value="엽장" onkeyup="colSearch(event)"></div>
        <div id="엽폭" class="엽폭">엽폭<input type="text" value="엽폭" onkeyup="colSearch(event)"></div>
        <div id="엽병장" class="엽병장">엽병장<input type="text" value="엽병장" onkeyup="colSearch(event)"></div>
        <div id="관부직경" class="관부직경">관부직경<input type="text" value="관부직경" onkeyup="colSearch(event)"></div>
        <div id="화방번호" class="화방번호">화방번호<input type="text" value="화방번호" onkeyup="colSearch(event)"></div>
        <div id="화방출뢰기" class="화방출뢰기">화방출뢰기<input type="text" value="화방출뢰기" onkeyup="colSearch(event)"></div>
        <div id="개화기일자" class="개화기일자">개화기일자<input type="text" value="개화기일자" onkeyup="colSearch(event)"></div>
        <div id="화방별총개수" class="화방별총개수">화방별총개수<input type="text" value="화방별총개수" onkeyup="colSearch(event)"></div>
        <div id="화방별꽃수" class="화방별꽃수">화방별꽃수<input type="text" value="화방별꽃수" onkeyup="colSearch(event)"></div>
        <div id="화방별꽃봉오리수" class="화방별꽃봉오리수">화방별꽃봉오리수<input type="text" value="화방별꽃봉오리수" onkeyup="colSearch(event)"></div>
        <div id="화방별개화수" class="화방별개화수">화방별개화수<input type="text" value="화방별개화수" onkeyup="colSearch(event)"></div>
        <div id="화방별적화수" class="화방별적화수">화방별적화수<input type="text" value="화방별적화수" onkeyup="colSearch(event)"></div>
        <div id="화방별착과수" class="화방별착과수">화방별착과수<input type="text" value="화방별착과수" onkeyup="colSearch(event)"></div>
        <div id="화방별적과수" class="화방별적과수">화방별적과수<input type="text" value="화방별적과수" onkeyup="colSearch(event)"></div>
        <div id="화방별수확수" class="화방별수확수">화방별수확수<input type="text" value="화방별수확수" onkeyup="colSearch(event)"></div>    
        `
    }
})

let inputValue = []; // 우리가 불러올 열 이름들
let abmsColumn = []; // abms 열 이름
// data[abmsColumn] = [inputValue]가 되어야함

// abms 데이터 만들기
$abms_save.addEventListener('click', () =>{
    let abmsChild= document.querySelectorAll('#abms_text > *');
    for(let i=0; i<abmsChild.length; i++){
        abmsColumn.push(abmsChild[i].classList[0]);
        inputValue.push(abmsChild[i].firstElementChild.value);
    }
    for(let i=0; i<excel_data.length;i++){
        let x={}; // 데이터 한 줄
        for(let j in abmsColumn){
            x[abmsColumn[j]] = excel_data[i][inputValue[j]]; 
        }
        console.log(x);
        abmsData.push(x);
    }
    console.log(abmsData)
})

// 검색으로 찾는건 나중에
function colSearch(event){
    let text = event.target.value;
    // for(let i=0; i<excel_col.length; i++){
    //     if(excel_col[i].includes(text)){
    //         event.target.value = excel_col[i];
    //     }
    // }
}

// 할거 
// 1. 우선 파일을 클릭할 때 제목을 local에 넘겨서 제목을 받아옴
// 그리고 저장시 파일제목+abms로 고정

// abms
// 없는 데이터는?
// 만약 같은 날짜가 여러개 있으면 합친다 -> 변수가 달라질것 같은데?

// abmsChild[0].firstElementChild.value
// '123'
// abmsChild[0].classList[0]
// '농가명'
// ['농가명'] 열에 [123]이름의 열이 들어가야 함