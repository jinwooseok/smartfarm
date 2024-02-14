import API from "/templates/src/Utils/API.mjs";
import { getFileNameList, setFileList } from "/templates/src/Utils/fileNameList.mjs";

class TimeDifferenceDataPage {
	templates() {
		return `
		<div class="explainDIV">
			예시) windowSize = 2,	count = 4, data = [1,2,3,4,5,6,7] </br>
			1 </br>
			2 </br>
			3 1 </br>
			4 2 </br>
			5 3 1 </br>
			6 4 2 </br>
			7 5 3 1

		</div>

		<div class="settingDIV">
			<div class="dateDIV">
				<span>날짜 열 이름</span>
				<select name="dateBox" id="dateBox" class="dateBox">
					<option value="null" selected></option>
				</select>
			</div>
			<div class="countDIV">
				<span>count</span>
				<input type="number" name="count" id="count" class="count" value="1">
			</div>
			<div class="windowSizeDIV">
				<span>windowSize</span>
				<input type="number" name="windowSize" id="windowSize" class="windowSize" value="1">
			</div>
		</div>

		<div class="buttonDIV" id="buttonDIV">
			<button class="save" id="save">저장</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>
		`
	}

}

export default new TimeDifferenceDataPage();