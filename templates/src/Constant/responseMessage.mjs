const responseMessage = Object.freeze({
	400: "필수 fileData에 값이 존재하지 않습니다",
	401: "로그인이 필요합니다.",
	452: "DB에 파일이 존재하지 않습니다.",
	454: "파일 저장에 실패하였습니다.",
	455: "저장된 임시파일이 없습니다.",
	456: "데이터를 csv로 변환할 수 없습니다.",
	470: "날짜열에 null값이 존재합니다. 결측치를 제거해주세요.",
	471: "날씨 API를 가져오는데 실패하였습니다. 잠시 후 다시 시도해주세요.",
	472: "시작행이 1보다 작거나 데이터 길이를 초과합니다.",
	473: "날짜열이 1보다 작거나 데이터 길이를 초과합니다.",
	474: "{variable} 변수에서 오류가 발생했습니다.",
	success: "success"
});

export default responseMessage;

// import responseMessage from "/templates/src/Constant/responseMessage.mjs";
// const status = response.status || response;
// responseMessage[status] === "success" ? location.replace("/file-list/") : alert(responseMessage[status]);
// return responseMessage[status] === "success" ? response.data : alert(responseMessage[status]);