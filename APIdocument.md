# api문서
### 데이터베이스 호출
###### /api/users/
- 유저 데이터베이스 전체 호출
###### /api/file/
- 파일 데이터베이스 전체 호출

------로그인 필수------
### data_list URL
###### /data_list/ => fileList
GET
    - data_list창으로 이동

###### /data_list/upload/ => fileList/upload
GET
    - upload창으로 이동
POST
    - 데이터베이스에 파일 업로드
    request : {name:'file_input',type:multipart/form-data,description:파일 자체
    name:'upload_title',type:string,description:파일명}
    response : 업로드 완료

###### /data_list/delete/ => fileList/delete
POST
    - 데이터베이스와 서버 스토리지에서 파일 삭제
    request : {name:'data',type:array,description:체크 박스를 누른 파일 이름 리스트}
    response : 삭제 완료

### merge URL
###### /merge/
POST
    - 데이터 2개 합치기
    request : {name:'data',type:array,description:체크 박스를 누른 파일 이름 리스트}
    response : "[json객체 , json객체]" 의 형태
### revise URL
###### /revise/
GET
    - revise창으로 이동
###### /revise/<str:file_name>/
POST
    -revise로 이동하면서 파일명 전달 시 호출 
###### /revise/loaddata/
POST
    -파일명으로 데이터를 호출
    request : {name:'file_name',type:string,description:기준 데이터}
    response : 호출한 데이터의 json문자열
###### /revise/farm/

