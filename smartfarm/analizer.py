from django.shortcuts import render
import pandas as pd
#분석도구들을 모아놓은 파일
import statsmodels.api as sm  
def linear(d,x,y):#회귀분석을 실행. 결과표,분산분석표,상관분석표까지 표현
    # from sklearn.model_selection import train_test_split
    # import statsmodels.api as sm
    # from statsmodels.formula.api import ols 
    # json=request.POST['jsonObject']
    # x=request.POST.getlist('x_value')
    # y=request.POST['y_value']
    # b=pd.read_json(json)
    # b.columns=[i.replace(' ','') for i in b.columns.values]
    # x_re=[i.replace(' ','') for i in x]
    # xx=b.loc[:,x_re]
    # xx_str=""#y~x를 이용한 ols는 anova_lm도 가능하다.
    # for i in x_re:
    #     if i==x[-1]:
    #         xx_str+=str(i)
    #     else:
    #         xx_str+=(str(i)+"+")

    # model=str(y)+" ~ "+xx_str
    # result = ols(model,data=b).fit()
    corr_html=xx.corr().to_html()
    f_html=sm.stats.anova_lm(result).to_html()
    c_html=result.summary().as_html()+"\n"+corr_html+ "\n"+f_html
    #사후분석
    return c_html

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
def logistic(request):
    x=request.POST.getlist('x_value')
    y=request.POST['y_value']
    json=request.POST['jsonObject']
    b=pd.read_json(json)
    b.columns=[i.replace(' ','') for i in b.columns.values]
    x_re=[i.replace(' ','') for i in x]
    xx=b.loc[:,x_re]
    xx_str=""#y~x를 이용한 ols는 anova_lm도 가능하다.
    for i in x_re:
        if i==x[-1]:
            xx_str+=str(i)
        else:
            xx_str+=(str(i)+"+")

    model=str(y)+" ~ "+xx_str
    lgmodel=sm.Logit.from_formula(model,data=b)
    result=lgmodel.fit().summary()
    return result.as_html()

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

