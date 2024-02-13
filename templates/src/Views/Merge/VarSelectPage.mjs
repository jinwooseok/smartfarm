import API from "/templates/src/Utils/API.mjs";

class VarSelectPage {

	#varList;

	constructor() {}

	templates() {
		const switchHtml = this.#makeVarList();
		return `
			<div class="varDIV" id="varDIV">
				<div class="varListDIV" id="varListDIV">
					${switchHtml}
				</div>
				<div class="confirmDIV" id="confirmDIV">
				</div>
			</div>
			<div class="buttonDIV" id="buttonDIV">
				<button class="nextPage" id="nextPage">다음</button>
				<button class="prevPage" id="prevPage">이전</button>
			</div>
		`
	}

	#makeVarList() {
		let html = '';

		for(let name of this.#varList.featureName) {
			html += `
				<label class="switchLabel">
					<span>${name.fileName}</span>
					<input id="switch" role="switch" type="checkbox" checked/>
				</label>
			`
		}

		return html;
	}

	makeCheckedList() {
		const list = this.#setCheckedVar();

		let html = '';

		for(let text of list) {
			html += `
				<p>${text}</p>
			`
		}

		return html;
	}

	#setCheckedVar() {
		const $$switch = document.querySelectorAll("#switch");
		const checkedVar = [];
		for (let i = 0; i < $$switch.length; i++) {
			if ($$switch[i].checked) {
				checkedVar.push($$switch[i].parentElement.childNodes[1].innerText);
			}
		}

		return checkedVar;
	}

	async setVarList(list) {
		this.#varList = list;
	}
}

export default new VarSelectPage();