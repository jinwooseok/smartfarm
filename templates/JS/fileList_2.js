const csrftoken = $("[name=csrfmiddlewaretoken]").val(); // csrftoken

function moveAnalystPage(event) {
  event.target.href = `/analyze/${event.target.innerHTML}/`;
}
