def fileListViewResponse(user_name, files):
    context={'user_name':user_name,
            'files':files}
    return context
def fileDownLoadApiResponse(file_name, data):
    context = {'file_name':file_name,
                'data': data}
    return context

def dataLoadApiResponse(file_name, data):
    context = {
        'result':'success',
        'file_name':file_name,
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

def dataEditView2Response(user_name):
    context = {'user_name':user_name}
    return context