import API from "/templates/src/Utils/API.mjs";
import Excel from "/templates/src/Model/Excel.mjs";

class ShowFilePage {

	#fileTitle;
	#fileDate;
	
	constructor() {
	}

	templates() {
		return `
		<div class="spreadSheetDIV" id="spreadSheetDIV">
		</div>

		<div class="settingDIV">
			<div class="dateDIV">
				<span>날짜 열</span>
				<input type="text" name="date" id="date" class="date" value="1">
			</div>

			<div class="startDIV">
				<span>처리 시작 행</span>
				<input type="text" name="startIndex" id="startIndex" class="startIndex" value="1">
			</div>

			<div class="periodSelectDIV">
				<span>주기 선택</span>
				<div class="radioDIV" id="periodDIV">
					<input type="radio" name="period" id="daily" value="daily" checked><label for="daily">일간</label>
					<input type="radio" name="period" id="weekly" value="weekly"><label for="weekly">주간</label>
					<input type="radio" name="period" id="else" value="else"><label for="else">기타</label>
				</div>
				<input type="text" id="elsePeriod" class="elsePeriod" disabled>
			</div>

			<div class="typeSelectDIV">
				<span>종류 선택</span>
				<div class="radioDIV" id="typeDIv">
					<input type="radio" name="type" id="env" value="env" checked><label for="env">환경</label>
					<input type="radio" name="type" id="growth" value="growth"><label for="growth">생육</label>
					<input type="radio" name="type" id="output" value="output"><label for="output">생산량</label>
				</div>
			</div>
		</div>	

		<div class="buttonDIV" id="buttonDIV">
			<button class="nextPage setting" id="nextPage">다음</button>
		</div>
		`
	}

	async setFileData() {
		const response = await API(`/files/${this.#fileTitle}/data/`, "get");
		this.#fileDate = response.data;
	}

	showFile(element) {
		element.innerHTML = "";
		new Excel(this.#fileDate, element);
	}

	setFileTitle(fileName) {
		this.#fileTitle = fileName;
	}

	getFileTitle() {
		return this.#fileTitle;
	}

	getFileDate() {
		return this.#fileDate;
	}
}

export default new ShowFilePage();