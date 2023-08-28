const $pretreatmentFileName = document.querySelector('#pretreatmentFileName');
const $pretreatmentSave = document.querySelector('#pretreatmentSave');

$pretreatmentSave.addEventListener("click", ()=>{
    console.log(`/revise/preprocess/${JSON.parse(localStorage.getItem("fileTitle"))}`)
    $.ajax({
        url:`preprocess/`,
        type:'post',
        dataType: 'json',
        headers: { 'X-CSRFToken': csrftoken },
        data:{},
        success: function (response) {
            if (response.data != null) {
                console.log(response.data);
                window.location.href = "/fileList/";
            }
            else {
                alert('전송할 데이터가 없습니다.')
            }

        },
        error: function (xhr, error) {
            alert("에러입니다.");
            console.error("error : " + error);
        }
    })
})