import calendar
from datetime import datetime
import plotly.graph_objects as go 
import streamlit as st
from streamlit_option_menu import option_menu  
import pandas as pd
import database as db  # local import
import visualization as  viz #local import
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

#--------Authentication--------

#with open("/home/niranjan/Desktop/my_projects/config.yaml") as file:
config = db.get_data("passcode") # retriving user data from database
del config["key"]
incomes = ["Salary", "Other Income"]
Fixed_Expense=["Rent","Electricity","Home Loan","LIC Premium","Fitness"]
Variable_Expense=["Swiggy-Zomato","Medical","Other",
                "Daily Office Expense", "Groceries", "Bike-refuel"
                ,"Mobile Recharge","Gas Cylinder","Family","Luxury Purchases"]
currency = "Rs"
page_title = "Income and Expense Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---

years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])
charts=["pie chart","bar chart","scatter plot","Mothly data"]
default_salary=90000

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

    # ----STREAMLIT STYLE ---
hide_st_style = """<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}header {visibility: hidden;}</style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)
name,authentication_status,username=authenticator.login("login","main")

if authentication_status==False:
    st.error("Username/password is incorrect")
if authentication_status==None:
    st.warning("Please enter your username and password")
if authentication_status:




    # -------------- SETTINGS --------------

    authenticator.logout("Logout","sidebar")
    st.sidebar.title(f"Welcome {name}")


#--------------------Main program-------




    #-------------SETTING OPTION MENU--------

    selected = option_menu(
        menu_title=None,
        options=["Monthly Income","Daily Expenditure", "Data Visualization"],
        icons=["pencil-fill", "pencil-fill","bar-chart-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal")

    #---------------------Filling Form Field For Income----------------------------
    if selected=="Monthly Income":
        st.header(f"Fixed Monthly Income & Expenditure")
        with st.form("Fixed Monthly Income & Expenditure"):
            col1, col2 = st.columns(2)
            col1.selectbox("Select Month:", months, key="month")
            col2.selectbox("Select Year:", years, key="year")

            "---"
            with st.expander("Monthly Income"):
                selected_salary = st.number_input(f"{incomes[0]}:",value=default_salary,
                                                min_value=None,max_value=None,step=None,key=incomes[0])
                st.write("You selected:", selected_salary )
                st.number_input(f"{incomes[1]:}",value=0,key=incomes[1])
            with st.expander("Fixed Monthly Expenditure"):
                for expense in Fixed_Expense:
                    st.number_input(f"{expense}:", min_value=0, step=10, key=expense)


            "---"
            submitted = st.form_submit_button("Save Data")
            if submitted:
                period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
                incomes = {income: st.session_state[income] for income in incomes}
                Fixed_Expense={expense:st.session_state[expense] for expense in Fixed_Expense}
                db.insert_field_db(f"income {period}",incomes)# Inserting in to database
                db.insert_field_db(f"expense {period}",Fixed_Expense) # Inserting in to database 
                st.success("Data saved!")

    #-----------------------Filling Form Field For Expenditure-------------
    if selected=="Daily Expenditure":
        st.header(f"Data entry in currenct {currency}")
        with st.form("entry_form",clear_on_submit=True):
            selected_date = st.date_input("Select a date",key="date")
            with st.expander("Variable Expenditure"):
                for expense in Variable_Expense:
                    st.number_input(f"{expense}:", min_value=0, step=10, key=expense)
            with st.expander("Comment"):
                comment = st.text_area("", placeholder="Enter a comment here ...")

            "---"
            if st.form_submit_button("Save Data"):
                date= st.session_state["date"]
                Variable_Expense={expense:st.session_state[expense] for expense in Variable_Expense}
                db.insert_field_db(str(date),Variable_Expense) # insering in to database
                st.success("Data saved!")

    #----------------Visualization------------------
    if selected=="Data Visualization":
        st.header("Chart")
        with st.form("Viz"):
            col1, col2 = st.columns(2)
            col1.selectbox("Select Month:", months, key="Month")
            col2.selectbox("Select Year:", years, key="Year")
            if st.form_submit_button("Save Data"):
                month=st.session_state["Month"]
                month_index=months.index(month)+1
                if month_index < 10:
                    month_index="0"+str(month_index)
                year=st.session_state["Year"]
                df=viz.monthly_variable_expenditure(month_index,year)
                df1=df.drop(columns=["key"])
                s=df1.sum()
                Variable_Expense_total=sum(s.values)
                s=s.sort_values(ascending=False)
#----------------------------------Summary---------------------
                monthly_fixed_expense=viz.monthly_fixed_expenditure_sum(month,year)
                monthly_income=viz.monthly_fixed_income(month,year)
                monthly_savings=monthly_income-(monthly_fixed_expense+Variable_Expense_total)
                st.write(f'Income earned: Rs.{monthly_income}\n Fixed expense: Rs.{monthly_fixed_expense}\n Variable expense: Rs.{Variable_Expense_total}\n Savings: Rs.{monthly_savings}')
                tab1, tab2 = st.tabs(["Bar chart", "Pie chart"])
                with tab1:
                    fig = go.Figure(go.Bar(x=s.index, y=s.values,name='Monthly Variable Expenditure'))
                    fig.update_layout(title='Monthly Expenses')
                    st.plotly_chart(fig)
                with tab2:
                    fig = go.Figure(go.Pie(labels=s.index, values=s.values,name='Monthly Variable Expenditure'))
                    fig.update_layout(title='Monthly Expenses')
                    st.plotly_chart(fig)
    #-----------------------------------------------
                tab1,tab2=st.tabs(["Scatter Plot","Monthly Data"])
                with tab1:
                    # create scatter plot
                    fig = go.Figure()
                    for column in df1.columns:
                        fig.add_trace(go.Scatter(x=df1.index, y=df1[column], mode='markers', name=column))

                        # add title and axis labels
                    fig.update_layout(title='Daily Expenses',
                        xaxis_title='Date',
                        yaxis_title='Amount (Rs)')
                    st.plotly_chart(fig)
                with tab2:
                    st.dataframe(df1)
#-----------------------------------------------



