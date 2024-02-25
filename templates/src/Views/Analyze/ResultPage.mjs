import Excel from "/templates/src/Model/Excel.mjs";

class ResultPage {
	#fileData;
	#graphData = [];
	#modelResult;

	templates() {

		const modelResultHtml = this.#makeModelResult();

		return `
		<div class="rowDIV resultDIV">
			<div class="graphDIV" id="graphDIV">
			</div>
			<div class="modelResultDIV">
				${modelResultHtml}
			</div>
		</div>

		<input type="text" name="mergeFileName" class="mergeFileName" id="mergeFileName" placeholder="파일 이름을 정해주세요.">
		<div class="spreadSheetDIV" id="spreadSheetDIV">

		</div>
		<div class="buttonDIV" id="buttonDIV">
			<button class="modelDown" id="modelDown">모델 다운</button>
			<button class="fileDown" id="fileDown">파일 다운</button>
			<button class="prevPage" id="prevPage">이전</button>
		</div>	
		`
	}

	#makeModelResult() {
		return `
			<div class="modelDIV">
				<div class="resultTitle">모델 이름</div>
				<div class="resultText">${this.#modelResult.model_name}</div>
			</div>
			<div class="MSEDIV">
				<div class="resultTitle">MSE</div>
				<div class="resultText">${this.#modelResult.MSE}</div>
			</div>
			<div class="R2DIV">
				<div class="resultTitle">R2</div>
				<div class="resultText">${this.#modelResult.R2}</div>
			</div>
		`
	}

	drawExcel(element) {
		element.innerHTML = "";
		new Excel(this.#fileData, element);
	}

	drawGraph() {
		const svgWidth = 600;
		const svgHeight = 450;
		const svg = d3
			.select("#graphDIV")
			.append("svg")
			.attr("width", svgWidth)
			.attr("height", svgHeight);

		// x 및 y 스케일 생성
		const xScale = d3
			.scaleLinear()
			.domain([d3.min(this.#graphData, (d) => d.yPred)-3, d3.max(this.#graphData, (d) => d.yPred)+3]) // yPred의 최대값을 x의 최대값으로 설정
			.range([0, svgWidth]);

		const yScale = d3
			.scaleLinear()
			.domain([d3.min(this.#graphData, (d) => d.y)-3, d3.max(this.#graphData, (d) => d.y)+3]) // y의 최대값을 y의 최대값으로 설정
			.range([svgHeight, 0]);

		// 산점도 그리기
		svg
			.selectAll("circle")
			.data(this.#graphData)
			.enter()
			.append("circle")
			.attr("cx", (d) => xScale(d.yPred))
			.attr("cy", (d) => yScale(d.y))
			.attr("r", 5)
			.attr("fill", "steelblue")
			// 마우스 이벤트 처리
			.on("mouseover", function (event, d) {
				d3.select(this).attr("r", 8); // 점 크기 키우기 (선택적)
				// 툴팁 표시
				tooltip.transition().duration(200).style("opacity", 0.9);
				tooltip
					.html(`yPred: ${d.yPred}, y: ${d.y}`)
					.style("visibility", "visible")
					.style("left", event.pageX + 10 + "px")
					.style("top", event.pageY - 15 + "px");
			})
			.on("mouseout", function () {
				d3.select(this).attr("r", 5); // 점 크기 되돌리기 (선택적)
				// 툴팁 숨기기
				tooltip.transition().duration(500).style("opacity", 0);
			});

		// x 및 y 축 그리기
		const xAxis = d3.axisBottom(xScale);
		const yAxis = d3.axisLeft(yScale);

		svg
			.append("g")
			.attr("transform", `translate(0, ${svgHeight})`)
			.call(xAxis);

		svg.append("g").call(yAxis);

		// 툴팁 요소 생성
		const tooltip = d3.select("body")
			.append("div")	
			.style("position", "absolute")
			.style("background-color", "white")
			.style("padding", "5px")
			.style("border", "1px solid #ddd")
			.style("border-radius", "5px")
			.style("opacity", 0);
	}

	setModelResult(data) {
		this.#modelResult = data;
		this.#fileData = this.#modelResult.testData;
		this.#setGraphData();
		return;
	}

	#setGraphData() {
		console.log("this.#modelResult", this.#modelResult)
		const y = this.#modelResult.y;
		const yPred = this.#modelResult.yPred;
		console.log(y)
		console.log(yPred)
		this.#graphData = [];
		for(let i in y) {
			const obj = {y:y[i], yPred: yPred[i]};
			this.#graphData.push(obj)
		}
	}

	getFileData() {
		return this.#fileData;
	}

	getGraphData() {
		return this.#graphData;
	}

	getModelResult() {
		return this.#modelResult;
	}
}

export default new ResultPage();

// 산점도, 결과, 엑셀