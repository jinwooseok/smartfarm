import Excel from "/templates/JS/Utils/Excel.mjs";
import Loading from "/templates/JS/Utils/Loading.mjs";
import { reviseDefaultValue } from "/templates/JS/revise/constantValue.js";

const csrftoken = $("[name=csrfmiddlewaretoken]").val(); // csrftoken

// upload를 통해 저장된 파일 이름을 불러옴
const fileListTitles = JSON.parse(localStorage.getItem("title_list"));
const $fileListSelectBox = document.querySelector("#fileListSelectBox");
const selectedFileTitle = JSON.parse(localStorage.getItem("fileTitle"));

const checkNowFileTitle = () => {
  fileListTitles.map( (title) => {
    if (title === selectedFileTitle) {
      $fileListSelectBox.innerHTML += `<Option value= '${title}' selected>` + title + `</option>`;
    }
    $fileListSelectBox.innerHTML += `<Option value= '${title}'>` + title + `</option>`;
  });
};

const moveSelectedFileTitle = () => {
  const selectedFileTitle =  $fileListSelectBox.options[$fileListSelectBox.selectedIndex].value;
  localStorage.setItem("fileTitle", JSON.stringify(selectedFileTitle));
  const link = document.createElement("a");
  link.href = `/revise/${selectedFileTitle}/`;
  link.style = "visibility:hidden";

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

$fileListSelectBox.addEventListener("change", moveSelectedFileTitle);

///////////////////////////////
let data;

const $spreadsheet = document.querySelector("#spreadsheet"); // 엑셀 창
const $fileName = document.querySelector("#fileName");
const $abmsFileName = document.querySelector("#abmsFileName");
const $pretreatmentFileName = document.querySelector("#pretreatmentFileName");
const $x_label = document.querySelector("#x_label");
const $dataColumnList = document.querySelector("#dataColumnList");

const setFileName = () => {
  const name = selectedFileTitle.replace(/(.csv|.xlsx|.xls)/g, "");
  $fileName.value = name + "_수정";
  $abmsFileName.value = name + "_ABMS";
  $pretreatmentFileName.value = name + "_전처리";
};

const settingDate = () => {
  data = new Excel(JSON.parse(document.getElementById("jsonObject").value).slice(0,100), $spreadsheet);
};

const addColumn = (htmlTag, text="") => {
  htmlTag.innerHTML = "";
  if (text !== "") {
    Object.keys(data.getData()[0]).map( (column) => {
      if (column.includes(text)) {
        htmlTag.innerHTML += `<option value="${column}">${column}</option>`
      }
    })
    return;
  };

  Object.keys(data.getData()[0]).map( (column) => {
    htmlTag.innerHTML += `<option value="${column}">${column}</option>`
  });
};

const start = () => {
  Loading.StartLoading();
  checkNowFileTitle();
  settingDate();
  setFileName();
  addColumn($dataColumnList);
  addColumn($x_label);
  Loading.CloseLoading();
};

start();

////////////////////////////////
const $wordContain = document.querySelector("#wordContain");
const $thirdText = document.querySelector("#thirdText");

const addWordContainSelectBox = (event) => {
  const selectValue = event.target.textContent;
  switch(selectValue) {
    case "전체" :
      addColumn($thirdText);
      break;
    case "온도" :
    case "기온" :
    case "습도" :
    case "CO2" :
    case "co2" :
    case "일사량" :
    case "일사" :
    case "강수량" :
      addColumn($thirdText, selectValue);
      break;
  }
};

$wordContain.addEventListener("click", addWordContainSelectBox);

const $selectedValueList = document.querySelector("#selectedValueList");
const $defaultSelect = document.querySelector("#defaultSelect"); // 쉬운 버전

let newDataArr = []; // 최종 select-final에 들어갈 때 값 중복 검사를 위한 배열, "주간평균내부온도" 형식
let newData = []; // 우리가 전송할 새로운 DATA, [ {text1 : [[text2, text3]] }] 형식

let newDataObj = {}; // newData에 들어갈 객체
function addObject(text1, text2, text3) {
  let objIndex = newData.findIndex((obj) => Object.keys(obj).includes(text1));

  if (objIndex > -1) {
    newData[objIndex][text1].push([text2, text3]);
  } else {
    newDataObj = new Object();
    newDataObj[text1] = [[text2, text3]];
    newData.push(newDataObj);
  }
}

// 배열 중복 검사
let duplicateArr = []; // 중복 배열
function checkDuplicate(new_value) {
  if (newDataArr.includes(new_value)) {
    duplicateArr.push(new_value);
    return false;
  }
  return !newDataArr.includes(new_value);
}

const createEasyVersionData  = (event) => {
  const selectedDefaultValue = event.target.textContent;
  const selectedValue =  $dataColumnList.options[$dataColumnList.selectedIndex]?.value ;

  if (selectedValue === undefined) {
    alert('왼쪽 상자에서 값을 선택해주세요');
    return;
  };

  reviseDefaultValue.map( (defaultValue) => {
    const value = defaultValue.split("_");

    if (checkDuplicate(value.join("") + selectedValue)) {
      if (selectedDefaultValue === "전체") {
        $selectedValueList.innerHTML += 
        `<Option value= '${defaultValue}${selectedValue}'>` +
          value.join("") + selectedValue +
        `</option>`;
        newDataArr.push(value.join("") + selectedValue);
        addObject(selectedValue, value[0], value[1]);
      }
      if (selectedDefaultValue === "온도") {
        $selectedValueList.innerHTML += 
        `<Option value= '${defaultValue}${selectedValue}'>` +
          value.join("") + selectedValue +
        `</option>`;
        newDataArr.push(value.join("") + selectedValue);
        addObject(selectedValue, value[0], value[1]);
      }
      if (
        selectedDefaultValue === "습도" ||
        selectedDefaultValue === "CO2"||
        selectedDefaultValue === "co2"
      ) {
        if (
          value[1] !== "DIF" ||
          value[1] !== "GDD" ||
          value[0] !== "일출전후t시간"
        ) {
          $selectedValueList.innerHTML += 
          `<Option value= '${defaultValue}${selectedValue}'>` +
            value.join("") + selectedValue +
          `</option>`;
          newDataArr.push(value.join("") + selectedValue);
          addObject(selectedValue, value[0], value[1]);
        }
      }
      if (selectedDefaultValue === "일사량") {
        alert("어떻게 넣어야 하는지 잘 모르겠다.");
        // $selectedValueList.innerHTML += 
        // `<Option value= '${defaultValue}${selectedValue}'>` +
        //   value.join("") + selectedValue +
        // `</option>`;
      } 
      if (selectedDefaultValue === "강수량") {
        alert("어떻게 넣어야 하는지 잘 모르겠다.");
        // $selectedValueList.innerHTML += 
        // `<Option value= '${defaultValue}${selectedValue}'>` +
        //   value.join("") + selectedValue +
        // `</option>`;
      }
    }
  })

  if (duplicateArr.length) {
    alert(`${duplicateArr}은 중복 값이라 제거했습니다.`);
    duplicateArr = [];
  }

}

$defaultSelect.addEventListener("click", createEasyVersionData);

///////////////////////

const $firstText = document.querySelector("#firstText");
const $secondText = document.querySelector("#secondText");
const $optionSelect = document.querySelector("#optionSelect");

const text = {
  first: "",
  second: "",
  third: "",
}

$firstText.addEventListener("click", (event) => {
  text.first = event.target.textContent;
});
$secondText.addEventListener("click", (event) => {
  text.second = event.target.textContent;
});
$thirdText.addEventListener("click", (event) => {
  text.third = event.target.textContent;
});

const createHardVersionData = () => {
  if (text.first === "") {
    alert('처음 값을 선택해 주세요');
    return;
  };
  if (text.second === "") {
    alert('두번째 값을 선택해 주세요');
    return;
  };
  if (text.third === "") {
    alert('마지막 값을 선택해 주세요');
    return;
  };

  const value = text.first+text.second+text.third;
  if (checkDuplicate(value)) {
    console.log("XXX")
    $selectedValueList.innerHTML += `<Option value= '${text.first}_${text.second}_${text.third}'>` + value + `</option>`;
    newDataArr.push(value);
    addObject(text.third, text.first, text.second);
  };

  if (duplicateArr.length) {
    alert(`${duplicateArr}은 중복 값이라 제거했습니다.`);
    duplicateArr = [];
  }
};

$optionSelect.addEventListener("click", createHardVersionData);

// 삭제 함수
function varDelete() {
  const checked = $selectedValueList.selectedOptions;
  const checkedList = Array.from(checked).map(option => option.value);

  if (checkedList) {
    for (let value of checkedList) {
      const inputValue = value.split("_");
      for (let i = 0; i < Object.keys(newData).length; i++) {
        if (Object.keys(newData[i])[0] === inputValue[2]) {
          for (let j = 0; j < newData[i][inputValue[2]].length; j++) {
            if (
              newData[i][inputValue[2]][j].includes(inputValue[0]) &&
              newData[i][inputValue[2]][j].includes(inputValue[1])
            ) {
              newDataArr.splice(newDataArr.indexOf(inputValue.join("")), 1); // 배열 제거
              newData[i][inputValue[2]].splice(j, 1); // 객체에서 제거
              break;
            }
          }
          if (newData[i][inputValue[2]].length === 0) {
            delete newData[i][inputValue[2]];
          }
        }
      }
      for (let i = checked.length - 1; i >= 0; i--) {
        const option = checked[i];
        $selectedValueList.remove(option.index);
      }
    }
  } else {
    alert("삭제할 항목을 선택하세요");
  }
}

const $optionDelete = document.querySelectorAll("#optionDelete");
// 변수 삭제
$optionDelete[0].addEventListener("click", varDelete);
$optionDelete[1].addEventListener("click", varDelete);

/////////////

const $submitData = document.querySelector("#submitData");
const $resetData = document.querySelector("#resetData");

const $date = document.querySelector("#date"); // 날짜 열 input
const $startIndex = document.querySelector("#startIndex"); // 날짜 열 input
const $type = document.querySelectorAll('input[name="type"]'); // 파일 종류 확인
const $period = document.querySelectorAll('input[name="period"]'); // 파일 종류 확인
const $periodContainer = document.querySelector('#periodContainer'); // 파일 종류 확인
// const $typeSelectContainer = document.querySelector('#typeSelectContainer'); // 파일 종류 확인

const checkRadioValue = (htmlTag) => {
  for (let i = 0; i < htmlTag.length; i++) {
    if (htmlTag[i].checked) {
      if (htmlTag[i].value === "else"){
        return document.getElementById("elsePeriod").value;
      }
      return htmlTag[i].value;
    }
  }
}

$periodContainer.addEventListener('click', (event) => {
  if (event.target.value === "else") {
    document.querySelector("#elsePeriod").disabled = false;
    return;
  } 
  document.querySelector("#elsePeriod").disabled = true;
})

// 초기화
$resetData.addEventListener("click", () => {
  newData = [];
  newDataArr = [];
  $selectedValueList.innerHTML = "";
  $fileName.value = "";
});

// 저장
$submitData.addEventListener("click", () => {
  $submitData.disabled = true;
  const yesOrNo = confirm("파일을 저장합니다."); // 예, 아니요를 입력 받음

  if (yesOrNo) {
    Loading.StartLoading();
    $.ajax({
      url: "farm/",
      type: "post",
      dataType: "json",
      headers: { "X-CSRFToken": csrftoken },
      data: {
        new_file_name: $fileName.value,
        file_type: checkRadioValue($type),
        startIndex: $startIndex.value,
        date: $date.value,
        DorW: checkRadioValue($period),
        valueObject: JSON.stringify(newData),
      },
      success: function (response) {
        if (response.data != null) {
          window.location.href = "/file-list/";
        } else {
          $submitData.disabled = false;
          alert("전송할 데이터가 없습니다.");
        }
      },
      error: function (xhr, error) {
        $submitData.disabled = false;
        alert("에러입니다.");
        console.error("error : " + error);
      },
    });
  }
  Loading.CloseLoading();
  $submitData.disabled = false;
});