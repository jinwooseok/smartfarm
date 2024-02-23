// import 모듈화
export default class Excel {
  #excelData;
  #excelColumn;

  constructor(data, box) {
    // 데이터와 div를 생성할 때 매개변수로
    this.#excelData = data; // 데이터
    this.#excelColumn = this.#makeCol(this.#excelData); // 열 데이터 만들기
    box.innerHtml = "";
    // excel 그리기
    jspreadsheet(box, {
      data: this.#excelData,
      columns: this.#excelColumn,
      tableOverflow: true,
      lazyLoading:true,
    });
  }

  // 열 생성
  #makeCol(data) {
    const excelColumn = [];
    for (let i in Object.keys(data[0])) {
      excelColumn[i] = { title: Object.keys(data[0])[i], width: "150px" };
    }
    return excelColumn;
  }

  // data 참조
  getData() {
    return this.#excelData;
  }
}
