import ShowFilePage from "./ShowFilePage.mjs";
import { reviseDefaultValue } from "/templates/src/Constant/variableList.mjs";
import responseMessage from "/templates/src/Constant/responseMessage.mjs";
import API from "/templates/src/Utils/API.mjs";

class RevisePage {

  #newData = [];
  #newDataList = [];
  #newDataObj = {};
  #checkingDuplicate = [];
	
	constructor() {
	}

  async submit(fileName, submitData) {
    console.log("var",submitData.var)
    const response = await API(`/files/${fileName}/data/farm/`, "post", submitData);
		const status = response.status || response;
    responseMessage[status] === "success" ? location.replace("/file-list/") : alert(responseMessage[status]);
  }

  templatesEasy() {
    document.querySelector('.box').classList.add("easyVersion");
    document.querySelector('.box').classList.remove("hardVersion");
    return `
    <select name="dataColumnList" id="dataColumnList" class="dataColumnList" multiple size="5">
    </select>
    <select multiple size="5">
      <option id="defaultSelect" value="temperature">온도</option>
      <option id="defaultSelect" value="humidity">습도</option>
      <option id="defaultSelect" value="co2">CO2</option>
      <option id="defaultSelect" value="insolation">일사량</option>
      <option id="defaultSelect" value="precipitation">강수량</option>
    </select>
    <button class="optionDelete" id="optionDelete">삭제</button>
    `;
  }

  templatesHard() {
    document.querySelector('.box').classList.add("hardVersion");
    document.querySelector('.box').classList.remove("easyVersion");
    return`
    <select multiple size="6">
      <option id="wordContain" value="all">전체</option>
      <option id="wordContain" value="temperature">온도</option>
      <option id="wordContain" value="humidity">습도</option>
      <option id="wordContain" value="co2">CO2</option>
      <option id="wordContain" value="insolation">일사량</option>
      <option id="wordContain" value="precipitation">강수량</option>
    </select>
    <select name="firstText" id="firstText" class="firstText" multiple size="6">
      <option value="전체">전체</option>
      <option value="주간_">주간</option>
      <option value="야간_">야간</option>
      <option value="일출부터정오_">일출부터정오</option>
      <option value="일출전후t시간_">일출전후t시간</option>
    </select>
    <select name="secondText" id="secondText" class="secondText" multiple size="6">
      <option value="평균_">평균</option>
      <option value="최소_">최소</option>
      <option value="최대_">최대</option>
      <option value="누적_">누적</option>
      <option value="DIF_">DIF</option>
      <option value="GDD_">GDD</option>
    </select>
    <select name="thirdText" id="thirdText" class="thirdText" multiple size="6">
      <!-- js를 통해 입력 -->
    </select>
    <button class="optionDelete" id="optionDelete"><i class="fa-solid fa-arrow-left"></i></button>
    <button class="optionADD" id="optionADD"><i class="fa-solid fa-arrow-right"></i></button>
    `;
  }

	templates() {
		return `
    <div class="reviseDIV">
      <div class="levelSelectDIV">
        <input type="radio" name="level" class="easy" id="easy" checked><label for="easy">쉬움</label>
        <input type="radio" name="level" class="hard" id="hard"><label for="hard">어려움</label>
      </div>
      <div class="box easyVersion">
        <select name="dataColumnList" id="dataColumnList" class="dataColumnList" multiple size="5">
        </select>
        <select multiple size="5">
          <option id="defaultSelect" value="temperature">온도</option>
          <option id="defaultSelect" value="humidity">습도</option>
          <option id="defaultSelect" value="co2">CO2</option>
          <option id="defaultSelect" value="insolation">일사량</option>
          <option id="defaultSelect" value="precipitation">강수량</option>
        </select>
        <button class="optionDelete" id="optionDelete"><i class="fa-solid fa-arrow-left"></i></button>
      </div>
    
      <div class="totalVariableDIV">
        <select name="selectedValueList" id="selectedValueList" class="selectedValueList" multiple size="5">
        </select>
      </div>

      <!-- 파일 저장 -->
      <div class="fileSaveDIV">
        <span>저장할 파일 이름</span>
        <input type="text" name="fileName" id="fileName" class="fileName"
          placeholder="저장할 파일의 이름을 입력하세요">
        <div>
          <button id="resetData">초기화</button>
        </div>
      </div>

    </div>

		<div class="buttonDIV" id="buttonDIV">
			<button class="save" id="save">저장</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>
		`
	}

  addWordContainSelectBox(event) {
    const selectValue = event.target.textContent;
    const $thirdText = document.querySelector("#thirdText");
    switch(selectValue) {
      case "전체" :
        ShowFilePage.setColumn($thirdText);
        break;
      case "온도" :
      case "기온" :
      case "습도" :
      case "CO2" :
      case "co2" :
      case "일사량" :
      case "일사" :
      case "강수량" :
        ShowFilePage.setColumn($thirdText, selectValue);
        break;
    }
  };

  #addNewObject(text1, text2, text3) {
    const objIndex = this.#newData.findIndex((obj) => Object.keys(obj).includes(text1));

    if (objIndex > -1) {
      this.#newData[objIndex][text1].push([text2, text3]);
    } else {
      this.#newDataObj = new Object();
      this.#newDataObj[text1] = [[text2, text3]];
      this.#newData.push(this.#newDataObj);
    }
  }

  #checkDuplicate(value) {
    if (this.#newDataList.includes(value)) {
      this.#checkingDuplicate.push(value);
      return false;
    }
    return !this.#newDataList.includes(value);
  }

  createEasyVersionData (event) {
    const selectedDefaultValue = event.target.textContent;
    const selectedValue = document.querySelector("#dataColumnList").options[document.querySelector("#dataColumnList").selectedIndex]?.value;
    const $selectedValueList = document.querySelector("#selectedValueList");
  
    if (selectedValue === undefined) {
      alert('왼쪽 상자에서 값을 선택해주세요');
      return;
    };
  
    for (let i=0; i<reviseDefaultValue.length; i++) {
      const defaultValue = reviseDefaultValue[i];
      const value = defaultValue.split("_");
  
      if (this.#checkDuplicate(value.join("") + selectedValue)) {
        if (selectedDefaultValue === "전체") {
          $selectedValueList.innerHTML += 
          `<Option value= '${defaultValue}${selectedValue}'>` +
            value.join("") + selectedValue +
          `</option>`;
          this.#newDataList.push(value.join("") + selectedValue);
          this.#addNewObject(selectedValue, value[0], value[1]);
        }
        if (selectedDefaultValue === "온도") {
          $selectedValueList.innerHTML += 
          `<Option value= '${defaultValue}${selectedValue}'>` +
            value.join("") + selectedValue +
          `</option>`;
          this.#newDataList.push(value.join("") + selectedValue);
          this.#addNewObject(selectedValue, value[0], value[1]);
        }
        if (
          selectedDefaultValue === "습도" ||
          selectedDefaultValue === "CO2"||
          selectedDefaultValue === "co2"
        ) {
          if (
            value[1] !== "DIF" ||
            value[1] !== "GDD" ||
            value[0] !== "일출전후2시간"
          ) {
            $selectedValueList.innerHTML += 
            `<Option value= '${defaultValue}${selectedValue}'>` +
              value.join("") + selectedValue +
            `</option>`;
            this.#newDataList.push(value.join("") + selectedValue);
            this.#addNewObject(selectedValue, value[0], value[1]);
          }
        }
        if (selectedDefaultValue === "일사량") {
          alert("미완.");
          console.log(value.join("") + selectedValue)
          break;
          // $selectedValueList.innerHTML += 
          // `<Option value= '${defaultValue}${selectedValue}'>` +
          //   value.join("") + selectedValue +
          // `</option>`;
        } 
        if (selectedDefaultValue === "강수량") {
          alert("미완.");
          break;
          // $selectedValueList.innerHTML += 
          // `<Option value= '${defaultValue}${selectedValue}'>` +
          //   value.join("") + selectedValue +
          // `</option>`;
        }
      }
    }
  
  
    if (this.#checkingDuplicate.length) {
      alert(`${this.#checkingDuplicate}은 중복 값이라 제거했습니다.`);
      this.#checkingDuplicate = [];
    }
  
  }

  #checkText(text) {
    if (text.first === "") {
      alert('처음 값을 선택해 주세요');
      return;
    };
    if (text.second === "") {
      alert('두번째 값을 선택해 주세요');
      return;
    };
    if (text.third === "") {
      alert('마지막 값을 선택해 주세요');
      return;
    };
  }

  createHardVersionData() {
    const text = {
      first: document.querySelector("#firstText").options[document.querySelector("#firstText").selectedIndex]?.textContent ,
      second: document.querySelector("#secondText").options[document.querySelector("#secondText").selectedIndex]?.textContent,
      third: document.querySelector("#thirdText").options[document.querySelector("#thirdText").selectedIndex]?.textContent,
    }
    this.#checkText(text);

    const $selectedValueList = document.querySelector("#selectedValueList");
    const value = text.first + text.second + text.third;
    if (this.#checkDuplicate(value)) {
      $selectedValueList.innerHTML += `<Option value= '${text.first}_${text.second}_${text.third}'>` + value + `</option>`;
      this.#newDataList.push(value);
      this.#addNewObject(text.third, text.first, text.second);
    };
  
    if (this.#checkingDuplicate.length) {
      alert(`${this.#checkingDuplicate}은 중복 값이라 제거했습니다.`);
      this.#checkingDuplicate = [];
    }
  }

  varDelete() {
    const $selectedValueList = document.querySelector("#selectedValueList");
    const checked = $selectedValueList.selectedOptions;
    const checkedList = Array.from(checked).map(option => option.value);

    if (checkedList) {
      for (let value of checkedList) {
        const inputValue = value.split("_");
        for (let i = 0; i < Object.keys(this.#newData).length; i++) {
          if (Object.keys(this.#newData[i])[0] === inputValue[2]) {
            for (let j = 0; j < this.#newData[i][inputValue[2]].length; j++) {
              if (
                this.#newData[i][inputValue[2]][j].includes(inputValue[0]) &&
                this.#newData[i][inputValue[2]][j].includes(inputValue[1])
              ) {
                this.#newDataList.splice(this.#newDataList.indexOf(inputValue.join("")), 1); // 배열 제거
                this.#newData[i][inputValue[2]].splice(j, 1); // 객체에서 제거
                break;
              }
            }
            if (this.#newData[i][inputValue[2]].length === 0) {
              delete this.#newData[i][inputValue[2]];
            }
          }
        }
        for (let i = checked.length - 1; i >= 0; i--) {
          const option = checked[i];
          $selectedValueList.remove(option.index);
        }
      }
    } else {
      alert("삭제할 항목을 선택하세요");
    }
  }

  setFileName(fileName) {
    const $fileName = document.querySelector('#fileName');
    const name = fileName.replace(/(.csv|.xlsx|.xls)/g, "");
    $fileName.value = name + "_수정";
  }

  resetData() {
    this.#newData = [];
    this.#newDataList = [];
    this.#newDataObj = {};
    this.#checkingDuplicate = [];
  }

  getNewData() {
    return this.#newData;
  }

}

export default new RevisePage();