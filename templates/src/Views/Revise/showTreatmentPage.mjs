import API from "/templates/src/Utils/API.mjs";

class ShowTreatmentPage{

	#staticData;
	#fileTitle;

	constructor() {
	}

	templates() {
		return `
		<div class="fileStaticDataDIV" id="fileStaticDataDIV">
			<div class="columnList">
				<div class="columnName" id="columnName">
					열 이름
				</div>
				<div class="nullCount" id="nullCount">
					빈 값
				</div>
				<div class="Q1" id="Q1">
					1사분위 값
				</div>
				<div class="Q2" id="Q2">
					중앙값
				</div>
				<div class="Q3" id="Q3">
					3사분위값
				</div>
				<div class="mean" id="mean">
					평균
				</div>
				<div class="min" id="min">
					최소
				</div>
				<div class="max" id="max">
					최대
				</div>
			</div>
		</div>

		<div class="buttonDIV" id="buttonDIV">
			<button class="next" id="next">다음</button>
			<button class="prev" id="prev">이전</button>
		</div>
		`
	}

	async setStaticData () {
		const response = await API(`/files/${this.#fileTitle}/data/summary/`, "get");
		this.#staticData = response.data;
		console.log("staticData", this.#staticData);
	}

	setFileTitle(fileName) {
		this.#fileTitle = fileName;
	}

	getStaticData() {
		return this.#staticData;
	}
}

export default new ShowTreatmentPage();

// const drawStaticData = (staticData) => {
// 	const $fileStaticDataDIV = document.querySelector("#fileStaticDataDIV");
// 	console.log("drawStaticData", staticData)
// 	// 여기부터 시작 => 통계치 그리기
// 	// for(let data of staticData) {
		
// 	// 	$fileStaticDataDIV.innerHTML += `
// 	// 		<div class="columnList">
// 	// 			<div class="columnName" id="columnName">
// 	// 				rererererererereerr
// 	// 			</div>
// 	// 			<div class="nullCount" id="nullCount">
// 	// 				3
// 	// 			</div>
// 	// 			<div class="Q1" id="Q1">
// 	// 				100
// 	// 			</div>
// 	// 			<div class="Q2" id="Q2">
// 	// 				100
// 	// 			</div>
// 	// 			<div class="Q3" id="Q3">
// 	// 				1000000000
// 	// 			</div>
// 	// 			<div class="mean" id="mean">
// 	// 				1
// 	// 			</div>
// 	// 			<div class="min" id="min">
// 	// 				0
// 	// 			</div>
// 	// 			<div class="max" id="max">
// 	// 				1
// 	// 			</div>
// 	// 		</div>
// 	// 	`
// 	// }
// }