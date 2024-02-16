class ToolPage {
	#varList;
	#featureNameList = [];

	templates() {
		const switchHtml = this.#makeVarListDIV();
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

				<fieldset class="typeDIV">
					<legend>분석 종류</legend>
					<select name="technique" id="technique" class="technique">
						<option value="linear">선형회귀분석</option>
						<option value="lstm">로지스틱회귀분석</option>
						<option value="rf">랜텀포레스트</option>
					</select>
				</fieldset>

				<fieldset class="trainSizeDIV">
					<legend>trainSize</legend>
					<input type="text" name="trainSize" class="trainSize" id="trainSize" placeholder="0~1">
				</fieldset>

				<fieldset class="nameDIV">
					<legend>모델 이름</legend>
					<input type="text" name="modelName" class="modelName" id="modelName" placeholder="모델 이름">
				</fieldset>

				<button class="create" id="create">생성하기</button>
			</div>
		</div>
		`
	}

	async setVarList(list) {
		this.#varList = list;
	}

	#makeVarListDIV() {
		let html = '';

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

		return checkedVar;
	}

	// 파일 정보 받기

	// API 연동

	getFeatureNameList() {
		return this.#featureNameList;
	}
} 

export default new ToolPage();