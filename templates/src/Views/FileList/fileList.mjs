import API from "/templates/src/Utils/API.mjs";
import Logout from "/templates/src/Utils/Logout.mjs";
import downloadToCsv from "/templates/src/Utils/DownloadToCsv.mjs";

const $checkAll = document.querySelector("#checkAll"); // 전체 선택 버튼
const $$condition = document.querySelectorAll(".condition");
const $fileContainer = document.querySelector("#fileContainer");

const $search = document.querySelector("#search");
const $delete = document.querySelector("#delete");
const $download = document.querySelector("#download");
const $logoutBtn = document.querySelector("#logoutBtn");

$logoutBtn.addEventListener("click", Logout);

let fileList;

// 초기 파일 목록 만들기
const setFileList = () => {
  fileList.map((file) => {
    let listDiv = document.createElement('div');
    listDiv.classList.add("list");
    listDiv.style.display = "flex"
    const listChild = `
      <input type="checkbox" class="check">
      <div class="fileTitle" id="AllTitle">
        ${file.fileName}
      </div>
      <div class="lastUpdateDate" id="lastUpdateDate">
        ${file.updatedDate}
      </div>
      <div class="revise" id="revise">
      데이터 처리
      </div>
      <div class="merge" id="merge">
        파일 병합
      </div>
      <div class="analyze" id="analyze">
        데이터 분석
      </div>
      <div class="ABMS" id="ABMS">
        ABMS
      </div>
    `;

    listDiv.innerHTML = listChild;
    $fileContainer.appendChild(listDiv);
  });
};

const movePage = (id, title) => {
  localStorage.setItem("fileTitle", JSON.stringify(title));

  switch (id) {
    case "revise" :
      location.href = `/revise/${title}/`
      break;
    case "analyze" :
      location.href = `/analytics/${title}/`
      break;
    case "ABMS" :
      location.href = `/abms/${title}/`
      break;
    case "merge" :
      location.href = `/merge/`
      break;
    default :
      alert("잘못된 요청입니다.");
      break;
  }
}

// 세팅 파일에 함수 넣기
const setOnClick = () => {
  const $$revise = document.querySelectorAll("#revise");
  const $$analyze = document.querySelectorAll("#analyze");
  const $$ABMS = document.querySelectorAll("#ABMS");
  const $$merge = document.querySelectorAll("#merge");

  $$revise.forEach((element) => {
    element.addEventListener('click', () => {
      movePage(element.id, element.parentNode.childNodes[3].innerText);
    });
  });
  $$analyze.forEach((element) => {
    element.addEventListener('click', () => {
      movePage(element.id, element.parentNode.childNodes[3].innerText);
    });
  });
  $$ABMS.forEach((element) => {
    element.addEventListener('click', () => {
      movePage(element.id, element.parentNode.childNodes[3].innerText);
    });
  });
  $$merge.forEach((element) => {
    element.addEventListener('click', () => {
      movePage(element.id, element.parentNode.childNodes[3].innerText);
    });
  });
};

(async function () {
  // 파일 불러오는 API
  const response = await API("/files/", "get");
  const status = response.status;
  if (status === "success") {
    fileList = response.data;
    setFileList();
    setOnClick();
  };
}());

// 파일 목록 보여주는 함수
const showFileList = (condition) => {
  const $$listAll = document.querySelectorAll(".list");
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
const changeClickedCss = (event) =>{
	$$condition.forEach((div) => {
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
	changeClickedCss(event);

  const $AllCheckBox = document.querySelectorAll(".check");
  $checkAll.checked = false;
  for (let i = 0; i < $AllCheckBox.length; i++) {
    $AllCheckBox[i].checked = false;
  }
}

// 클릭한 조건 확인 및 html 수정 함수
$$condition.forEach((element) => {
	element.addEventListener('click', handleFileNameCondition);
});

// 전체 체크
function AllCheck() {
  const $AllCheckBox = document.querySelectorAll(".check");
  const $$listAll = document.querySelectorAll(".list");

  for (let i = 0; i < $AllCheckBox.length; i++) {
    if ($$listAll[i].style.display === "flex") {
      $AllCheckBox[i].checked = this.checked;
    }
  }
}

// 전체 선택 이벤트
$checkAll.addEventListener("change", AllCheck);

// 체크한 파일 수 확인
const getCheckedItems = () => {
  const $AllCheckBox = document.querySelectorAll(".check");
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

const clickDownloadButton = () => {
	const downloadTitle = setDownloadFile();

	downloadTitle?.map( async (title) => {
		const response = await API("/files/download/", "post", {fileName: title});
    const status = response.status;
	  return status === "success" ? downloadToCsv(response.data, title) : null;
  }); 
}

$download.addEventListener("click", clickDownloadButton);

// 파일 삭제 함수
const deleteCheckedItems = (checkedItems) => {
  const $AllCheckBox = document.querySelectorAll(".check");
  const $AllTitle = document.querySelectorAll("#AllTitle");

  const deleteList = checkedItems.map((checkbox) => {
    const index = Array.from($AllCheckBox).indexOf(checkbox);
    const title = $AllTitle[index].innerText;
    return title;
	});

  deleteList?.map( async (name) => {
    const response = await API("/files/delete/", "delete", {fileName : JSON.stringify(name)});
    const status = response.status;
  	return status === "success" ? location.replace("/file-list/") : null;
  });
}

const clickDeleteButton = () => {
  const checkedItems = getCheckedItems();
  if (!checkedItems.length) {
    alert("삭제할 파일을 선택하세요");
    return;
  }

  const yesOrNo = confirm(`파일 ${checkedItems.length}개를 삭제합니다.`);
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
    $checkAll.checked = false;
    showFileList(text);
  }, 200);
}

$search.addEventListener("keyup", searchInputTest);

// 페이지 이동 함수

// 페이지 뒤로가기 방지
