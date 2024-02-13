import { abmsTextValue } from "../../Constant/variableList.mjs";
import API from "/templates/src/Utils/API.mjs";

const $abmsType = document.querySelector("#abmsType");
const $abmsText = document.querySelector("#abmsText");
const $abmsSave = document.querySelector("#abmsSave");
const $abmsFileName = document.querySelector("#abmsFileName");
const $startIndex = document.querySelector("#startIndex");
const $date = document.querySelector("#date");

const fileName = JSON.parse(localStorage.getItem("fileTitle"));
$abmsFileName.value = fileName.replace(/(.csv|.xlsx|.xls)/g, "") +  "_ABMS";

const setFileData = async () =>{
	const response = await API(`/files/${fileName}/data/`, "get");
	return response.data;
}

const data = await setFileData();
const variableList = Object.keys(data[0]);

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
const setSelectedValue = () => {
  const $columnBox = document.querySelectorAll("#columnBox");
  const $columnBoxSelect = document.querySelectorAll("#columnBox > select");

  for (let i=0; i < $columnBox.length; i++) {
    $columnBoxSelect[i].innerHTML = '<option value="null"></option>';
    variableList.map((column) => {
      const value = column.trim();
      if ($columnBox[i].childNodes[0].data.trim() === value) {
        $columnBoxSelect[i].innerHTML += `<option value='${value}' selected>` + value + `</option>`;
      } else {
        $columnBoxSelect[i].innerHTML += `<option value='${value}'>` + value + `</option>`;
      }
    });
  }

};

$abmsText.innerHTML = generateColumnHTML(abmsTextValue["환경"]);
setSelectedValue()

const setABMSdata = () =>{
  const abmsData = [];
  const inputValue = [];
  const abmsColumn = [];
	
	const $columnBox = document.querySelectorAll("#columnBox");
	const $columnBoxSelect = document.querySelectorAll("#columnBox > select");

  for (let i = 0; i < $columnBox.length; i++) {
    // abmsColumn.push($columnBox[i].childNodes[0].data.trim()); 한글
    abmsColumn.push($columnBox[i].childNodes[1].id); // 영문
    inputValue.push($columnBoxSelect[i].value);
  }

  data.map((row) => {
    let addObjectToABMSData = {};
    inputValue.map((value, index) => {
      addObjectToABMSData[abmsColumn[index]] = (row[value] || row[`${value} `]) ?? 'null';
    });
    abmsData.push(addObjectToABMSData);
		console.log(addObjectToABMSData)
  })
  return abmsData;
};

const setEnvData = () => {
	// [[before,after],[before,after]]
	const abmsData = [];

	const $columnBox = document.querySelectorAll("#columnBox");
	const $columnBoxSelect = document.querySelectorAll("#columnBox > select");

  for (let i = 0; i < $columnBox.length; i++) {
    // abmsColumn.push($columnBox[i].childNodes[0].data.trim()); 한글
    abmsData.push([$columnBoxSelect[i].value, $columnBox[i].childNodes[1].id]); // 영문
  }

	return abmsData;
}

// abms 데이터 만들기
$abmsSave.addEventListener("click", async() => {
	const fileType = $abmsType.options[$abmsType.selectedIndex].value;
  console.log(setEnvData())

	// if (fileType !== "환경") {
	// 	const response = await API("/files/save/", "post", {
	// 		fileName: $abmsFileName.value,
	// 		fileData : JSON.stringify(setABMSdata()),
	// 	});

	// 	response.status === "success" ? location.replace("/file-list/") : alert("에러");
	// 	return;
	// }

	// const response = await API(`/abms/${fileName}/env/`, "post", {
	// 	startIndex : $startIndex.value,
	// 	date: $date.value,
	// 	columns: JSON.stringify(setEnvData()),
	// 	newFileName: $abmsFileName.value,
	// });
	// response.status === "success" ? location.replace("/file-list/") : alert("에러");
	// return;
});

$abmsType.addEventListener("change", () => {
  const text = $abmsType.options[$abmsType.selectedIndex].value;
  $abmsText.innerHTML = generateColumnHTML(abmsTextValue[text]);
  setSelectedValue();
});