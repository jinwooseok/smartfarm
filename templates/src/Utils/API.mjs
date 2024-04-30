import cookies from "/templates/src/Utils/CsrfToken.mjs";

// 비동기로 작동
// url: 링크
// type: get, post
// data: 객체 형태로 전송할 데이터, get인 경우 data를 전송하지 않는다.
const API = async (url, type, data={}) => {
	try {
		const response = await $.ajax({
			url: url,
			type: type,
			dataType: "json",
			headers: { "X-CSRFToken": cookies['csrftoken'] },
			data: data,
			async: false,
		});
		// 정상적으로 작동하면 값을 반환
		return response;

	} catch (error) {
		// 전송에 실패하면 실패한 원인을 알림으로 
		alert(`ERROR ${error.responseJSON.message}`)
		return error.responseJSON ? error.responseJSON : error.status;
	}
}

export default API;