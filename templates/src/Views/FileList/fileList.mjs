import API from "/templates/src/Utils/API.mjs";

const $checkAll = document.querySelector("#checkAll"); // 전체 선택 버튼
const $AllCheckBox = document.querySelectorAll(".check");

const $$fileNameCondition = document.querySelectorAll(".fileNameCondition");
const $$listAll = document.querySelectorAll(".list");

const $AllTitle = document.querySelectorAll("#AllTitle");

const $search = document.querySelector("#search");
const $delete = document.querySelector("#delete");
const $download = document.querySelector("#download");

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
// // 파일 불러오는 API
// const response = await API("files/", "get");
// console.log(response);
// fileList = response.data; // 형식 = [{fileName": ,"lastUpdateDate":}, {fileName": ,"lastUpdateDate":},]
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

// 파일 삭제 함수
const deleteCheckedItems = async (checkedItems) => {
  const deleteList = checkedItems.map((checkbox) => {
    const index = Array.from($AllCheckBox).indexOf(checkbox);
    const title = $AllTitle[index].innerText;
    checkbox.parentElement.remove();
    return title;
	});

	const response = await API("delete/", "post", JSON.stringify(deleteList));

	if (response === "success") {
		location.href = "../";
	} else {
		alert("삭제 실패");
	}
  // $.ajax({
  //   url: "delete/",
  //   type: "post",
  //   dataType: "json",
  //   headers: { "X-CSRFToken": csrftoken },
  //   data: { data: JSON.stringify(deleteList) },
  //   success: function (response) {
  //     if (response.data != null) {
  //       location.href = "../";
  //     }
  //   },
  //   error: function (xhr, error) {
  //     alert("에러입니다.");
  //     console.error("error : " + error);
  //   }
  // });
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

// 파일 검색 함수
const searchInputTest = (event) => {
  const text = event.target.value;
	showFileList(text);
}

$search.addEventListener("keyup", searchInputTest);

// 페이지 이동 함수

// 페이지 뒤로가기 방지
