class SelectPage {

	templates(list) {
		const modelList = this.#drawModelList(list);
		return `
			<div class="selectDIV">
				<div class="card">
					<p class="title">모델을 생성합니다</p>
					<p>설명변수, 반응 변수</p>
					<p>모델 명, 분석 도구, trainSize</p>
					<p>선택해 모델을 만듭니다.</p>
					<button class="nextPage" id="nextPage">모델 생성</button>
				</div>
				<div class="card">
					<p class="title">모델을 선택합니다.</p>
					<select class="modelList" id="modelList">
						${modelList}
					</select>
					<button class="modelSelect" id="modelSelect">모델 선택</button>
				</div>
			</div>
		`
	}

	#drawModelList(list) {
		let html = ''
		list.map((value) => {
			html += `
				<option value="${value}">${value}</option>
			`
		});
		return html;
	}
}

export default new SelectPage();