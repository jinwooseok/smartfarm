
// download 로직, csv로
const downloadToCsv = (data, title) => {
  const jsonData = data;

  let toCsv = '';
  let row="";

  for(let i in jsonData[0]){
    row += i+","; // 열 입력
  }
  row = row.slice(0,-1);
  toCsv += row +"\r\n";

  toCsv += jsonData.reduce((csv, rowObject) => {
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

export default downloadToCsv;