import Excel from "/templates/src/Model/Excel.mjs";
import Loading from "/templates/src/Utils/Loading.mjs";

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
			.domain([d3.min(this.#graphData, (d) => d.y_pred)-3, d3.max(this.#graphData, (d) => d.y_pred)+3]) // y_pred의 최대값을 x의 최대값으로 설정
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
			.attr("cx", (d) => xScale(d.y_pred))
			.attr("cy", (d) => yScale(d.y))
			.attr("r", 5)
			.attr("fill", "steelblue")
			// 마우스 이벤트 처리
			.on("mouseover", function (event, d) {
				d3.select(this).attr("r", 8); // 점 크기 키우기 (선택적)
				// 툴팁 표시
				tooltip.transition().duration(200).style("opacity", 0.9);
				tooltip
					.html(`y_pred: ${d.y_pred}, y: ${d.y}`)
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

	async setModelResult(modelName, data) {
		// const response = await API(await API(`/analytics/${modelName}/`, "post", data);
		// const status = response.status;
		Loading.CloseLoading()
		// return status === "success" ? this.#modelResult = response.data : null;
		this.#modelResult = {
					"model": "Linear Regression",
					"featureNames": [
							"외부기온",
							"내부습도"
					],
					"targetNames": "내부온도",
					"randomState": 42,
					"MSE": 1.2507419735977627,
					"R2": 0.7334409023180202,
					"testData": [
							{
									"외부기온": 13.68,
									"내부습도": 100.0,
									"내부온도": 15.5,
									"내부온도_pred": 16.26453105235415
							},
							{
									"외부기온": 20.85,
									"내부습도": 66.53,
									"내부온도": 21.53,
									"내부온도_pred": 21.21006981781263
							},
							{
									"외부기온": 13.5,
									"내부습도": 100.0,
									"내부온도": 15.48,
									"내부온도_pred": 16.105358501156754
							},
							{
									"외부기온": 16.0,
									"내부습도": 88.0,
									"내부온도": 15.72,
									"내부온도_pred": 17.815998319536142
							},
							{
									"외부기온": 14.1,
									"내부습도": 99.0,
									"내부온도": 15.32,
									"내부온도_pred": 16.594259500201225
							},
							{
									"외부기온": 19.75,
									"내부습도": 68.77,
									"내부온도": 20.38,
									"내부온도_pred": 20.330698816020597
							},
							{
									"외부기온": 18.5,
									"내부습도": 68.0,
									"내부온도": 20.92,
									"내부온도_pred": 19.19324476500738
							},
							{
									"외부기온": 16.22,
									"내부습도": 82.0,
									"내부온도": 16.7,
									"내부온도_pred": 17.760497519096287
							},
							{
									"외부기온": 12.0,
									"내부습도": 99.87,
									"내부온도": 15.3,
									"내부온도_pred": 14.773502932202021
							},
							{
									"외부기온": 13.52,
									"내부습도": 100.0,
									"내부온도": 15.5,
									"내부온도_pred": 16.123044340178687
							},
							{
									"외부기온": 11.59,
									"내부습도": 99.85,
									"내부온도": 17.77,
									"내부온도_pred": 14.410109748820123
							},
							{
									"외부기온": 12.41,
									"내부습도": 97.87,
									"내부온도": 15.8,
									"내부온도_pred": 15.052714288924609
							},
							{
									"외부기온": 10.73,
									"내부습도": 99.14,
									"내부온도": 16.21,
									"내부온도_pred": 13.620030009031407
							},
							{
									"외부기온": 21.25,
									"내부습도": 64.23,
									"내부온도": 21.95,
									"내부온도_pred": 21.467936003540196
							},
							{
									"외부기온": 15.78,
									"내부습도": 97.0,
									"내부온도": 17.68,
									"내부온도_pred": 17.99652163481656
							},
							{
									"외부기온": 19.8,
									"내부습도": 60.68,
									"내부온도": 21.16,
									"내부온도_pred": 20.037769365222058
							},
							{
									"외부기온": 19.03,
									"내부습도": 72.0,
									"내부온도": 19.55,
									"내부온도_pred": 19.828616185542682
							},
							{
									"외부기온": 14.08,
									"내부습도": 89.25,
									"내부온도": 15.1,
									"내부온도_pred": 16.170250487947474
							},
							{
									"외부기온": 20.52,
									"내부습도": 60.83,
									"내부온도": 21.32,
									"내부온도_pred": 20.68071069575367
							},
							{
									"외부기온": 12.73,
									"내부습도": 92.56,
									"내부온도": 15.29,
									"내부온도_pred": 15.114397862007747
							},
							{
									"외부기온": 20.12,
									"내부습도": 66.17,
									"내부온도": 20.63,
									"내부온도_pred": 20.54953399173121
							},
							{
									"외부기온": 13.52,
									"내부습도": 100.0,
									"내부온도": 15.4,
									"내부온도_pred": 16.123044340178687
							},
							{
									"외부기온": 14.78,
									"내부습도": 100.0,
									"내부온도": 17.46,
									"내부온도_pred": 17.237252198560466
							},
							{
									"외부기온": 13.3,
									"내부습도": 89.0,
									"내부온도": 15.6,
									"내부온도_pred": 15.470084223188707
							},
							{
									"외부기온": 12.9,
									"내부습도": 93.0,
									"내부온도": 16.39,
									"내부온도_pred": 15.283064129204126
							},
							{
									"외부기온": 14.28,
									"내부습도": 100.0,
									"내부온도": 15.68,
									"내부온도_pred": 16.79510622301214
							},
							{
									"외부기온": 13.7,
									"내부습도": 100.0,
									"내부온도": 15.4,
									"내부온도_pred": 16.28221689137608
							},
							{
									"외부기온": 11.99,
									"내부습도": 100.0,
									"내부온도": 15.6,
									"내부온도_pred": 14.770077655000811
							},
							{
									"외부기온": 15.68,
									"내부습도": 76.31,
									"내부온도": 17.97,
									"내부온도_pred": 17.04585382902317
							},
							{
									"외부기온": 16.98,
									"내부습도": 80.66,
									"내부온도": 17.88,
									"내부온도_pred": 18.376716011967627
							},
							{
									"외부기온": 12.24,
									"내부습도": 95.0,
									"내부온도": 15.7,
									"내부온도_pred": 14.782779784707376
							},
							{
									"외부기온": 15.02,
									"내부습도": 88.25,
									"내부온도": 15.68,
									"내부온도_pred": 16.959810750364806
							},
							{
									"외부기온": 15.28,
									"내부습도": 89.82,
									"내부온도": 16.2,
									"내부온도_pred": 17.25515510708316
							},
							{
									"외부기온": 12.11,
									"내부습도": 98.0,
									"내부온도": 15.81,
									"내부온도_pred": 14.79284434590537
							},
							{
									"외부기온": 18.8,
									"내부습도": 72.56,
									"내부온도": 19.36,
									"내부온도_pred": 19.648566572894023
							},
							{
									"외부기온": 17.6,
									"내부습도": 81.0,
									"내부온도": 17.93,
									"내부온도_pred": 18.93914623999615
							},
							{
									"외부기온": 14.16,
									"내부습도": 97.0,
									"내부온도": 15.6,
									"내부온도_pred": 16.563968674039984
							},
							{
									"외부기온": 20.32,
									"내부습도": 67.47,
									"내부온도": 19.95,
									"내부온도_pred": 20.780568805048112
							},
							{
									"외부기온": 13.5,
									"내부습도": 90.85,
									"내부온도": 17.18,
									"내부온도_pred": 15.724039830893048
							}
					],
					"y_pred": [
							16.26453105235415,
							21.21006981781263,
							16.105358501156754,
							17.815998319536142,
							16.594259500201225,
							20.330698816020597,
							19.19324476500738,
							17.760497519096287,
							14.773502932202021,
							16.123044340178687,
							14.410109748820123,
							15.052714288924609,
							13.620030009031407,
							21.467936003540196,
							17.99652163481656,
							20.037769365222058,
							19.828616185542682,
							16.170250487947474,
							20.68071069575367,
							15.114397862007747,
							20.54953399173121,
							16.123044340178687,
							17.237252198560466,
							15.470084223188707,
							15.283064129204126,
							16.79510622301214,
							16.28221689137608,
							14.770077655000811,
							17.04585382902317,
							18.376716011967627,
							14.782779784707376,
							16.959810750364806,
							17.25515510708316,
							14.79284434590537,
							19.648566572894023,
							18.93914623999615,
							16.563968674039984,
							20.780568805048112,
							15.724039830893048
					],
					"y": [
							15.5,
							21.53,
							15.48,
							15.72,
							15.32,
							20.38,
							20.92,
							16.7,
							15.3,
							15.5,
							17.77,
							15.8,
							16.21,
							21.95,
							17.68,
							21.16,
							19.55,
							15.1,
							21.32,
							15.29,
							20.63,
							15.4,
							17.46,
							15.6,
							16.39,
							15.68,
							15.4,
							15.6,
							17.97,
							17.88,
							15.7,
							15.68,
							16.2,
							15.81,
							19.36,
							17.93,
							15.6,
							19.95,
							17.18
					],
					"model_name": "linear_env"
			}

		this.#fileData = this.#modelResult.testData;
		this.#setGraphData();
	}

	#setGraphData() {
		const y = this.#modelResult.y;
		const y_pred = this.#modelResult.y_pred;
		this.#graphData = [];
		for(let i in y) {
			const obj = {y:y[i], y_pred: y_pred[i]};
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