import Excel from "/templates/JS/Utils/Excel.mjs";
import Loading from "/templates/JS/Utils/Loading.mjs";

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
}

const moveSelectedFileTitle = () => {

}