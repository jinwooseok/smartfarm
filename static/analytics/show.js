function down() {
    var wb = XLSX.utils.table_to_book(document.getElementById('datatablesSimple'), {sheet : "시트명", raw:true});
    XLSX.writeFile(wb, ('파일명.xlsx'));
}
