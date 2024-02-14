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

	setColumn(htmlTag, text="") {
		htmlTag.innerHTML = "";
		if (text !== "") {
			Object.keys(this.#fileDate[0]).map((column) => {
				if (column.includes(text)) {
					htmlTag.innerHTML += `<option value="${column}">${column}</option>`
				}
			})
			return;
		};
	
		Object.keys(this.#fileDate[0]).map( (column) => {
			htmlTag.innerHTML += `<option value="${column}">${column}</option>`
		});
	}

	async setFileData() {
		const response = await API(`/files/${this.#fileTitle}/data/`, "get");
		console.log(response.data)
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