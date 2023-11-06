const $pretreatmentFileName = document.querySelector('#pretreatmentFileName');
const $pretreatmentSave = document.querySelector('#pretreatmentSave');
const excel_data = JSON.parse(document.getElementById("jsonObject").value);

$pretreatmentSave.addEventListener('click', () => {
	$.ajax({
		url: `revise/${JSON.parse(localStorage.getItem("title_list"))}/preprocess/`,
		type:'post',
		dataType: 'json',
		headers: { 'X-CSRFToken': csrftoken },
		data:{
				newFileName : $pretreatmentFileName.value,
		},
		success:function(response){
				alert("완료되었습니다.");
				window.location.href = "/fileList/";
		},
})
})