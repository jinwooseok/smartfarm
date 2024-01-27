class Graph {

	#data;
	#maxIndex = 80;
	#chart;
	
	constructor() {

	}

	nextData() {

	}	

	closeGraph() {
		document.querySelector("#fileStaticDataDIV").style.width = "1000px";
		document.querySelector("#graphDIV").style.display = "none";
	}

	showGraph(event) {
		document.querySelector("#fileStaticDataDIV").style.width = "500px";
		document.querySelector("#graphDIV").style.display = "block";

		// const xColumn = lineDraw(name);

		// this.#chart = bb.generate({
		// 	bindto: "#myChart",
		// 	data: {
		// 		x: xColumn,
		// 		type: "line",
		// 		columns: graphArr,
		// 	},
		// 	axis: {
		// 		x: {
		// 			type: "category",
		// 			tick: {
		// 				rotate: 75,
		// 				multiline: false,
		// 				tooltip: true,
		// 			},
		// 		},
		// 	},
		// });
	
		// buttonShow(startIndex, lastIndex);
	}

	#setMaxIndex(length ) {
		this.#maxIndex = this.#maxIndex > length ? length : this.#maxIndex;
	}
	
	setData(data) {
		this.#data = data;
		this.#setMaxIndex(data.length);
	}

	getData() {
		return this.#data;
	}

}

export default new Graph();