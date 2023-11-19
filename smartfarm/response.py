def fileListViewResponse(user_name, files):
    context={'user_name':user_name,
            'files':files}
    return context
def fileDownLoadApiResponse(file_name, data):
    context = {'file_name':file_name,
                'data': data}
    return context

def dataLoadApiResponse(data, summary,file_name):
    context = {
        'result':'success',
        'file_name':file_name,
        'summarys' : summary,
        'data': data}
    return context

def dataEditViewResponse(data, summary, user_name, file_name):
    context = {
                    'user_name':user_name,
                    'result':'success',
                    'data' : data,
                    'summarys' : summary,
                    'file_name':file_name
                }
    return context

def dataEditWithNoFileViewResponse(user_name):
    context = {'user_name':user_name}
    return context

def successResponse():
    context = {'result':'success'}
    return context

def failResponse():
    context = {'result':'fail'}
    return context

def successDataResponse(data):
    context = {'result':'success',
                'data':data}
    return context

def fileMergeViewResponse(user_name, files):
    context={'user_name':user_name,
            'files':files}
    return context

def fileMergeApiResponse(file_name_list,files = None):
    context = {'result':'success',
            'files':files,   
            'fileNameList': file_name_list}
    return context

def analysisViewResponse(user_name, data):
    context={'user_name':user_name,
            'data': data}
    return context