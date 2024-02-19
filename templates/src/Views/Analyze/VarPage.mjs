import API from "/templates/src/Utils/API.mjs";
import responseMessage from "/templates/src/Constant/responseMessage.mjs";

class VarPage {
	#varList = "";
	#featureNameList = [];
	#xValues = [];

	templates() {
		const switchHtml = this.#makeVarListDIV(); // 목록이 두번 만들어짐
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
					${switchHtml}
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

					<button class="timeDiffBtn" id="timeDiffCreate" disabled>시차변수 생성</button>
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

			<fieldset class="windowSizeDIV">
				<legend>windowSize</legend>
				<input type="number" name="windowSize" class="windowSize" id="windowSize" value="1">
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

		<button class="timeDiffBtn" id="timeDiffCreate" disabled>시차변수 생성</button>
		`
	}

	#makeVarListDIV() {
		let html = '';
		this.#featureNameList = [];
		for(let variables of this.#varList) {
			this.#featureNameList.push(variables.featureName)
			html += `
				<label class="switchLabel">
					<div class="featureName">
						${variables.featureName}
					</div>
					<div class="featureType" id="featureType">
						${variables.featureType}
					</div>
					<div class="featureImportance" id="featureImportance">
						${variables.feature_importance}
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
		this.#xValues = checkedVar;
		return checkedVar;
	}

	async setVarList(fileName) {
		const response = await API(`/files/${fileName}/data/feature/`, "get");
		const status = response.status || response;
		if (response.status === "success") {
			return responseMessage[status] === "success" ? this.#varList = response.data : alert(responseMessage[status]);
		}
	}

	async postTimeDiffData(timeDiffName, data) {
		const response = await API(`/files/${timeDiffName}/data/timeseries/`, "post", data);
		const status = response.status || response;
		return responseMessage[status] === "success" ? response.data : alert(responseMessage[status]);
	}

	async setFileData(fileTitle) {
		const response = await API(`/files/${fileTitle}/data/`, "get");
		const status = response.status || response;
		return responseMessage[status] === "success" ? response.data : alert(responseMessage[status]);
	}

	getVarList() {
		return this.#varList;
	}

	getFeatureNameList() {
		console.log(this.#featureNameList)
		return this.#featureNameList;
	}

	getXValues() {
		return this.#xValues;
	}
} 

export default new VarPage();