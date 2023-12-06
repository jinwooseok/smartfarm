const csrftoken = $("[name=csrfmiddlewaretoken]").val(); // csrftoken

const data = JSON.parse(document.getElementById("jsonObject").value);
const dataColumn = Object.keys(data[0]);

// 분석
const $normalization = document.querySelector("#normalization");
const $analyzeValue_x = document.querySelector("#analyzeValue_x");
const $selectedValue_X = document.querySelector("#selectedValue_X");
const $selectedValue_Y = document.querySelector("#selectedValue_Y");
const $analyzeMoveX = document.querySelector("#analyzeMoveX");
const $analyzeDeleteX = document.querySelector("#analyzeDeleteX");
const $analyzeBtn = document.querySelector("#analyze");
const $technique = document.querySelector("#technique");
const $analyze_result = document.querySelector("#analyze-result");

// 그래프 //
const $graphAdd = document.querySelector("#graphAdd");
const $graphDelete = document.querySelector("#graphDelete");
const $dataSelectBox = document.querySelector("#dataSelectBox");
const $graphValueSelectBox = document.querySelector("#graphValueSelectBox");
const $graphDown = document.querySelector("#graphDown");
const $graphContainer = document.querySelector("#graphContainer");

window.onload = () => {
  for (let x of dataColumn) {
    // x=x.replace(' ','');
    $analyzeValue_x.innerHTML += `<option value=${x}>${x}</option>`;
    $selectedValue_Y.innerHTML += `<option value=${x}>${x}</option>`;
    $dataSelectBox.innerHTML += `<option value=${x}>${x}</option>`;
    $graphValueSelectBox.innerHTML += `<option value=${x}>${x}</option>`;
  }
};

/////////////////////////////////////
const xValueArr = []; // 선택한 x값 배열
let normalizationValue;

// 정규화 선택
$normalization.addEventListener("click", (event) => {
  normalizationValue = event.target.value;
});

// 선택한 x값 이동
$analyzeMoveX.addEventListener("click", () => {
  let checked = document.querySelectorAll("#analyzeValue_x :checked");
  let selected = [...checked].map((option) => option.textContent);

  for (let x of selected) {
    $selectedValue_X.innerHTML += `<option value=${x}>${x}</option>`;
    xValueArr.push(x);
  }
});

// x값 삭제
$analyzeDeleteX.addEventListener("click", () => {
  let checked = document.querySelectorAll("#selectedValue_X :checked");
  let selected = [...checked].map((option) => option.textContent);

  for (let x of selected) {
    $(`#selectedValue_X option[value='${x}']`).remove();
    xValueArr.splice(xValueArr.indexOf(x), 1);
  }
});

$analyzeBtn.addEventListener("click", () => {
  $analyze_result.style.display = "block";

  $.ajax({
    url: `/analyze/${JSON.parse(localStorage.getItem("fileTitle"))}/stat`,
    type: "get",
    dataType: "json",
    data: {
      xValue: JSON.stringify(xValueArr), //x 값 배열임
      yValue:
        $selectedValue_Y.options[$selectedValue_Y.selectedIndex].textContent, //y 값
      technique: $technique.options[$technique.selectedIndex].textContent, // 분석 종류
      scaler: normalizationValue, // 정규화 종류
    },
    success: function (response) {
      if (response.data != null) {
        $analyze_result.innerHTML = response.data; // 결과 창 html
      }
    },
    error: function (xhr, error) {
      alert("에러입니다.");
      console.error("error : " + error);
    },
  });
});

/////////////////////////////////////

let chart; // 그래프
let graphArr = []; // 사용한 변수
let selectArr = []; // 업데이트용 y열 이름만 보관 ["열 이름","열 이름", "열 이름", ..]

// 특수 문자 및 공백 제거 정규 표현식
const reg = /[`~!@#$%^&*()_|+\-=?;:'",.<>\{\}\[\]\\\/ ]/gim;

const $buttonContainer = document.querySelector("#buttonContainer");
const $SelectedDate = document.querySelector("#SelectedDate");

let exCount = 90 > data.length ? data.length : 90;
let startIndex = 0;
let lastIndex = exCount;

const buttonShow = (startIndex, lastIndex) => {
  if (lastIndex === data.length && startIndex === 0) {
    $Prev.style.visibility = "hidden";
    $Next.style.visibility = "hidden";
  } else if (lastIndex === data.length) {
    $Prev.style.visibility = "inherit";
    $Next.style.visibility = "hidden";
  } else if (startIndex === 0) {
    $Prev.style.visibility = "hidden";
    $Next.style.visibility = "inherit";
  }
};

// 그래프 보여주기
$graphAdd.addEventListener("click", () => {
  $graphContainer.style.display = "block";

  let xText = $dataSelectBox.options[$dataSelectBox.selectedIndex].value;
  let yText =
    $graphValueSelectBox.options[$graphValueSelectBox.selectedIndex].value;

  // 날짜 열 생성
  for (let i = 0; i < data.length; i++) {
    $SelectedDate.innerHTML += `<option value=${data[i][xText]}>${data[i][xText]}</option>`;
  }

  // x축 선택 필수
  if (xText === "notSelect") {
    alert("날짜를 선택하세요");
    return;
  }

  let arr = []; // 데이터 배열
  // ["열 이름", data...]

  $buttonContainer.style.display = "flex"; // 화살표 생성

  // 맨 처음 그림 -> 그냥 다 넣는다.
  if (graphArr.length === 0) {
    // x값 설정
    arr.push(xText);
    selectArr.push(xText);
    for (let i = startIndex; i < lastIndex; i++) {
      if (reg.test(data[i][xText])) {
        arr.push(Number(data[i][xText].replace(reg, "")));
      } else {
        arr.push(Number(data[i][xText]));
      }
    }
    graphArr.push(arr);
    arr = [];
    //y값
    arr.push(yText);
    selectArr.push(yText);
    for (let i = startIndex; i < lastIndex; i++) {
      arr.push(Number(data[i][yText]));
    }
    graphArr.push(arr);
    chart = bb.generate({
      bindto: "#chart",
      data: {
        x: xText,
        type: "line",
        columns: graphArr,
      },
      zoom: {
        enabled: true, // for ESM specify as: zoom()
        type: "drag",
      },
      axis: {
        x: {
          type: "category",
          tick: {
            rotate: 75,
            multiline: false,
            tooltip: true,
          },
          //height: 130
        },
      },
    });
  } else {
    // 데이터 추가
    if (selectArr.includes(yText)) {
      return;
    }
    arr.push(yText);
    selectArr.push(yText);
    for (let i = startIndex; i < lastIndex; i++) {
      arr.push(Number(data[i][yText]));
    }
    graphArr.push(arr);
    chart.load({
      columns: graphArr,
    });
  }
console.log(graphArr)
  buttonShow(startIndex, lastIndex);
});

document.querySelector("#graphType").addEventListener("click", () => {
  let type =
    document.querySelector("#graphType").options[
      document.querySelector("#graphType").selectedIndex
    ].value;
  chart.load({
    type: type,
    columns: graphArr,
  });
});

$graphDelete.addEventListener("click", () => {
  let yText =
    $graphValueSelectBox.options[$graphValueSelectBox.selectedIndex].value;
  chart.unload({
    ids: yText,
  });

  graphArr.splice(graphArr.indexOf(yText), 1);
  selectArr.splice(selectArr.indexOf(yText), 1);
});

$graphDown.addEventListener("click", () => {
  chart.export(
    {
      // width: 800,
      // height: 600,
      // preserveAspectRatio: false,
      // preserveFontStyle: false,
      mimeType: "image/png",
    },
    (dataUrl) => {
      const link = document.createElement("a");

      link.download = `${JSON.parse(localStorage.getItem("fileTitle"))}.png`;
      link.href = dataUrl;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  );
});

const $Prev = document.querySelector("#Prev");
const $Next = document.querySelector("#Next");

const updateChart = (startIndex, lastIndex) => {
  graphArr = []; // 초기화

  let arr = [];
  arr.push(selectArr[0]);
  for (let i = startIndex; i < lastIndex; i++) {
    if (reg.test(data[i][selectArr[0]])) {
      arr.push(Number(data[i][selectArr[0]].replace(reg, "")));
    } else {
      arr.push(Number(data[i][selectArr[0]]));
    }
  }
  graphArr.push(arr);
  arr = [];

  selectArr.map((value, index) => {
    if (index !== 0) {
      arr.push(value);
      for (let i = startIndex; i < lastIndex; i++) {
        arr.push(Number(data[i][value]));
      }
      graphArr.push(arr);
      arr = [];
    }
  });

  buttonShow(startIndex, lastIndex);

  chart.load({
    columns: graphArr,
  });
};

$Next.addEventListener("click", () => {
  startIndex = startIndex + exCount;
  lastIndex =
    startIndex + exCount > data.length ? data.length : startIndex + exCount;

  updateChart(startIndex, lastIndex);
});

$Prev.addEventListener("click", () => {
  lastIndex = lastIndex - exCount <= exCount ? exCount : lastIndex - exCount;
  startIndex = lastIndex - exCount <= 0 ? 0 : lastIndex - exCount;

  updateChart(startIndex, lastIndex);
});

$SelectedDate.addEventListener("change", () => {
  startIndex = $SelectedDate.options[$SelectedDate.selectedIndex].index;
  lastIndex =
    startIndex + exCount > data.length ? data.length : startIndex + exCount;

  updateChart(startIndex, lastIndex);
});
