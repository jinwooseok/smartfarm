import API from "/templates/src/Utils/API.mjs";

const setFileListSelectBox = async ()=> {
	const response = await API("/files/file-name/", "get");
	return response.data;
}

export default setFileListSelectBox;