class Graph{

	#showCount; // 한 번에 보여주는 label 수
	#graphData;

	#xAxisValue;
	#startIndex;
	#lastIndex;

	constructor(data) {
		this.#graphData = data;
		this.#showCount = 70;

		this.#setIndex(0, this.#showCount);
	}

	// x축 값 설정

	// y값 설정

	// 다중 그래프

	// 단일 그래프

	#setIndex(startIndex, lastIndex) {
		this.#startIndex = startIndex;
		this.#lastIndex = lastIndex;
	}

}

export default Graph;