import setFileListSelectBox from "/templates/src/Utils/setFileListSelectBox.mjs";
import API from "/templates/src/Utils/API.mjs";
import Excel from "/templates/src/Model/Excel.mjs";

class MergePage {

	#mergeDataList;
	#fileDate;
	#fileTitle

	templates() {
		return `
		<div class="selectDIV">
			<div class="card">
				<p class="cardTitle">생육</p>
				<select name="growthSelectBox" id="growthSelectBox" class="growthSelectBox">
				</select>
				<select name="growthVariable" id="growthVariable" class="growthVariable">
				</select>
			</div>

			<div class="card">
				<p class="cardTitle">환경</p>
				<select name="environmentSelectBox" id="environmentSelectBox" class="environmentSelectBox">
				</select>
				<select name="environmentVariable" id="environmentVariable" class="environmentVariable">
				</select>
			</div>

			<div class="card">
				<p class="cardTitle">생산량</p>
				<select name="outputSelectBox" id="outputSelectBox" class="outputSelectBox">
				</select>
				<select name="outputVariable" id="outputVariable" class="outputVariable">
				</select>
			</div>

			<div class="card">
				<p class="cardTitle">결과 확인</p>
				<input type="text" name="mergeFileName" class="mergeFileName" id="mergeFileName" placeholder="파일 이름을 정해주세요.">
				<button class="merge" id="merge">병합하기</button>
			</div>
		</div>

		<div class="spreadSheetDIV" id="spreadSheetDIV">
		</div>

		<div class="buttonDIV" id="buttonDIV">
			<button class="nextPage" id="nextPage">다음</button>
		</div>
		`
	}

	inputSelectBoxValue(list) {
		const $selectBoxes = {
			growth: document.querySelector("#growthSelectBox"),
			environment: document.querySelector("#environmentSelectBox"),
			output: document.querySelector("#outputSelectBox"),
		};
		list.map( (title) => {
			$selectBoxes.growth.innerHTML += `<Option value= '${title.fileName}' selected>` + title.fileName + `</option>`;
			$selectBoxes.environment.innerHTML += `<Option value= '${title.fileName}' selected>` + title.fileName + `</option>`;
			$selectBoxes.output.innerHTML += `<Option value= '${title.fileName}' selected>` + title.fileName + `</option>`;
		});
	}

	async #postFilename (name) {
		const response = await API(`files/${name}/data/feature/` ,"get");
		console.log("postFIleName", response);
	};

	async #updateVariableOptions ($selectBox, $variable, index) {
		$variable.innerHTML = "";
		const title = $selectBox.options[$selectBox.selectedIndex].textContent;
	
		if (title === '') {
			$variable.innerHTML = "";
			this.#mergeDataList[index] = '';
			return;
		}
		
		console.log(title);
		const data = await this.#postFilename(title);
		this.#mergeDataList[index] = data;

		const dataColumn = Object.keys(JSON.parse(data)[0]);
		for (let column of dataColumn) {
			$variable.innerHTML += `<Option value='${column}'>${column}</option>`;
		}
	}

	setEventListener() {
		const $selectBoxes = {
			growth: document.querySelector("#growthSelectBox"),
			environment: document.querySelector("#environmentSelectBox"),
			output: document.querySelector("#outputSelectBox"),
		};
		
		const $variables = {
			growth: document.querySelector("#growthVariable"),
			environment: document.querySelector("#environmentVariable"),
			output: document.querySelector("#outputVariable"),
		};

		Object.values($selectBoxes).forEach(($selectBox, index) => {
			$selectBox.addEventListener("change", () => {
				this.#updateVariableOptions($selectBox, Object.values($variables)[index], index);
			});
		});
	}

	#setMergeVariable() {
		const $variableSelectBoxes = [$variables.growth, $variables.environment, $variables.output];

		const columnName = $variableSelectBoxes
			.map($selectBox => $selectBox.options[$selectBox.selectedIndex]?.value)
			.filter(title => title !== "null");
	
		return columnName;
	}

	async sendMergeInfo() {
		const columnName = this.#setMergeVariable();

		const data = {
			fileName: this.#fileTitle,
			columnName: JSON.stringify(columnName),
		}

		const response = await API("/merge/", "post", data);
		console.log("sendMergeInfo", response);
	}

	setFileTitle(fileName) {
		this.#fileTitle = fileName;
		console.log(fileName);
	}

	async setFileData() {
		const response = await API(`/files/${this.#fileTitle}/data/`, "get");
		this.#fileDate = response.data;
	}

	showFile(element) {
		element.innerHTML = "";
		new Excel(this.#fileDate, element);
	}
}

export default new MergePage();