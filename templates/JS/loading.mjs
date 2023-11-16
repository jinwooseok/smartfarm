const screenWidth = window.screen.width;
const screenHeight = window.screen.height;

export const Loading = () => {
  let Div = document.createElement('div')
  Div.id="loadingContainer"
  Div.style.cssText = `
  width:${screenWidth}px; height:${screenHeight}px; opacity:0.3; position:absolute; z-index:9000; background-color:#fff; display:block; left:0; top:0;
  `
  let loadingImg = "";
  loadingImg += "<div id='loadingImg'>";
  loadingImg +=
    `<img src="/templates/IMG/Spinner.gif" style='z-index:9000; display: block;  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);'/>`;
  loadingImg += "</div>";

  Div.innerHTML=loadingImg;

  document.querySelector("body").appendChild(Div);
  console.log("로딩창 열기");
};

export const CloseLoading = () => {
  document.querySelector('#loadingContainer').style.display='none'
  console.log("로딩창 닫기");
};
