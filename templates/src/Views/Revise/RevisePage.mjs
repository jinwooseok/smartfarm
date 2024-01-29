import API from "/templates/src/Utils/API.mjs";

// 페이지 디자인 하기 
/*
<!-- 엑셀 기준 열 지정 및 주기 선택 -->
        <div class="variablesContainer">
          <input type="radio" name="level" class="easy" id="easy" checked><label for="easy">쉬움</label>
          <div class="box easyVersion">
            <select name="dataColumnList" id="dataColumnList" class="dataColumnList" multiple size="5">
            </select>
            <select name="defaultSelect" id="defaultSelect" class="defaultSelect" multiple size="5">
              <option value="temperature">온도</option>
              <option value="humidity">습도</option>
              <option value="co2">CO2</option>
              <option value="insolation">일사량</option>
              <option value="precipitation">강수량</option>
            </select>
            <button class="optionDelete" id="optionDelete">삭제</button>
          </div>

          <input type="radio" name="level" class="hard" id="hard"><label for="hard">어려움</label>
          <div class="box hardVersion">
            <select name="wordContain" id="wordContain" class="wordContain" multiple size="6">
              <option value="all">전체</option>
              <option value="temperature">온도</option>
              <option value="humidity">습도</option>
              <option value="co2">CO2</option>
              <option value="insolation">일사량</option>
              <option value="precipitation">강수량</option>
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
            <button class="optionDelete" id="optionDelete">삭제</button>
            <button class="optionSelect" id="optionSelect">이동</button>
          </div>
        </div>

        <div class="totalVariableContainer">
          <select name="selectedValueList" id="selectedValueList" class="selectedValueList" multiple size="5">
          </select>
        </div>

      </div>
 */
class RevisePage {

	#reviseInfo ={}
	
	constructor() {
	}

	templates() {
		return `
    <div class="fileSaveDIV">
      <span>저장할 파일 이름</span>
      <input type="text" name="fileName" id="fileName" class="fileName"
      placeholder="저장할 파일의 이름을 입력하세요">
    </div>


		<div class="buttonDIV" id="buttonDIV">
			<button class="nextPage" id="nextPage">다음</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>
		`
	}

}

export default new RevisePage();