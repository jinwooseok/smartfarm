let sort = function(instance, cellNum, order) {
    var order = (order) ? 'desc' : 'asc';
    $('#log').append('The column  ' + cellNum + ' sorted by ' + order + '');
}

// import 모듈화
export default class Excel {
    constructor(data, box) { // 데이터와 div를 생성할 때 매개변수로
        this.excelData = data; // 데이터
        this.makeCol(this.excelData); // 열 데이터 만들기
        this.box=box; // 그려줄 div 선택
        this.box.innerHTML=''; // 이전 데이터 excel 초기화
        
        // excel 그리기
        jspreadsheet(this.box, { 
            data : this.excelData,
            columns : this.excelColumn,
            tableOverflow: true,
            onsort : sort,
        })
    }

    // 열 생성
    makeCol(data){
        this.excelColumn=[];
        for(let i in Object.keys(data[0])){
            this.excelColumn[i] = ({ title: Object.keys(data[0])[i], width: '150px' })
        }
    }
    
    // data 참조
    getData(){
        return this.excelData;
    }

    // ().setFileName(name); -> 다운로드할 때 파일 이름 설정
    setFileName (name){
        this.fileName = name;
    }

}