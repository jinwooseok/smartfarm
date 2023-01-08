var JsonFile = JSON.parse(JsonFile);
function making_table(File){
    var col_name = File.schema.fields;
    var fields = File.data;
    var html=[],h=-1;
    const element =document.getElementById('content');
    for (var i=0;i<col_name.length;i++){
        if (i==0){html[++h]='<tr><th>'}
        html[++h]=col_name[i].name;
        html[++h]='</th><th>'
        if(i==col_name.length-1){html[++h]='</th></tr>';break}
    }
    for (var j=0;j<fields.length;j++){
        for (var i=0;i<col_name.length;i++){
        if (i==0){html[++h]='<tr><td>'}
        field_name = col_name[i].name;
        html[++h]=fields[j][field_name];
        html[++h]='</td><td>'
        if(i==col_name.length-1){html[++h]='</td></tr>';break}
        }
    }
    element.innerHTML = html.join('');
}
making_table(JsonFile)
