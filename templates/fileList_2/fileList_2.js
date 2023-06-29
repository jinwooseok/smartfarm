const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // csrftoken
function moveAnalystPage(event) {
    // title 내부 저장
    titleList=[];
    const $titleAll = document.querySelectorAll('#list_title');
    for (let x of $titleAll) {
        titleList.push(x.innerText);
    }
    localStorage.setItem("title_list", JSON.stringify(titleList));
    localStorage.setItem('fileTitle', JSON.stringify(event.target.innerHTML));
    event.target.href = `/analyze/${event.target.innerHTML}/`;
}

