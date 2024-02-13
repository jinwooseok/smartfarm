import API from "/templates/src/Utils/API.mjs";

export const getFileNameList = async ()=> {
	const response = await API("/files/file-name/", "get");
	return response.data;
}

export const setFileList = async ($div, fileName) => {
	const data = await getFileNameList();
	
  data.map( (title) => {
    if (title.fileName === fileName) {
      $div.innerHTML += `<Option value= '${title.fileName}' selected>` + title.fileName + `</option>`;
    } else {
      $div.innerHTML += `<Option value= '${title.fileName}'>` + title.fileName + `</option>`;
    }
  });
};
