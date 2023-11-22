const $checkAll = document.querySelector("#checkAll"); // 전체 선택 버튼
const $AllCheckBox = document.querySelectorAll(".check");

// 버튼
const $delete = document.querySelector("#delete");
const $AllTitle = document.querySelectorAll("#AllTitle");
const $listAll = document.querySelectorAll(".list");
const $search = document.querySelector("#search");

//토큰
const csrftoken = $("[name=csrfmiddlewaretoken]").val(); // csrftoken

// 전체 선택
function setAllCheckStatus(status) {
  for (let i = 0; i < $AllCheckBox.length; i++) {
    $AllCheckBox[i].checked = status;
  }
}

function AllCheck() {
  setAllCheckStatus(this.checked);
}

function getCheckedItems() {
  return Array.from($AllCheckBox).filter((checkbox) => checkbox.checked);
}

function deleteCheckedItems(checkedItems) {
  const deleteList = checkedItems.map((checkbox) => {
    const index = Array.from($AllCheckBox).indexOf(checkbox);
    const title = $AllTitle[index].innerText;
    checkbox.parentElement.remove();
    return title;
  });
  $.ajax({
    url: "delete/",
    type: "post",
    dataType: "json",
    headers: { "X-CSRFToken": csrftoken },
    data: { data: JSON.stringify(deleteList) },
    success: function (response) {
      if (response.data != null) {
        location.href = "../";
      }
    },
    error: function (xhr, error) {
      alert("에러입니다.");
      console.error("error : " + error);
    }
  });
}

function clickDeleteButton() {
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

// 전체 선택 이벤트
$checkAll.addEventListener("change", AllCheck);

// 검색용 저장
const titleList = [];
for (let title of $AllTitle) {
  titleList.push(title.innerText);
}

$search.addEventListener("keyup", (event) => {
  let text = event.target.value;
  for (let i = 0; i < titleList.length; i++) {
    if (!titleList[i].includes(text)) {
      $listAll[i].style.display = "none";
    } else {
      $listAll[i].style.display = "flex";
    }
  }
});

// 파일 클릭
function moveRevisePage(event) {
  localStorage.setItem("title_list", JSON.stringify(titleList)); // 로컬에 저장
  localStorage.setItem("fileTitle", JSON.stringify(event.target.innerHTML));
  location.href = `/revise/${event.target.innerHTML}/`;
}

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

// 다운로드 버튼
const $download = document.querySelector("#download");
$download.addEventListener("click", () => {
  
  const downloadTitle = setDownloadFile();

  downloadTitle?.map((title) => {
    $.ajax({
      url: "/download/",
      type: "post",
      dataType: "json",
      headers: { "X-CSRFToken": csrftoken },
      data: {
        data: title,
      },
      async :false,
      success: function (response) {
        if (response.data != null) {
          download(response.data, title);
        }
      },
      error: function (xhr, error) {
        alert("에러입니다.");
        console.error("error : " + error);
      },
    });
  }); 
});

// download 로직, csv로
const download = function (data, title) {
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