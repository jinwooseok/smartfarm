import API from "/templates/src/Utils/API.mjs";

class ToolPage {
	#xVarList;

	templates() {
		const xHtml = this.#drawXListHtml();
		return `
		<div class="rowDIV">
			<fieldset class="xDIV">
				<legend>x 값</legend>	
				<div class="variableDIV">
					${xHtml}
				</div>
			</fieldset>

			<div class="fieldsetDIV">
				<fieldset class="yDIV">
					<legend>y 값</legend>
					<input type="text" name="yValueInput" class="yValueInput" id="yValueInput" disabled>
				</fieldset>

				<fieldset class="trainSizeDIV">
					<legend>trainSize</legend>
					<input type="text" name="trainSize" class="trainSize" id="trainSize" value="0.7">
				</fieldset>

				<fieldset class="nameDIV">
					<legend>모델 이름</legend>
					<input type="text" name="modelName" class="modelName" id="modelName" placeholder="모델 이름">
				</fieldset>
			</div>

			<div class="tollDIV">
				<fieldset>
					<legend>분석 도구 선택</legend>
					<div class="toolSelectDIV" id="toolSelectDIV">
						<input type="radio" name="classify" id="classify" value="classify"><label for="classify">분류</label>
						<input type="radio" name="regress" id="regress" value="regress"><label for="regress">회귀</label>
					</div>
				</fieldset>
			</div>

			<div class="modelResultDIV">
			</div>
		</div>
		<div class="buttonDIV" id="buttonDIV">
			<button class="nextPage analyze" id="nextPage" disabled>분석</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>	
		`
	}

	onClickTimeDIff(id) {
		if (id === "classify") {
			return `
			<fieldset class="timeDiffDIV">
				<legend>분석 도구 선택</legend>
				<div class="toolSelectDIV" id="toolSelectDIV">
					<input type="radio" name="classify" id="classify" value="classify" checked><label for="classify">분류</label>
					<input type="radio" name="regress" id="regress" value="regress"><label for="regress">회귀</label>
				</div>

				<fieldset class="typeDIV">
					<legend>분석 종류</legend>
					<select name="technique" id="technique" class="technique">
						<option value="rf">랜덤포레스트</option>
						<option value="svc">소프트 벡터머신</option>
					</select>
				</fieldset>
			</fieldset>

			<div class="optionDIV" id="optionDIV"></div>

			<button class="create" id="create">모델 생성</button>
			`
		}
		return `
		<fieldset class="timeDiffDIV">
			<legend>분석 도구 선택</legend>
			<div class="toolSelectDIV" id="toolSelectDIV">
				<input type="radio" name="classify" id="classify" value="classify"><label for="classify">분류</label>
				<input type="radio" name="regress" id="regress" value="regress" checked><label for="regress">회귀</label>
			</div>

			<fieldset class="typeDIV">
					<legend>분석 종류</legend>
					<select name="technique" id="technique" class="technique">
						<option value="linear">선형 회귀분석</option>
						<option value="lstm">로지스틱 회귀분석</option>
						<option value="lasso">라쏘 회귀</option>
						<option value="ridge">릿지 회귀</option>
						<option value="elastic">엘라스틱넷</option>
						<option value="gb">gradient_boosting</option>
						<option value="svr">소프트 벡터회귀</option>
						<option value="rfr">랜덤포레스트 회귀</option>
					</select>
				</fieldset>
		</fieldset>

		<div class="optionDIV" id="optionDIV">
		</div>

		<button class="create" id="create">모델 생성</button>
		`
	}

	drawOptionDiv(option) {
		if (option === "lasso" || option === "ridge") {
			return `
				<legend>alpha</legend>
				<input type="number" name="alpha" class="alpha" id="alpha" placeholder="0~1 사이 값을 입력해주세요">
			`
		} else if (option === "elastic") {
			return `
				<legend>alpha</legend>
				<input type="number" name="alpha" class="alpha" id="alpha" value="1">
				<legend>l1_ratio</legend>
				<input type="number" name="l1_ratio" class="l1_ratio" id="l1_ratio" placeholder="0~1 사이 값을 입력해주세요">
			`
		} else if (option === "svr" || option === "svc") {
			return `
				<legend>kernal</legend>
				<div class="kernalDIV" id="kernalDIV">
					<input type="radio" name="kernal" id="rbf" value="rbf"><label for="rbf">rbf</label>
					<input type="radio" name="kernal" id="poly" value="poly"><label for="poly">poly</label>
					<input type="radio" name="kernal" id="linear" value="linear"><label for="linear">linear</label>
				</div>
			`
		} else if (option === "gb") {
			return `
				<legend>n_estimators</legend>
				<input type="number" name="n_estimators" class="n_estimators" id="n_estimators" placeholder="0보다 큰 값">
				<legend>learning_rate</legend>
				<input type="number" name="learning_rate" class="learning_rate" id="learning_rate" placeholder="0~1 사이 값을 입력해주세요">
				<legend>max_depth</legend>
				<input type="number" name="max_depth" class="max_depth" id="max_depth" placeholder="0보다 큰 값">
			`
		} else if (option === "rfs" || option === "rf") {
			return `
				<legend>n_estimators</legend>
				<input type="number" name="n_estimators" class="n_estimators" id="n_estimators" placeholder="0보다 큰 값">
				<legend>max_depth</legend>
				<input type="number" name="max_depth" class="max_depth" id="max_depth" placeholder="0보다 큰 값">
				`
		}
	}

	drawModelResult(result) {
		return `
			<div class="modelDIV">
				<div class="resultTitle">모델 이름</div>
				<div class="resultText">${result.model_name}</div>
			</div>
			<div class="MSEDIV">
				<div class="resultTitle">MSE</div>
				<div class="resultText">${result.MSE}</div>
			</div>
			<div class="R2DIV">
				<div class="resultTitle">R2</div>
				<div class="resultText">${result.R2}</div>
			</div>
		`
	}

	setSelectedX(values) {
		this.#xVarList = values; //[1,2,3] 배열 형식
	}

	#drawXListHtml() {
		let html = ''
		this.#xVarList.map((x) => {
			html += `
				<div>
					<p id="${x}">${x}</p>
				</div>
			`
		});

		return html;
	}

	validateData(data) {
		const {modelName, model, trainSize, yValue, xValue} = data;

		if (modelName === "모델 이름" || modelName ==="") {
			alert("이름을 정해주세요");
			return;
		}

		if (Number(trainSize) < 0 && Number(trainSize) > 1) {
			alert("trainSize는 0~1로 입력해주세요");
			return;
		}
	}

	async postModelData(fileName, data) {
		this.validateData(data);
		const response = await API(`/analytics/${fileName}/model/`, "post", data);
    const status = response.status;
		return status === "success" ? response.data : null;
	}

} 

export default new ToolPage();