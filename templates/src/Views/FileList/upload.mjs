import API from "/templates/src/Utils/API.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";

const $uploadDialog = document.querySelector("#uploadDialog");
const $upload = document.querySelector("#upload");
const $fileUpload = document.querySelector("#fileUpload");
const $closeUploadPopup = document.querySelector("#closeUploadPopup");

const $fileUploadDrag = document.querySelector("#fileUploadDrag");
const $fileUploadInput = document.querySelector("#fileUploadInput");
const $fileIcon = document.querySelector("#fileIcon");
const $fileName = document.querySelector("#fileName");

// 파일 업로드 버튼 팝업창 관리 함수
$upload.addEventListener("click", () => {
	$uploadDialog.style.display = "flex";
	$uploadDialog.showModal();
})

$closeUploadPopup.addEventListener("click", () => {
  $uploadDialog.style.display = "none";
  $uploadDialog.close();
});

let selectedFile;
let sheetData = "";

const fileSetting = () => {
  $fileIcon.style.display = "none";
  // $fileUploadDrag.style.display = "none";
  $fileName.value = selectedFile.name.replace(/\s/g, "_");
}

const readXlsxFileContent = (file) => {
  const reader = new FileReader();

  Loading.StartLoading();

  reader.onload = function (event) {
    const fileContent =  event.target.result;
    const workbook = XLSX.read(fileContent, { type: "binary" });
    sheetData = XLSX.utils.sheet_to_row_object_array(workbook.Sheets[workbook.SheetNames[0]]);
    Loading.CloseLoading();
  };

  reader.onerror = function (event) {
    console.error(event.target.error);
    Loading.CloseLoading();
  };

  reader.readAsBinaryString(file);
}

const readCsvFileContent = (file) => {
  const reader = new FileReader();
  Loading.StartLoading();

  reader.onload = function (event) {
    const fileContent =  event.target.result;
    sheetData = parseCSV(fileContent);
    Loading.CloseLoading();
  };

  reader.onerror = function (event) {
    console.error(event.target.error);
    Loading.CloseLoading();
  };

  reader.readAsText(file, 'EUC-KR');
}

const parseCSV = (csvContent) => {
  const lines = csvContent.split('\n');
  const result = [];
  
  // 첫 줄을 헤더로 사용
  const headers = lines[0].split(',');

  // 나머지 줄 처리
  for (let i = 1; i < lines.length - 1; i++) {
    const values = lines[i].split(',');
    const entry = {};
    headers.forEach((header, index) => {
      entry[header] = values[index];
    });
    result.push(entry);
  }

  return result;
}

$fileUploadInput.addEventListener("change", (event) => {
  selectedFile = event.target.files[0];
  if (!selectedFile) {
    return;
  }
  showFile();
});

$fileUploadDrag.addEventListener("dragenter", (event) => {
  event.preventDefault();
  $fileUploadDrag.style.backgroundColor = "#999";
});

$fileUploadDrag.addEventListener("dragleave", (event) => {
  event.preventDefault();
  $fileUploadDrag.style.backgroundColor = "";
});

$fileUploadDrag.addEventListener("drop", (event) => {
  event.preventDefault();
  selectedFile = event.dataTransfer.files[0];
  showFile();
});

const showFile = () => {
  fileSetting();
  if (
    $fileName.value.toLowerCase().includes("xls") ||
    $fileName.value.toLowerCase().includes("xlsx") 
  ) {
    readXlsxFileContent(selectedFile);
    return;
  }

  if ($fileName.value.toLowerCase().includes("csv")) {
    readCsvFileContent(selectedFile);
    return;
  }
}


// 파일 업로드
const uploadFile = async () => {
	const data = {
		fileName: $fileName.value,
		fileData: JSON.stringify(sheetData),
	};

  console.log(sheetData[0]);
  console.log(sheetData[sheetData.length-1]);

	const response = await API("/files/save/", "post" , data);

  checkResponse(response);
  
}

const checkResponse = (code) => {
  switch(code) {
    case code.status === "success":
      location.replace("/file-list/");
      break;
    case 401 :
      alert("로그인이 필요합니다.");
      location.replace("/users/sign-in/");
      break;
    case 452 :
        alert("DB에 파일이 존재하지 않습니다.");
        break;
    case 454 :
      alert("파일 저장에 실패하였습니다.");
      break;
    case 456 :
      alert("데이터를 csv로 변환할 수 없습니다.");
      break;
  }
}

// 업로드 하고 다시 페이지 호출
$fileUpload.addEventListener("click", uploadFile);


// 파일 업로드 함수
