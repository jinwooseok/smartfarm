import API from "/templates/src/Utils/API.mjs";

class ShowPreprocessPage{

	#staticData;
	#fileTitle;

	constructor() {
	}

	async templates() {
		
		const staticHtml = await this.drawHtml();
		const html = `
		<div class="rowDIV">
			<div class="fileStaticDataDIV" id="fileStaticDataDIV">
				<div class="titleListDIV" id="titleListDIV">
					<div class="columnList">
						<div class="columnName">
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
				<div class="listDIV" id="listDIV">
					${staticHtml}
				</div>
			</div>
			<div class="graphDIV" id="graphDIV">
				<div id="myChart">
				</div>
				<div id="buttonContainer" class="buttonContainer">
					<div id="Prev" style="visibility: hidden;"> <i class="fa-solid fa-arrow-left"></i></div>
					<div id="Next"> <i class="fa-solid fa-arrow-right"></i></div>
				</div>
				<button class="closeGraph" id="closeGraph">닫기</button>
			</div>
		</div>
		
		<div class="buttonDIV" id="buttonDIV">
			<button class="nextPage treat" id="nextPage">다음</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>
		`

		return html;
	}

	async submit() {
		const response = await API(`/files/${this.#fileTitle}/data/preprocess/`, "post");
		console.log(response, "treat");
	}

	async drawHtml() {
		let html = '';

		await this.setStaticData();

		for(let data of this.#staticData) {
			html += `
				<div class="columnList">
					<div class="columnName" id="columnName">
						${data.name}
					</div>
					<div class="nullCount" id="nullCount">
						${data["Null_count"]}
					</div>
					<div class="Q1" id="Q1">
						${data.Q1}
					</div>
					<div class="Q2" id="Q2">
						${data.Q2}
					</div>
					<div class="Q3" id="Q3">
						${data.Q3}
					</div>
					<div class="mean" id="mean">
						${data.mean}
					</div>
					<div class="min" id="min">
						${data.min}
					</div>
					<div class="max" id="max">
						${data.max}
					</div>
				</div>
			`
		}

		return html;
	}

	async setStaticData() {
		const response = await API(`/files/${this.#fileTitle}/data/summary/`, "get");
		this.#staticData = response.data;
	}

	setFileTitle(fileName) {
		this.#fileTitle = fileName;
	}

	getStaticData() {
		return this.#staticData;
	}
}

export default new ShowPreprocessPage();