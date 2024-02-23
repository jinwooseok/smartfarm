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
			<button class="nextPage analyze" id="nextPage">분석</button>
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
						<option value="rf">랜텀포레스트</option>
					</select>
				</fieldset>
			</fieldset>

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
						<option value="linear">선형회귀분석</option>
						<option value="lstm">로지스틱회귀분석</option>
					</select>
				</fieldset>
		</fieldset>

		<button class="create" id="create">모델 생성</button>
		`
	}

	drawModelResult(result) {
		console.log(result)
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