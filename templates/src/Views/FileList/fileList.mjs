import API from "/templates/src/Utils/API.mjs";

const $$fileNameCondition = document.querySelectorAll(".fileNameCondition");
const $$listAll = document.querySelectorAll(".list");

const $search = document.querySelector("#search");


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

// 클릭한 조건 확인 및 html 수정 함수
$$fileNameCondition.forEach((element) => {
	element.addEventListener('click', () => {
		const condition = element.querySelector('p').innerText;
		showFileList(condition);
	});
});

// 체크한 파일 확인 함수

// 파일 다운로드 함수

// 파일 삭제 함수

// 파일 검색 함수
const searchInputTest = (event) => {
  const text = event.target.value;
  for (let i = 0; i < fileList.length; i++) {
    if (!fileList[i].fileName.includes(text)) {
      $$listAll[i].style.display = "none";
    } else {
      $$listAll[i].style.display = "flex";
    }
  }
}

$search.addEventListener("keyup", searchInputTest);


// 페이지 이동 함수

// 페이지 뒤로가기 방지