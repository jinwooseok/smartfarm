import API from "/templates/src/Utils/API.mjs";

export const getFileNameList = async ()=> {
	const response = await API("/files/file-name/", "get");
	return response.data;
}

export const setFileList = ($div, data, fileName='') => {
  data.map( (title) => {
    const value = typeof title === 'string' ? title : title.fileName;
    if (value === fileName) {
      $div.innerHTML += `<Option value= '${value}' selected>` + value + `</option>`;
    } else {
      $div.innerHTML += `<Option value= '${value}'>` + value + `</option>`;
    }
  });
};