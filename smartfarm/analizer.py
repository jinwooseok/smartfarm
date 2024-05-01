from django.shortcuts import render
import pandas as pd
#분석도구들을 모아놓은 파일
import statsmodels.api as sm  
def linear(d,x,y):#회귀분석을 실행. 결과표,분산분석표,상관분석표까지 표현
    all_value = x+[y]
    d = d[all_value]
    d=d.fillna(0)
    if d.shape[0] == 0 :  
        return 400 

    X = sm.add_constant(d)
    
    result = sm.OLS(d[y],X).fit()
    result_dict = {}
    result_dict = result.summary().as_html()
    return result_dict

def ttest(request,type):#2번 단일표본 3번 독립표본 4번 대응표본
    import scipy.stats as stats
    json=request.POST['jsonObject']
    b=pd.read_json(json)
    if type=="2":
        x=request.POST['x_value']
        t=stats.ttest_ind(b.loc[:,x])
    if type=="3":
        x=request.POST['x_value']
        y=request.POST['y_value']
        t=stats.ttest_ind(b.loc[:,x],b.loc[:,y])
    if type=="4":
        x=request.POST['x_value']
        y=request.POST['y_value']
        t=stats.ttest_rel(b.loc[:,x], b.loc[:,y])
    return str(t)
def logistic(d,x,y):
    all_value = x+[y]
    d = d[all_value]
    d=d.dropna()
    if d.shape[0] == 0 :  
        return 400 
    result = sm.Logit(d[y],d[x]).fit()
    result_dict = {}
    result_dict = result.summary().as_html()
    return result_dict

def x_prob(request):
    from scipy import stats
    json=request.POST['jsonObject']
    x=request.POST['x_value']
    df=pd.read_json(json)
    #null값 체크
    
    #정규성검정
    #독립성검정
    #상관분석
    return 0

