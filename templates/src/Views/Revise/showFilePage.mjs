import API from "/templates/src/Utils/API.mjs";
import Excel from "/templates/src/Model/Excel.mjs";

class ShowFilePage {

	#fileTitle;
	#fileDate;
	
	constructor () {
	}

	templates() {
		return `
		<div class="spreadSheetDIV" id="spreadSheetDIV">
		</div>

		<div class="buttonDIV" id="buttonDIV">
			<button class="next" id="next">다음</button>
			<button class="prev" id="prev">이전</button>
		</div>
		`
	}

	async setFileData() {
		const response = await API(`/files/${this.#fileTitle}/data/`, "get");
		this.#fileDate = response.data;
	}

	showFile (element) {
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