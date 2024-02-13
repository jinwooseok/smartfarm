import API from "/templates/src/Utils/API.mjs";

class TimeDifferenceDataPage {
	templates() {
		return `
		<div class="buttonDIV" id="buttonDIV">
			<button class="save" id="save">저장</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>
		`
	}
}

export default new TimeDifferenceDataPage();