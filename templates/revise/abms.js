const $abms_var = document.querySelector('#abms_var');
const $abms_text = document.querySelector('#abms_text');
const $abms_save = document.querySelector('#abms_save');
let abmsData = []; // abms 데이터

let excel_data = JSON.parse(document.getElementById('jsonObject').value);
let excel_col= Object.keys(excel_data[0]);

const csrftoken = $('[name=csrfmiddlewaretoken]').val();

// 종류 선택
$abms_var.addEventListener('click', (event) => {
    let text = $abms_var.options[$abms_var.selectedIndex].value;

    if (text.includes('토마토')) {
        $abms_text.innerHTML = `
        <div id="columnBox" class="columnBox">
        농가명<select name="농가명" id="농가명">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        조사일자<select name="조사일자" id="조사일자">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        개체번호<select name="개체번호" id="개체번호">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        줄기번호<select name="줄기번호" id="줄기번호">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        초장<select name="초장" id="초장">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        생장길이<select name="생장길이" id="생장길이">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        엽수<select name="엽수" id="엽수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        엽장<select name="엽장" id="엽장">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        엽폭<select name="엽폭" id="엽폭">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        줄기굵기<select name="줄기굵기" id="줄기굵기">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방높이<select name="화방높이" id="화방높이">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방번호<select name="화방번호" id="화방번호">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별총개수<select name="화방별총개수" id="화방별총개수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별꽃수<select name="화방별꽃수" id="화방별꽃수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별꽃봉오리수<select name="화방별꽃봉오리수" id="화방별꽃봉오리수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별개화수<select name="화방별개화수" id="화방별개화수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별착과수<select name="화방별착과수" id="화방별착과수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별적과수<select name="화방별적과수" id="화방별적과수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별수확수<select name="화방별수확수" id="화방별수확수">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        비고<select name="비고" id="비고">
            <option value="null"></option>
        </select>
    </div>
            `
    } else if (text === '딸기') {
        $abms_text.innerHTML = `
            <div id="columnBox" class="columnBox">
                농가명<select name="농가명" id="농가명">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                조사일자<select name="조사일자" id="조사일자">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                개체번호<select name="개체번호" id="개체번호">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                액아구분<select name="액아구분" id="액아구분">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                초장<select name="초장" id="초장">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                엽수<select name="엽수" id="엽수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                엽장<select name="엽장" id="엽장">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                엽폭<select name="엽폭" id="엽폭">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                엽병장<select name="엽병장" id="엽병장">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                관부직경<select name="관부직경" id="관부직경">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방번호<select name="화방번호" id="화방번호">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방출뢰기<select name="화방출뢰기" id="화방출뢰기">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                개화기일자<select name="개화기일자" id="개화기일자">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별총개수<select name="화방별총개수" id="화방별총개수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별꽃수<select name="화방별꽃수" id="화방별꽃수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별꽃봉오리수<select name="화방별꽃봉오리수" id="화방별꽃봉오리수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별개화수<select name="화방별개화수" id="화방별개화수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별적화수<select name="화방별적화수" id="화방별적화수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별착과수<select name="화방별착과수" id="화방별착과수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별적과수<select name="화방별적과수" id="화방별적과수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                화방별수확수<select name="화방별수확수" id="화방별수확수">
                <option value="null"></option></select>
            </div>
            <div id="columnBox" class="columnBox">
                비고<select name="비고" id="비고">
                <option value="null"></option></select>
            </div>
            `
    }
    setSelectedValue();
})

// selectBox 값
function setSelectedValue() {
    let abmsChild = document.querySelectorAll('#columnBox');
    const $columnBox_select = document.querySelectorAll('#columnBox > select');

    for (let i = 0; i < abmsChild.length; i++) {
        $columnBox_select[i].innerHTML = '<option value="null"></option>'
        for (let x of excel_col) {
            if (abmsChild[i].childNodes[0].data.trim() === x) {
                $columnBox_select[i].innerHTML += `<Option value= '${x}' selected>` + x + `</option>`;
            } else {
                $columnBox_select[i].innerHTML += `<Option value= '${x}'>` + x + `</option>`;
            }
        }
    }
}
setSelectedValue();
let inputValue = []; // 우리가 불러올 열 이름들
let abmsColumn = []; // abms 열 이름
// data[abmsColumn] = [inputValue]가 되어야함


// abms 데이터 만들기
$abms_save.addEventListener('click', () =>{
    abmsData=[];
    let abmsChild = document.querySelectorAll('#columnBox');
    const $columnBox_select = document.querySelectorAll('#columnBox > select');

    for (let i = 0; i < abmsChild.length; i++) {
        abmsColumn.push(abmsChild[i].childNodes[0].data.trim());
        inputValue.push($columnBox_select[i].options[$columnBox_select[i].selectedIndex].value);
    }
    for(let i=0; i<excel_data.length;i++){
        let x={}; // 데이터 한 줄
        for(let j in abmsColumn){
            x[abmsColumn[j]] = excel_data[i][inputValue[j]]??''; 
        }
        abmsData.push(x);
    }

    $.ajax({
        url: '/mergeView/',
        type:'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data:{
            header:"save",
            data: JSON.stringify(abmsData),
            file_name : document.querySelector('#abmsFileName').value,
        },
        success:function(response){
            if(response.data != null){
                location.href=`/fileList`; // 이게 작동 안함
            }
        },
    })
})
