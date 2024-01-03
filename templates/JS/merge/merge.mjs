import Excel from "/templates/JS/Utils/Excel.mjs";
import cookies from "/templates/JS/Utils/csrfToken.mjs";
import Loading from "/templates/JS/Utils/Loading.mjs";

const csrftoken = cookies['csrftoken'] // csrftoken

const $selectBoxes = {
  growth: document.querySelector("#growthSelectBox"),
  environment: document.querySelector("#environmentSelectBox"),
  output: document.querySelector("#outputSelectBox"),
};

const $variables = {
  growth: document.querySelector("#growthVariable"),
  environment: document.querySelector("#environmentVariable"),
  output: document.querySelector("#outputVariable"),
};

const $mergeFileName = document.querySelector("#mergeFileName");
const $merge = document.querySelector("#merge");
const $save = document.querySelector("#save");
const $spreadsheet = document.querySelector("#spreadsheet"); // 엑셀 창

let mergeDataList = Array(3).fill('');
let mergeCompleteData; // 

// 선택한 파일 불러오기
const postFilename = async (name) => {
  try {
    const response = await $.ajax({
      url: "../loaddata/",
      type: "post",
      dataType: "json",
      headers: { "X-CSRFToken": csrftoken },
      data: { fileName: name },
      async: false,
    });

    if (response.data != null) {
      return response.data;
    } else {
      alert("전송할 데이터가 없습니다.");
    }
  } catch (error) {
    alert("에러입니다.");
    console.error("error : " + error);
  }
};

// 파일 변수 불러오기
const updateVariableOptions = async ($selectBox, $variable, index) => {
  $variable.innerHTML = "";
  const title = $selectBox.options[$selectBox.selectedIndex].textContent;

  if (title === '') {
    $variable.innerHTML = "";
    mergeDataList[index] = '';
    return;
  }

  try {
    const data = await postFilename(title);
    mergeDataList[index] = data;

    const dataColumn = Object.keys(JSON.parse(data)[0]);
    for (let x of dataColumn) {
      $variable.innerHTML += `<Option value='${x}'>${x}</option>`;
    }
  } catch (error) {
    alert("다른 파일을 선택해주세요.");
  }
};

Object.values($selectBoxes).forEach(($selectBox, index) => {
  $selectBox.addEventListener("change", () => {
    updateVariableOptions($selectBox, Object.values($variables)[index], index);
  });
});

const setMergeColumn = () => {
  const $variableSelectBoxes = [$variables.growth, $variables.environment, $variables.output];

  const columnName = $variableSelectBoxes
    .map($selectBox => $selectBox.options[$selectBox.selectedIndex]?.value)
    .filter(title => title !== "null");

  return columnName;
}

// 병합
$merge.addEventListener("click", async () => {
  $spreadsheet.innerHTML = "";
  const mergeColumn = setMergeColumn();

  while (mergeDataList.indexOf('') > -1) {
    mergeDataList.splice(mergeDataList.indexOf(''), 1);
  }

  Loading.StartLoading();

  try {
    const response = await $.ajax({
      url: "../merge-view/",
      type: "post",
      dataType: "json",
      headers: { "X-CSRFToken": csrftoken },
      data: {
        header: "merge",
        columnName: JSON.stringify(mergeColumn),
        data: JSON.stringify(mergeDataList),
      },
    });

    if (response.data != null) {
      mergeCompleteData = new Excel(JSON.parse(response.data).slice(0, 500), $spreadsheet); // 200개만 보여줌
      Loading.CloseLoading();
    }
  } catch (error) {
    Loading.CloseLoading();
    alert("에러입니다.");
    console.error("error : " + error);
  }
});

const checkFileName = () => {
  if ($mergeFileName.value === "") {
    alert("파일 이름을 정해주세요");
    return false;
  }
  return true;
}

// 저장하기
$save.addEventListener("click", async () => {
  if (!checkFileName()) return;

  Loading.StartLoading();

  const mergedFileName = $mergeFileName.value;
  const mergeData = JSON.stringify(mergeCompleteData.getData());

  try {
    const response = await $.ajax({
      url: "../merge-view/",
      type: "post",
      dataType: "json",
      headers: { "X-CSRFToken": csrftoken },
      data: {
        header: "save",
        fileName: mergedFileName,
        mergedData: mergeData,
      },
    });
    // response.data가 없음
    window.location.href = "/file-list/";
    Loading.CloseLoading();
  } catch (error) {
    alert("에러입니다.");
    Loading.CloseLoading();
    console.error("error : " + error);
  }
});