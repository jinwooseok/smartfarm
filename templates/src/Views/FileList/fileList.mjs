import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";

const $checkAll = document.querySelector("#checkAll"); // 전체 선택 버튼
const $AllCheckBox = document.querySelectorAll(".check");

const $$fileNameCondition = document.querySelectorAll(".fileNameCondition");
const $$listAll = document.querySelectorAll(".list");

const $AllTitle = document.querySelectorAll("#AllTitle");

const $search = document.querySelector("#search");
const $delete = document.querySelector("#delete");
const $download = document.querySelector("#download");
const $logoutBtn = document.querySelector("#logoutBtn");

$logoutBtn.addEventListener("click", Logout);

let fileList = [
	{
		fileName: "예시_수정",
		lastUpdateDate: "2024-01-01",
	},
	{
		fileName: "예시_병합",
		lastUpdateDate: "2024-01-01",
	},
	{
		fileName: "예시_환경",
		lastUpdateDate: "2024-01-01",
	},
	{
		fileName: "예시_생육",
		lastUpdateDate: "2024-01-01",
	},
	{
		fileName: "예시_생산량",
		lastUpdateDate: "2024-01-01",
	},
	{
		fileName: "예시_생육_생산량_병합",
		lastUpdateDate: "2024-01-01",
	},
	{
		fileName: "예시_생육_환경_병합",
		lastUpdateDate: "2024-01-01",
	},
	{
		fileName: "예시",
		lastUpdateDate: "2024-01-01",
	},
];

// (async function () {
//   // 파일 불러오는 API
//   const response = await API("/files/", "get");
//   console.log(response);
//   fileList = response.data; // 형식 = [{fileName": ,"lastUpdateDate":}, {fileName": ,"lastUpdateDate":},]
// }());

// 파일 목록 보여주는 함수
const showFileList = (condition) => {
	// 불러온 파일을 조건에 따라 보여주기
	if (condition === "전체") {
		for (let i = 0; i < fileList.length; i++) {
			$$listAll[i].style.display = "flex";
		}
		return;
	}

	for (let i = 0; i < fileList.length; i++) {
    if (!fileList[i].fileName.includes(condition)) {
      $$listAll[i].style.display = "none";
    } else {
      $$listAll[i].style.display = "flex";
    }
  }
}

// 클릭한 조건 css 변경
const changeCss = (event) =>{
	$$fileNameCondition.forEach((div) => {
		div.style.backgroundColor = "#fff";
		div.style.color = "#000";
	});

	const clickedDiv = event.currentTarget;
	clickedDiv.style.backgroundColor = '#007A33';
	clickedDiv.style.color = '#ffffff';
}

const handleFileNameCondition = (event) =>{
	const condition = event.target.innerText;
	showFileList(condition);
	changeCss(event);
  for (let i = 0; i < $AllCheckBox.length; i++) {
    $AllCheckBox[i].checked = false;
  }
}

// 클릭한 조건 확인 및 html 수정 함수
$$fileNameCondition.forEach((element) => {
	element.addEventListener('click', handleFileNameCondition);
});

// 전체 체크
function AllCheck() {
	for (let i = 0; i < $AllCheckBox.length; i++) {
    $AllCheckBox[i].checked = this.checked;
  }
}

// 전체 선택 이벤트
$checkAll.addEventListener("change", AllCheck);

// 체크한 파일 수 확인
const getCheckedItems = () => {
  return Array.from($AllCheckBox).filter((checkbox) => checkbox.checked);
}

// 파일 다운로드 함수
const setDownloadFile = () =>{
  const DownloadFile = getCheckedItems();

  const downloadTitle = [];
  DownloadFile.map((file) => {
    downloadTitle.push(file.parentElement.childNodes[3].innerText);
  });

  if (downloadTitle.length === 0) {
    alert('파일을 선택해주세요');
    return;
  }

  return downloadTitle;
}

// download 로직, csv로
const downloadToCsv = (data, title) => {
  const jsonData = data
  let jsonDataParsing = JSON.parse(jsonData);

  let toCsv = '';
  let row="";

  for(let i in jsonDataParsing[0]){
    row += i+","; // 열 입력
  }
  row = row.slice(0,-1);
  toCsv += row +"\r\n";

  toCsv += jsonDataParsing.reduce((csv, rowObject) => {
    const row = Object.values(rowObject).join(",") + "\r\n";
    return csv + row;
  }, "");

  if (toCsv === "") {
    alert("Invalid data");
    return;
  }

  const fileName = title;
  const uri = "data:text/csv;charset=utf-8,\uFEFF" + encodeURI(toCsv);

  const link = document.createElement("a");
  link.href = uri;
  link.style.visibility = "hidden";
  link.download = fileName;

  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const clickDownloadButton = () => {
	const downloadTitle = setDownloadFile();
  console.log("downloadTitle", downloadTitle);
	downloadTitle?.map( async (title) => {
		const response = await API("/download/", "post", {data: title,});
    console.log(response, "downloadResponse");
		if(response.status === "success") {
			downloadToCsv(response.data, title);
		}
  }); 
}

$download.addEventListener("click", clickDownloadButton);


// 파일 삭제 함수
const deleteCheckedItems = async (checkedItems) => {
  const deleteList = checkedItems.map((checkbox) => {
    const index = Array.from($AllCheckBox).indexOf(checkbox);
    const title = $AllTitle[index].innerText;
    checkbox.parentElement.remove();
    return title;
	});

	const response = await API("delete/", "post", JSON.stringify(deleteList));
  console.log(response, "deleteResponse");
	if (response.status === "success") {
		location.href = "../";
	} else {
		alert("삭제 실패");
	}
}

const clickDeleteButton = () => {
  const checkedItems = getCheckedItems();
  if (!checkedItems.length) {
    alert("삭제할 파일을 선택하세요");
    return;
  }

  const yesOrNo = confirm("정말 삭제하나요?");
  if (yesOrNo) {
    deleteCheckedItems(checkedItems);
    $checkAll.checked = false;
    AllCheck();
  } else {
    alert("삭제를 취소합니다.");
  }
}

// 삭제 이벤트
$delete.addEventListener("click", clickDeleteButton);

let debounce;

// 파일 검색 함수
const searchInputTest = (event) => {
  const text = event.target.value;

  clearTimeout(debounce);

  debounce = setTimeout(() => {
    showFileList(text);
  }, 200);
  
}

$search.addEventListener("keyup", searchInputTest);

// 페이지 이동 함수

// 페이지 뒤로가기 방지
