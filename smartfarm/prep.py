import pandas as pd
#특정 열의 상태
def show(request):
    json=request.POST['jsonObject']
    x=request.POST['x_value']
    df=pd.read_json(json)  
    result=str(df.info())
    return result

#공백 제거
def fill_blank(request):
    json=request.POST['jsonObject']
    df=pd.read_json(json)
    df[''].apply(lambda x: x.replace(" ",""))

#값 대체
def rep(request):
    nan_rp=request.POST['대체값']
    if nan_rp == 'mean':
        df = df.fillna(df.mean())
    if nan_rp == '0' :
        df.loc[df['A'] != df['A'], nan_rp] = 0
    else:
        df = df.fillna(0)

    return df

#합치기
#왼쪽기준 오른쪽기준 

#날짜통일
