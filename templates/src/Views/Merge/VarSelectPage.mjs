class VarSelectPage {

	#varList;
	#selectedVarList = [];

	constructor() {}

	templates() {
		const switchHtml = this.#makeVarListDIV();
		return `
			<div class="varDIV" id="varDIV">
				<div class="varListDIV" id="varListDIV">
					${switchHtml}
				</div>
				<div class="confirmDIV" id="confirmDIV">
				</div>
			</div>
			<div class="buttonDIV" id="buttonDIV">
				<button class="nextPage switchComplete" id="nextPage">다음</button>
				<button class="prevPage" id="prevPage">이전</button>
			</div>
		`
	}

	#makeVarListDIV() {
		let html = '';

		// for(let name of this.#varList.featureName) {
		// 	html += `
		// 		<label class="switchLabel">
		// 			<span>${name.fileName}</span>
		// 			<input id="switch" role="switch" type="checkbox" checked/>
		// 		</label>
		// 	`
		// }

		const testList = ["123","456","789","asdsdf","assdfd","assdfasd","aswed","asewrd","aq12sd","adsfsd","aafdssd","aaaaasd"]
		for(let name of testList) {
			html += `
				<label class="switchLabel">
					<span>${name}</span>
					<input id="switch" role="switch" type="checkbox" checked/>
				</label>
			`
		}

		return html;
	}

	makeCheckedListDIV() {
		const list = this.#setCheckedVarList();

		let html = '';

		for(let text of list) {
			html += `
				<p>${text}</p>
			`
		}

		return html;
	}

	#setCheckedVarList() {
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