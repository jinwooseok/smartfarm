import API from "/templates/src/Utils/API.mjs";

export const getFileNameList = async ()=> {
	const response = await API("/files/file-name/", "get");
	return response.data;
}

export const setFileList = ($div, data, fileName='') => {	
  data.map( (title) => {
    if (title.fileName === fileName) {
      $div.innerHTML += `<Option value= '${title || title.fileName}' selected>` + title || title.fileName + `</option>`;
    } else {
      $div.innerHTML += `<Option value= '${title || title.fileName}'>` + title || title.fileName + `</option>`;
    }
  });
};