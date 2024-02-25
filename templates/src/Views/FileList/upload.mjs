import API from "/templates/src/Utils/API.mjs";
import Excel from "/templates/src/Model/Excel.mjs";
import { setFileList } from "/templates/src/Utils/fileNameList.mjs";

const $file = document.querySelector(".file");
const $uploadDialog = document.querySelector("#uploadDialog");
const $upload = document.querySelector("#upload");
const $fileUpload = document.querySelector("#fileUpload");
const $closeUploadPopup = document.querySelector("#closeUploadPopup");
const $dateBox = document.querySelector("#dateBox");
const $startIndex = document.querySelector("#startIndex");

const $fileUploadInput = document.querySelector("#fileUploadInput");
const $fileIcon = document.querySelector("#fileIcon");
const $fileName = document.querySelector("#fileName");


const fileHtml = `
  <div class="icon">
  <i class="fa-solid fa-cloud-arrow-up" id="fileIcon"></i>
    <span>파일을 선택하세요</span>
  </div>
  `

let selectedFile;
let sheetData = "";

const fileSetting = (status) => {
  $file.innerHTML = status === "start" ? fileHtml : "";
  $fileIcon.style.display = status === "start" ? "flex" : "none";
  $fileName.value = status === "start" ? "선택한 파일 이름" : selectedFile.name.replace(/\s/g, "_");
}

// 파일 업로드 버튼 팝업창 관리 함수
$upload.addEventListener("click", () => {
  fileSetting("start");
  $uploadDialog.style.display = "flex";
	$uploadDialog.showModal();
})

$closeUploadPopup.addEventListener("click", () => {
  $dateBox.innerHTML = "";
  $uploadDialog.style.display = "none";
  $uploadDialog.close();
});

const readFileContent = (file, fileType) => {
  const reader = new FileReader();

  reader.onload = function (event) {
    const fileContent = event.target.result;
    if (fileType === 'xlsx') {
      const workbook = XLSX.read(fileContent, { type: 'binary' });
      sheetData = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[workbook.SheetNames[0]]);
    } else if (fileType === 'csv') {
      sheetData = parseCSV(fileContent);
    }

    new Excel(sheetData.slice(0, 30), $file);
    setFileList($dateBox, Object.keys(sheetData[0]));
  };

  reader.onerror = function (event) {
    console.error(event.target.error);
  };

  if (fileType === 'xlsx') {
    reader.readAsBinaryString(file);
  } else if (fileType === 'csv') {
    reader.readAsText(file, 'EUC-KR');
  }
};

const parseCSV = (csvContent) => {
  const lines = csvContent.split('\n');
  const result = [];
  
  // 첫 줄을 헤더로 사용
  const headers = lines[0].split(',');

  // 나머지 줄 처리
  for (let i = 1; i < lines.length - 1; i++) {
    const values = lines[i].replace(/"(\d+),(\d+)"/g, '$1$2').split(',');
    const entry = {};
    headers.forEach((header, index) => {
      entry[header] = values[index];
    });
    result.push(entry);
  }
  return result;
}

const showFile = () => {
  fileSetting("setting");
  if (
    $fileName.value.toLowerCase().includes("xls") ||
    $fileName.value.toLowerCase().includes("xlsx") 
  ) {
    readFileContent(selectedFile, 'xlsx');
    return;
  }

  if ($fileName.value.toLowerCase().includes("csv")) {
    readFileContent(selectedFile, 'csv');
    return;
  }
}

$fileUploadInput.addEventListener("input", (event) => {
  selectedFile = event.target.files[0];
  console.log(event.target.files)
  if (!selectedFile) {
    return;
  }
  showFile();
});

// 파일 업로드
const uploadFile = async () => {
	const data = {
		fileName: $fileName.value,
		fileData: JSON.stringify(sheetData),
    startIndex: $startIndex.value,
    dateColumn: $dateBox.options[$dateBox.selectedIndex]?.value,
	};
	const response = await API("/files/save/", "post" , data);
  const status = response.status;
	return status === "success" ? location.replace("/file-list/") : null;
}

// 업로드 하고 다시 페이지 호출
$fileUpload.addEventListener("click", uploadFile);