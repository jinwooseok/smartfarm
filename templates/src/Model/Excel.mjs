// import 모듈화
export default class Excel {

  // private
  #excelData; // 데이터
  #excelColumn; // 열 이름

  // 파일 데이터, 데이터를 그릴 html tag를 매개변수로 받는다.
  constructor(data, box) {
    this.#excelData = data; 
    this.#excelColumn = this.#makeCol(this.#excelData); // 열 데이터 만들기
    box.innerHtml = ""; // 기존 tag의 화면 디자인은 제거
    
    // excel 그리기
    // tag, {데이터, 열, 기타 옵션}
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

  // data 반환
  getData() {
    return this.#excelData;
  }
}
