const screenWidth = window.screen.width;
const screenHeight = window.screen.height;

export const Loading = () => {
  let Div = document.createElement('div')
  Div.id="loadingContainer"
  Div.style.cssText = `
  width:${screenWidth}px; height:${screenHeight}px; opacity:0.3; position:absolute; z-index:9000; background-color:#fff; display:block; left:0; top:0;`

  let loadingImg = "";
  loadingImg += "<div id='loadingImg'>";
  loadingImg +=
    `<img src="/templates/IMG/Spinner.gif" style='z-index:9000; display: block;  position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);'/>`;
  loadingImg += "</div>";

  Div.innerHTML=loadingImg;

  document.querySelector("body").appendChild(Div);
};

export const CloseLoading = () => {
  const $loadingContainer = document.querySelector('#loadingContainer');
  const $loadingImg = document.querySelector('#loadingImg');

  // 엘리먼트 제거
  if ($loadingContainer) {
    $loadingContainer.parentNode.removeChild($loadingContainer);
  }

  if ($loadingImg) {
    $loadingImg.parentNode.removeChild($loadingImg);
  }
};
