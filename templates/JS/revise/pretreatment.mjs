import cookies from "/templates/JS/Utils/csrfToken.js";
import Loading from "/templates/JS/Utils/Loading.mjs";

const $pretreatmentFileName = document.querySelector('#pretreatmentFileName');
const $pretreatmentSave = document.querySelector('#pretreatmentSave');

const csrftoken = cookies['csrftoken'] // csrftoken

$pretreatmentSave.addEventListener('click', () => {
	Loading.StartLoading();
	$.ajax({
		url: `/revise/${JSON.parse(localStorage.getItem("fileTitle"))}/preprocess/`,
		type:'post',
		dataType: 'json',
		headers: { 'X-CSRFToken': csrftoken },
		data:{
				newFileName : $pretreatmentFileName.value,
		},
		success:function(response){
			Loading.CloseLoading();
				alert("완료되었습니다.");
				window.location.href = "/file-list/";
		},
	})
	Loading.CloseLoading();
})