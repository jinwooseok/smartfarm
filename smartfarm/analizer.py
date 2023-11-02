from django.shortcuts import render
import pandas as pd
#분석도구들을 모아놓은 파일
import statsmodels.api as sm  
def linear(d,x,y):#회귀분석을 실행. 결과표,분산분석표,상관분석표까지 표현
    from sklearn.model_selection import train_test_split
    from statsmodels.formula.api import ols 
    print(y)
    print(x)

    result = sm.OLS(d[y],d[x]).fit()
    #f_html=result.summary().to_html()
    result_dict = {}
    result_dict = result.summary().as_html()
    # for i, table in enumerate(result.summary().tables):
    #     df = pd.read_html(table.as_html(),header=0)[0]
    #     print(len(df))
    #     for j in range(len(df)):
    #         df.iloc[j,0] = str(df.iloc[j,0]).replace(":", "")
    #         df.iloc[j,2] = str(df.iloc[j,2]).replace(":", "")
                
    #         print(df.iloc[j,0],df.iloc[j,1],df.iloc[j,2],df.iloc[j,3])
    #         result_dict[df.iloc[j,0]] = df.iloc[j,1]
    #         result_dict[df.iloc[j,2]] = df.iloc[j,3]
    # #사후분석
    # print(result_dict)
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

