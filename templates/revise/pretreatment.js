const $pretreatmentFileName = document.querySelector('#pretreatmentFileName');
const $pretreatmentSave = document.querySelector('#pretreatmentSave');
<<<<<<< HEAD
1
$pretreatmentSave.addEventListener('click', () => {
	$.ajax({
		url: `revise/${JSON.parse(localStorage.getItem("fileTitle"))}/preprocess/`,
=======

$pretreatmentSave.addEventListener('click', () => {
	$.ajax({
		url: `/revise/${JSON.parse(localStorage.getItem("fileTitle"))}/preprocess/`,
>>>>>>> 76456d5b10e11562338f115943b10e70be2bb91f
		type:'post',
		dataType: 'json',
		headers: { 'X-CSRFToken': csrftoken },
		data:{
				newFileName : $pretreatmentFileName.value,
		},
		success:function(response){
				alert("완료되었습니다.");
				window.location.href = "/file-list/";
		},
})
})