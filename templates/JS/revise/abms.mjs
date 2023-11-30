import { abmsTextValue } from "/templates/JS/revise/constantValue.mjs";

const $abmsType = document.querySelector("#abmsType");
const $abmsText = document.querySelector("#abmsText");
const $abmsSave = document.querySelector("#abmsSave");
const $abmsFileName = document.querySelector("#abmsFileName");
const csrftoken = $("[name=csrfmiddlewaretoken]").val();
const $columnBox = document.querySelectorAll("#columnBox");
const $columnBoxSelect = document.querySelectorAll("#columnBox > select");

const excelData = JSON.parse(document.getElementById("jsonObject").value);
const excelCol = Object.keys(excelData[0]);

// 종류 선택
const generateColumnHTML = (columnSet) => {
  return Object.entries(columnSet)
    .map(
      ([columnName, columnId]) => `
      <div id="columnBox" class="columnBox">
        ${columnName}
        <select name="${columnName}" id="${columnId}">
          <option value="null"></option>
        </select>
      </div>
    `
    )
    .join("");
};

// selectBox 초기값
function setSelectedValue() {
  const $columnBox = document.querySelectorAll("#columnBox");
  const $columnBoxSelect = document.querySelectorAll("#columnBox > select");

  for (let i=0; i < $columnBox.length; i++) {
    $columnBoxSelect[i].innerHTML = '<option value="null"></option>';
    excelCol.map((column) => {
      if ($columnBox[i].childNodes[0].data.trim() === column) {
        $columnBoxSelect[i].innerHTML += `<Option value='${column}' selected>` + column + `</option>`;
      } else {
        $columnBoxSelect[i].innerHTML += `<Option value='${column}'>` + column + `</option>`;
      }
    });
  }

};

const setABMSdata = () =>{
  const abmsData = [];
  const inputValue = [];
  const abmsColumn = [];

  for (let i = 0; i < $columnBox.length; i++) {
    // abmsColumn.push($columnBox[i].childNodes[0].data.trim()); 한글
    abmsColumn.push($columnBox[i].childNodes[1].id); // 영문
    inputValue.push($columnBoxSelect[i].value);
  }

  for (let i = 0; i < excelData.length; i++) {
    let x = {};
    for (let j in abmsColumn) {
      x[abmsColumn[j]] = excelData[i][inputValue[j]] ?? "";
    }
    abmsData.push(x);
  }

  return abmsData;
};

setSelectedValue();

// abms 데이터 만들기
$abmsSave.addEventListener("click", () => {
  const ABMSdata = setABMSdata();
  $.ajax({
    url: `/revise/${JSON.parse(localStorage.getItem("fileTitle"))}/abms/`,
    type: "post",
    dataType: "json",
    headers: { "X-CSRFToken": csrftoken },
    data: {
      newFileName: $abmsFileName.value,
      ABMSData : ABMSdata,
    },
    success: function (response) {
      alert("완료되었습니다.");
      window.location.href = "/file-list/";
    },
    error : function(xhr, ajaxSettings, thrownError) 
    {
        alert("수정하는데 오류가 발생하였습니다.");
    },
  });
});

$abmsType.addEventListener("change", () => {
  const text = $abmsType.options[$abmsType.selectedIndex].value;
  $abmsText.innerHTML = generateColumnHTML(abmsTextValue[text]);
  setSelectedValue();
});