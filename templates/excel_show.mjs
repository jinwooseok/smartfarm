// import 모듈화
export class Excel {
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
        })
    }

    // 열 생성
    makeCol(data){
        this.excelColumn=[];
        for(let i in Object.keys(data[0])){
            this.excelColumn[i] = ({ title: Object.keys(data[0])[i], width: '150px' })
        }
    }

    // download
    download(data){
        const jsonData = JSON.stringify(data);
        let jsonDataParsing = JSON.parse(jsonData);
        let toCsv = '';
        let row="";

        for(let i in jsonDataParsing[0]){
            row += i+","; // 열 입력
        }
        row = row.slice(0,-1);
        toCsv += row +"\r\n";

        for(let i=0; i<jsonDataParsing.length; i++){
            row="";
            for(let j in jsonDataParsing[i]){
                row += ""+jsonDataParsing[i][j] + ","; // 열 제외 입력
            }
            row.slice(0, row.length - 1);
            toCsv += row + '\r\n';
        }

        if(toCsv===''){
            alert("Invalid data");
            return;
        }

        let fileName = `${this.fileName}_수정`; // 다운로드 파일 이름

        //Initialize file format you want csv or xls
        let uri = 'data:text/csv;charset=utf-8,\uFEFF' + encodeURI(toCsv);

        let link = document.createElement("a");    
        link.href = uri;
        link.style = "visibility:hidden";
        link.download = fileName + ".csv";
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
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