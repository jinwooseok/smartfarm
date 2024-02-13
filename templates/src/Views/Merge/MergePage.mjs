import API from "/templates/src/Utils/API.mjs";
import Excel from "/templates/src/Model/Excel.mjs";

class MergePage {

	#fileDate;

	templates() {
		return `
		<div class="selectDIV">
			<div class="card">
				<p class="cardTitle">생육</p>
				<select name="growthSelectBox" id="growthSelectBox" class="growthSelectBox">
					<option value="null" selected></option>
				</select>
				<select name="growthVariable" id="growthVariable" class="growthVariable">
				</select>
			</div>

			<div class="card">
				<p class="cardTitle">환경</p>
				<select name="environmentSelectBox" id="environmentSelectBox" class="environmentSelectBox">
					<option value="null" selected></option>
				</select>
				<select name="environmentVariable" id="environmentVariable" class="environmentVariable">
				</select>
			</div>

			<div class="card">
				<p class="cardTitle">생산량</p>
				<select name="outputSelectBox" id="outputSelectBox" class="outputSelectBox">
					<option value="null" selected></option>
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
			<button class="nextPage" id="nextPage" >다음</button>
		</div>
		`
	}

	inputValueToSelectBox(list) {
		const $selectBoxes = {
			growth: document.querySelector("#growthSelectBox"),
			environment: document.querySelector("#environmentSelectBox"),
			output: document.querySelector("#outputSelectBox"),
		};

		list.map( (title) => {
			$selectBoxes.growth.innerHTML += `<Option value='${title.fileName}'>` + title.fileName + `</option>`;
			$selectBoxes.environment.innerHTML += `<Option value='${title.fileName}'>` + title.fileName + `</option>`;
			$selectBoxes.output.innerHTML += `<Option value='${title.fileName}'>` + title.fileName + `</option>`;
		});
	}

	async getFileVarList (name) {
		const response = await API(`/files/${name}/data/feature/` ,"get");
		return response.data;
	};

	async #handleChangeUpdateVarOptions ($selectBox, $variable, index) {
		$variable.innerHTML = "";

		const title = $selectBox.options[$selectBox.selectedIndex].textContent;
		if (title === '') {
			$variable.innerHTML = "";
			return;
		}
		
		const data = await this.getFileVarList(title);
		for (let column of data) {
			$variable.innerHTML += `<Option value='${column.featureName}'>${column.featureName}</option>`;
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
				this.#handleChangeUpdateVarOptions($selectBox, Object.values($variables)[index], index);
			});
		});
	}

	#setMergeVarList() {
		const $variables = {
			growth: document.querySelector("#growthVariable"),
			environment: document.querySelector("#environmentVariable"),
			output: document.querySelector("#outputVariable"),
		};

		const $variableSelectBoxes = [$variables.growth, $variables.environment, $variables.output];

		const columnName = $variableSelectBoxes
			.map($selectBox => $selectBox.options[$selectBox.selectedIndex]?.value)
			.filter(title => title !== undefined);
	
		return columnName;
	}

	#setMergeFileName() {
		const $selectBoxes = {
			growth: document.querySelector("#growthSelectBox"),
			environment: document.querySelector("#environmentSelectBox"),
			output: document.querySelector("#outputSelectBox"),
		};

		const $nameSelectBoxes = [$selectBoxes.growth, $selectBoxes.environment, $selectBoxes.output];

		const nameList = $nameSelectBoxes
			.map($selectBox => $selectBox.options[$selectBox.selectedIndex]?.value)
			.filter(title => title !== "null");
	
		return nameList;
	}

	async mergeData() {
		const columnsToMerge = this.#setMergeVarList();
		const namesToMerge = this.#setMergeFileName();

		const data = {
			mergeDataNames : JSON.stringify(namesToMerge),
			mergeStandardVarList : JSON.stringify(columnsToMerge),
		}

		const response = await API("/merge/", "post", data);
		const returnData = Object.values(response.data);
		this.#setFileData(returnData[0]);
	}

	#setFileData(data) {
		this.#fileDate = data;
	}

	showFile(element) {
		element.innerHTML = "";
		new Excel(this.#fileDate, element);
	}

	getFileData() {
		return this.#fileDate;
	}
}

export default new MergePage();