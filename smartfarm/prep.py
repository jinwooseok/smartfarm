import pandas as pd
def show(request):
    json=request.POST['jsonObject']
    x=request.POST['x_value']
    df=pd.read_json(json)  
    result=str(df.info())
    return result

# #
# def rep(request):
#     nan_rp=request.POST['대체값']
#     if nan_rp == 'mean':
#         df = df.fillna(df.mean())
#     if nan_rp == and  :
#     df.loc[df[] != df['A'], nan_rp] = 0
#     return result
#     else:
#         df = df.fillna(0)