import API from "/templates/src/Utils/API.mjs";

class VarPage {
	#fileFeatureInfo = ""; // 파일 변수 중요도 및 특징 겍체
	#featureNameList = []; // 파일 변수 이름 목록
	#fileData = "";

	templates() {
		return `
		<div class="rowDIV">
			<div class="variableDIV">
				<div class="columnList">
					<div class="featureName">
						변수 이름
					</div>
					<div class="featureType" id="featureType">
						변수 타입
					</div>
					<div class="featureImportance" id=	"featureImportance">
						변수 중요도
					</div>
					<div class="switchDIV" id="switchDIV">
						선택
					</div>
				</div>
				<div class="listDIV" id="listDIV">
			
				</div>
			</div>

			<div class="fieldsetDIV">
				<fieldset class="yDIV">
					<legend>y 값</legend>
					<select name="yValue" id="yValue" class="yValue">
					</select>
				</fieldset>

				<div class="timeDIV">
					<fieldset class="timeDiffDIV">
						<legend>시차 변수 선택</legend>
						<div class="timeDiffUseDIV" id="timeDiffUseDIV">
							<input type="radio" name="time" id="not" value="not" checked><label for="not">사용 x</label>
							<input type="radio" name="time" id="use" value="use"><label for="use">사용</label>
						</div>
						</select>
					</fieldset>
				</div>
			</div>
		</div>

		<div class="buttonDIV" id="buttonDIV">
			<button class="nextPage" id="nextPage">다음</button>
		</div>
		`
	}

	onClickTimeDIff(id) {
		if (id === "use") {
			return `
			<fieldset class="timeDiffDIV">
				<legend>시차 변수 선택</legend>
				<div class="timeDiffUseDIV" id="timeDiffUseDIV">
					<input type="radio" name="time" id="not" value="not"><label for="not">사용 x</label>
					<input type="radio" name="time" id="use" value="use" checked><label for="use">사용</label>
				</div>
			</fieldset>

			<fieldset class="countDIV">
				<legend>count</legend>
				<input type="number" name="count" class="count" id="count" value="1">
			</fieldset>

			<button class="timeDiffBtn" id="timeDiffCreate">시차변수 생성</button>
			`
		}
		return `
		<fieldset class="timeDiffDIV">
			<legend>시차 변수 선택</legend>
			<div class="timeDiffUseDIV" id="timeDiffUseDIV">
				<input type="radio" name="time" id="not" value="not" checked><label for="not">사용 x</label>
				<input type="radio" name="time" id="use" value="use" ><label for="use">사용</label>
			</div>
		</fieldset>
		`
	}

	makeVarListDIV(list) {
		console.log("makeVarListDIV 변수 목록", list)
		let html= "";
		this.#featureNameList = [];
		for(let variables of list) {
			this.#featureNameList.push(variables.featureName);
			html += `
				<label class="switchLabel">
					<div class="featureName">
						${variables.featureName}
					</div>
					<div class="featureType" id="featureType">
						${variables.featureType}
					</div>
					<div class="featureImportance" id="featureImportance">
						${variables.featureImportance}
					</div>
					<div class="switchDIV">
						<input class="switch" id="switch" role="switch" type="checkbox" checked/>
					</div>
				</label>
			`
		}
		return html;
	}

	setCheckedVarList() {
		const $$switch = document.querySelectorAll("#switch");
		const checkedVar = [];
		for (let i = 0; i < $$switch.length; i++) {
			if ($$switch[i].checked) {
				checkedVar.push($$switch[i].parentElement.parentElement.childNodes[1].innerText);
			}
		}
		return checkedVar;
	}

	async setFileFeatureInfo(fileName) {
		const response = await API(`/files/${fileName}/data/feature/`, "get");
		const status = response.status;
		return status === "success" ? this.#fileFeatureInfo = response.data : null;
	}

	async setImportanceOfFeature(fileName, data) {
		const response = await API(`/files/${fileName}/data/feature/importance/`, "post", data);
		const status = response.status;
		return status === "success" ? this.#fileFeatureInfo = response.data : null;
	}

	async postTimeDiffData(fileName, data) {
		const response = await API(`/files/${fileName}/data/timeseries/`, "post", data);
		const status = response.status;
		if (status === "success") {
			this.#fileData = response.data;
			await this.setImportanceOfFeature(fileName, {
				xValue: JSON.stringify(Object.keys(response.data[0])),
				yValue: data.yValue,
				fileData: JSON.stringify(response.data),
			})
			return;
		}
	}

	async setFileData(fileTitle) {
		const response = await API(`/files/${fileTitle}/data/`, "get");
		const status = response.status;
		return status === "success" ? this.#fileData = response.data : null;
	}

	getFileFeatureInfo() {
		return this.#fileFeatureInfo;
	}

	getFeatureNameList() {
		return this.#featureNameList;
	}

	getFileData() {
		return this.#fileData;
	}
} 

export default new VarPage();