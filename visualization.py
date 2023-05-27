import pandas as pd
import plotly.graph_objects as go 
import database as db

def monthly_variable_expenditure(month,year):
    df=pd.DataFrame()
    for day in range(1,32):
        if day<10:
            day="0"+str(day)
        date=f"{year}-{month}-{day}"
        if db.get_data(date):
            dict=db.get_data(date)
            df_date=pd.DataFrame(dict,index=[date])
            df = pd.concat([df,df_date],axis=0)
    return  df

def monthly_fixed_income(month,year):
    key = f"income {year}_{month}"
    dict=db.get_data(key)
    income=dict["Salary"] +dict["Other Income"]
    return income
def monthly_fixed_expenditure(month,year):
    key=f"expense {year}_{month}"
    dict=db.get_data(key)
    df=pd.DataFrame(dict,index=[key])
    df.drop(columns=["key"],inplace=True)
    return df

def monthly_fixed_expenditure_sum(month,year):
    key=f"expense {year}_{month}"
    dict=db.get_data(key)
    df=pd.DataFrame(dict,index=[key])
    df.drop(columns=["key"],inplace=True)
    s=df.sum(axis=1)
    sum=s.values[0]
    return sum

print(monthly_variable_expenditure("05",2023))  




