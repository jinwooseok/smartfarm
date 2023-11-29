function moveAnalystPage(event) {
  localStorage.setItem("fileTitle", JSON.stringify(event.target.innerHTML));
  event.target.href = `/analyze/${event.target.innerHTML}/`;
}