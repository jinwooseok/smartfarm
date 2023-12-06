const $close = document.querySelector("#close"); // dialog 닫기
const $buttonContainer = document.querySelector("#buttonContainer");
const $graphContainer = document.querySelector("#graphContainer");

// 저장된 데이터를 불러옴
const ex_data = JSON.parse(document.getElementById("jsonObject").value);
let chart;

const exCount = 40 > ex_data.length ? ex_data.length : 40;
let startIndex = 0;
let lastIndex = exCount;

let graphArr = [];
let selectArr = [];

const buttonShow = (startIndex, lastIndex) => {
  if (lastIndex === ex_data.length && startIndex === 0) {
    $Prev.style.visibility = "hidden";
    $Next.style.visibility = "hidden";
  } else if (lastIndex === ex_data.length) {
    $Prev.style.visibility = "inherit";
    $Next.style.visibility = "hidden";
  } else if (startIndex === 0) {
    $Prev.style.visibility = "hidden";
    $Next.style.visibility = "inherit";
  }
};

$close.addEventListener("click", () => {
  graphArr = [];
  selectArr = [];
  $graphContainer.style.display = "none";
});

const lineDraw = (name) => {

  // alert("에러 수정 중 입니다.");
  // return;

  const showColumnName = name; // 그려줄 열 이름

  const yData = []; // y축 값 배열
  const xData = []; // x축 값 배열

  // x축 열 이름
  const xColumn =
    document.querySelector("#x_label").options[
      document.querySelector("#x_label").selectedIndex
    ].value;

  if (xColumn === "null") {
    alert("x축을 선택해 주세요");
    return;
  } else {
    xData.push(xColumn);
    selectArr.push(xColumn);
    yData.push(showColumnName);
    selectArr.push(showColumnName);
  }

  for (let i = startIndex; i < lastIndex; i++) {
    xData.push(ex_data[i][xColumn]); // x값
    yData.push(ex_data[i][showColumnName]); // y값
  }

  graphArr = [[...xData], [...yData]];

  showGraph(xColumn);
};

const showGraph = (xColumn) => {
  chart = bb.generate({
    bindto: "#myChart",
    data: {
      x: xColumn,
      type: "line",
      columns: graphArr,
    },
    axis: {
      x: {
        type: "category",
        tick: {
          rotate: 75,
          multiline: false,
          tooltip: true,
        },
      },
    },
  });

  buttonShow(startIndex, lastIndex);
};

const $Prev = document.querySelector("#Prev");
const $Next = document.querySelector("#Next");

const updateChart = (startIndex, lastIndex) => {
  graphArr = []; // 초기화
  let arr = [];

  selectArr.map((value, index) => {
    arr.push(value);
    for (let i = startIndex; i < lastIndex; i++) {
      arr.push(Number(ex_data[i][value]));
    }
    graphArr.push(arr);
    arr = [];
  });
  console.log(graphArr);
  chart.load({
    columns: graphArr,
  });
  buttonShow(startIndex, lastIndex);
};

$Next.addEventListener("click", () => {
  startIndex = startIndex + exCount;
  lastIndex =
    startIndex + exCount > ex_data.length
      ? ex_data.length
      : startIndex + exCount;
  updateChart(startIndex, lastIndex);
});

$Prev.addEventListener("click", () => {
  lastIndex = lastIndex - exCount <= exCount ? exCount : lastIndex - exCount;
  startIndex = lastIndex - exCount <= 0 ? 0 : lastIndex - exCount;

  updateChart(startIndex, lastIndex);
});
