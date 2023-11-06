const $abms_var = document.querySelector('#abms_var');
const $abms_text = document.querySelector('#abms_text');
const $abms_save = document.querySelector('#abms_save');
const $abmsFileName = document.querySelector('#abmsFileName');

const excel_data = JSON.parse(document.getElementById('jsonObject').value);
const excel_col= Object.keys(excel_data[0]);

const csrftoken = $('[name=csrfmiddlewaretoken]').val();

// 종류 선택
$abms_var.addEventListener('click', (event) => {
    const text = $abms_var.options[$abms_var.selectedIndex].value;

    if (text.includes('토마토')) {
        $abms_text.innerHTML = `
    <div id="columnBox" class="columnBox">
        농가명<select name="농가명" id="FRMHS_NM">
            <option value="null"></option>
    </select>
    </div>
    <div id="columnBox" class="columnBox">
        조사일자<select name="조사일자" id="EXAMIN_DATETM">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        개체번호<select name="개체번호" id="PPLT_NO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        줄기번호<select name="줄기번호" id="STEM_NO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        초장<select name="초장" id="PLLN">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        생장길이<select name="생장길이" id="GRWT_LT">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        엽수<select name="엽수" id="FLG_YLD">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        엽장<select name="엽장" id="LFLN">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        엽폭<select name="엽폭" id="FLG_BT">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        줄기굵기<select name="줄기굵기" id="STEM_DMT">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방높이<select name="화방높이" id="FCLU_HG">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방번호<select name="화방번호" id="FCLU_NO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별총개수<select name="화방별총개수" id="TOTAL_PER_FCLU">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별꽃수<select name="화방별꽃수" id="FCLU_FLWR_CO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별꽃봉오리수<select name="화방별꽃봉오리수" id="FCLU_BLM_CO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별개화수<select name="화방별개화수" id="FCLU_FLAN_CO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별착과수<select name="화방별착과수" id="FCLU_FRTST_CO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별적과수<select name="화방별적과수" id="FCLU_FRTTHIN_CO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별수확수<select name="화방별수확수" id="FCLU_HVST_CO">
            <option value="null"></option>
        </select>
    </div>
    <div id="columnBox" class="columnBox">
        비고<select name="비고" id="RM">
            <option value="null"></option>
        </select>
    </div>
            `
    } else if (text === '딸기') {
        $abms_text.innerHTML = `
    <div id="columnBox" class="columnBox">
        농가명<select name="농가명" id="FRMHS_NM">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        조사일자<select name="조사일자" id="EXAMIN_DATETM">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        개체번호<select name="개체번호" id="PPLT_NO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        액아구분<select name="액아구분" id="AXBD_SE">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        초장<select name="초장" id="PLLN">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        엽수<select name="엽수" id="FLG_YLD">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        엽장<select name="엽장" id="LFLN">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        엽폭<select name="엽폭" id="FLG_BT">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        엽병장<select name="엽병장" id="LFST_LT">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        관부직경<select name="관부직경" id="CROWN_DMT">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방번호<select name="화방번호" id="FCLU_NO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방출뢰기<select name="화방출뢰기" id="FCLU_BUDDING_DT">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        개화기일자<select name="개화기일자" id="BLPR_DATETM">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별총개수<select name="화방별총개수" id="TOTAL_PER_FCLU">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별꽃수<select name="화방별꽃수" id="FCLU_FLWR_CO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별꽃봉오리수<select name="화방별꽃봉오리수" id="FCLU_BLM_CO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별개화수<select name="화방별개화수" id="FCLU_FLAN_CO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별적화수<select name="화방별적화수" id="FCLU_DEBLM_CO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별착과수<select name="화방별착과수" id="FCLU_FRTTHIN_CO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별적과수<select name="화방별적과수" id="FCLU_FRTST_CO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        화방별수확수<select name="화방별수확수" id="FCLU_HVST_CO">
        <option value="null"></option></select>
    </div>
    <div id="columnBox" class="columnBox">
        비고<select name="비고" id="비고" value="RM">
        <option value="null"></option></select>
    </div>
            `
    }
    setSelectedValue();
})

// selectBox 초기값
function setSelectedValue() {
    let $columnBox = document.querySelectorAll('#columnBox');
    const $columnBox_select = document.querySelectorAll('#columnBox > select');

    for (let i = 0; i < $columnBox.length; i++) {
        $columnBox_select[i].innerHTML = '<option value="null"></option>'
        for (let x of excel_col) {
            if ($columnBox[i].childNodes[0].data.trim() === x) {
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


// abms 데이터 만들기
$abms_save.addEventListener('click', () =>{
    const abmsData=[];
    const $columnBox = document.querySelectorAll('#columnBox');
    const $columnBox_select = document.querySelectorAll('#columnBox > select');
    for (let i = 0; i < $columnBox.length; i++) {
        // abmsColumn.push($columnBox[i].childNodes[0].data.trim()); 한글
        abmsColumn.push($columnBox[i].childNodes[1].id); // 영문
        inputValue.push($columnBox_select[i].value);
    }
    for (let i = 0; i < excel_data.length; i++) {
        let x = {}; // 데이터 한 줄
        for (let j in abmsColumn) {
            x[abmsColumn[j]] = excel_data[i][inputValue[j]] ?? '';
        }
        abmsData.push(x);
    }

    console.log(JSON.stringify(abmsData));
    console.log($abmsFileName.value);

    $.ajax({
        url: `revise/${JSON.parse(localStorage.getItem("title_list"))}/abms/`,
        type:'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data:{
            newFileName : $abmsFileName.value,
        },
        success:function(response){
            alert("완료되었습니다.");
            window.location.href = "/fileList/";
        },
    })
})
