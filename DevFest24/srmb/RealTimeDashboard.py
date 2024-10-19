import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import requests
from datetime import datetime

# to open an html page 
def load_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

# Set the page configuration
st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
    layout='wide'
)



# Add custom CSS to change the background color
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #F0F8FF;  /* Change this to your desired background color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Dashboard", "Recommendations", "Financial Report", "Add Expenses","Add Enterprise","Add Revenue"))

if page == "Dashboard":
    st.title("ProfitPath: Real-Time Financial Dashboard")
    st.markdown("#### Monitor your financial metrics in real time! 🔍")

    placeholder = st.empty()

    # Function to fetch data from API
    def fetch_data():
        response_expenses = requests.get('http://localhost:8000/api/depenses/')
        response_revenues = requests.get('http://localhost:8000/api/revenues/')
        return response_expenses, response_revenues

    # Near real-time / live feed simulation
    for seconds in range(200):
        response_expenses, response_revenues = fetch_data()

        if response_expenses.status_code == 200 and response_revenues.status_code == 200:
            # Process Depenses (Expenses)
            depenses_data = response_expenses.json()
            df_depenses = pd.DataFrame(depenses_data)

            # Ensure 'montant' is numeric
            df_depenses['montant'] = pd.to_numeric(df_depenses['montant'], errors='coerce')
            df_depenses = df_depenses.dropna(subset=['montant'])

            # Group by 'type' and sum 'montant'
            expenses_by_category = df_depenses.groupby('type')['montant'].sum().reset_index()
            total_expenses = expenses_by_category['montant'].sum() if not expenses_by_category['montant'].empty else 0.0

            # Process Revenues
            revenues_data = response_revenues.json()
            df_revenues = pd.DataFrame(revenues_data)

            # Ensure 'montant' is numeric
            df_revenues['montant'] = pd.to_numeric(df_revenues['montant'], errors='coerce')
            df_revenues = df_revenues.dropna(subset=['montant'])

            # Group by 'categorie' and sum 'montant'
            revenue_by_category = df_revenues.groupby('categorie')['montant'].sum().reset_index()
            total_revenue = revenue_by_category['montant'].sum() if not revenue_by_category['montant'].empty else 0.0

            # Calculate Cash Flow from Operations, Investment, and Financing for the last 30 days
            today = pd.to_datetime('today').normalize()
            thirty_days_ago = today - pd.DateOffset(days=30)

            # Cash Flow from Operations
            operational_expenses = df_depenses[df_depenses['type_flux_tresorerie'] == 'opérationnelle']
            operational_revenues = df_revenues[df_revenues['type_flux_tresorerie'] == 'opérationnelle']

            operational_expenses['date'] = pd.to_datetime(operational_expenses['date'], errors='coerce')
            operational_expenses_last_30_days = operational_expenses[
                operational_expenses['date'].between(thirty_days_ago, today)
            ]['montant'].sum() if not operational_expenses['montant'].empty else 0.0

            operational_revenues['date'] = pd.to_datetime(operational_revenues['date'], errors='coerce')
            operational_revenues_last_30_days = operational_revenues[
                operational_revenues['date'].between(thirty_days_ago, today)
            ]['montant'].sum() if not operational_revenues['montant'].empty else 0.0

            cash_flow_operational = operational_revenues_last_30_days - operational_expenses_last_30_days

            # Cash Flow from Investment
            investment_expenses = df_depenses[df_depenses['type_flux_tresorerie'] == 'investissement']
            investment_revenues = df_revenues[df_revenues['type_flux_tresorerie'] == 'investissement']

            investment_expenses['date'] = pd.to_datetime(investment_expenses['date'], errors='coerce')
            investment_expenses_last_30_days = investment_expenses[
                investment_expenses['date'].between(thirty_days_ago, today)
            ]['montant'].sum() if not investment_expenses['montant'].empty else 0.0

            investment_revenues['date'] = pd.to_datetime(investment_revenues['date'], errors='coerce')
            investment_revenues_last_30_days = investment_revenues[
                investment_revenues['date'].between(thirty_days_ago, today)
            ]['montant'].sum() if not investment_revenues['montant'].empty else 0.0

            cash_flow_investment = investment_revenues_last_30_days - investment_expenses_last_30_days

            # Cash Flow from Financing
            financing_expenses = df_depenses[df_depenses['type_flux_tresorerie'] == 'financement']
            financing_revenues = df_revenues[df_revenues['type_flux_tresorerie'] == 'financement']

            financing_expenses['date'] = pd.to_datetime(financing_expenses['date'], errors='coerce')
            financing_expenses_last_30_days = financing_expenses[
                financing_expenses['date'].between(thirty_days_ago, today)
            ]['montant'].sum() if not financing_expenses['montant'].empty else 0.0

            financing_revenues['date'] = pd.to_datetime(financing_revenues['date'], errors='coerce')
            financing_revenues_last_30_days = financing_revenues[
                financing_revenues['date'].between(thirty_days_ago, today)
            ]['montant'].sum() if not financing_revenues['montant'].empty else 0.0

            cash_flow_financing = financing_revenues_last_30_days - financing_expenses_last_30_days

            # Calculate Benefice (Profit) for Last 30 Days
            benefice_last_30_days = total_revenue - total_expenses

            # Get only the last 6 records for revenues and expenses, dropping the 'id' column
            df_revenues_last_6 = df_revenues.tail(6).drop(columns=['id'], errors='ignore')
            df_depenses_last_6 = df_depenses.tail(6).drop(columns=['id'], errors='ignore')

            # UI - Display Financial Metrics
            with placeholder.container():
                st.markdown("---")  # Horizontal line for separation
                
                # Key Financial Metrics at the Top
                st.markdown("## 💼 Key Financial Metrics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(label="Cash Flow (Operations) 🔄", value=f"${cash_flow_operational:,.2f}")
                
                with col2:
                    st.metric(label="Cash Flow (Investment) 💸", value=f"${cash_flow_investment:,.2f}")
                
                with col3:
                    st.metric(label="Cash Flow (Financing) 💸", value=f"${cash_flow_financing:,.2f}")
                
                with col4:
                    st.metric(label="Benefice (Profit) 💼", value=f"${benefice_last_30_days:,.2f}")

                st.markdown("---")  # Horizontal line for separation

                # First Row: Revenue & Expenses Overview
                st.markdown("## 💰 Financial Overview")
                col5, col6 = st.columns(2)

                with col5:
                    st.metric(label="Total Revenue 💰", value=f"${total_revenue:,.2f}")
                    st.markdown("#### Revenues by Category")
                    fig_revenues = px.pie(
                        revenue_by_category,
                        names='categorie',
                        values='montant',
                        title='Revenues by Category',
                        color='categorie',
                        color_discrete_sequence=px.colors.qualitative.Pastel1,
                        hole=0.3,
                        labels={'montant': 'Amount', 'categorie': 'Revenue Category'},
                        hover_data=['montant'],
                    )
                    fig_revenues.update_traces(textinfo='percent+label', textfont_size=12)
                    fig_revenues.update_layout(margin=dict(l=100, r=100, t=100, b=100))
                    st.plotly_chart(fig_revenues, use_container_width=True, key=f'fig_revenues_{seconds}')  # Unique key
                    st.markdown("---")  # Horizontal line for separation
                    
                # First Row: Revenue & Expenses Overview
                    st.markdown("## 💶 Last Transactions ")
                    # Table for last 6 Revenues
                    st.markdown("### Last 6 Revenues:")
                    st.table(df_revenues_last_6)

                with col6:
                    st.metric(label="Total Expenses 📉", value=f"${total_expenses:,.2f}")
                    st.markdown("#### Expenses by Category")
                    fig_expenses = px.pie(
                        expenses_by_category,
                        names='type',
                        values='montant',
                        title='Expenses by Category',
                        color='type',
                        color_discrete_sequence=px.colors.qualitative.Pastel2,
                        hole=0.3,
                        labels={'montant': 'Amount', 'type': 'Expense Type'},
                        hover_data=['montant'],
                    )
                    fig_expenses.update_traces(textinfo='percent+label', textfont_size=12)
                    fig_expenses.update_layout(margin=dict(l=100, r=100, t=100, b=100))
                    st.plotly_chart(fig_expenses, use_container_width=True, key=f'fig_expenses_{seconds}')  # Unique key

                    # Table for last 6 Expenses
                    st.markdown("---")  # Horizontal line for separation

                # First Row: Revenue & Expenses Overview
                    st.markdown("##  ")
                    st.markdown("### Last 6 Expenses:")
                    st.table(df_depenses_last_6)

        time.sleep(1)

elif page == "Recommendations":
    st.title("Recommendations")
    st.markdown("### Suggestions to improve financial health will be displayed here.")
    # Include your recommendation logic here

elif page == "Financial Report":
    st.title("Financial Report")
    st.markdown("### Detailed financial report will be generated here.")
    # Include your financial report logic here

elif page == "Add Expenses":
    st.title("Add Expenses")
    st.markdown("### Enter the details of the new expense below:")

    # Create a form for adding expenses
    with st.form(key='expense_form'):
        # Fixed values
        entreprise = 1  # Always set to 1
       
        # User inputs
        expense_type = st.selectbox("Type of Expense", ["Dépenses d'exploitation", "Salaires", "Loyer", "Impôts et taxes", "Dépenses financières", "autre"])
        type_flux_tresorerie = st.selectbox("Type of Cash Flow", ["opérationnelle" ,"investissement","financement"])  # Select from choices
        amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
        description = st.text_input("Description")
        date = st.date_input("Date", value=datetime.today())
        
        # Submit button
        submit_button = st.form_submit_button(label='Add Expense')

        if submit_button:
            # Prepare data to send
            expense_data = {
                'entreprise': entreprise,  # Always set to 1
                'type': expense_type,
                'type_flux_tresorerie': type_flux_tresorerie,  # User-selected value
                'montant': f"{amount:.2f}",  # Format amount to 2 decimal places
                'date': str(date),  # Convert date to string
                'description': description
            }
            # Send POST request to API
            response = requests.post('http://localhost:8000/api/add-depenses/', json=expense_data)

            if response.status_code == 201:
                st.success("Expense added successfully!")
            else:
                st.error(f"Error adding expense: {response.json()}")


elif page == "Add Enterprise":
    st.title("Add Enterprise")
    st.markdown("### Enter the details of the new enterprise below:")

    # Create a form for adding an enterprise
    with st.form(key='enterprise_form'):
        # User inputs
        name = st.text_input("Enterprise Name")
        address = st.text_input("Address")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")

        # Submit button
        submit_button = st.form_submit_button(label='Add Enterprise')

        if submit_button:
            # Prepare data to send
            enterprise_data = {
                'name': name,
                'address': address,
                'email': email,
                'phone': phone
            }
            # Send POST request to your API
            response = requests.post('http://localhost:8000/api/add-entreprise/', json=enterprise_data)

            if response.status_code == 201:
                st.success("Enterprise added successfully!")
            else:
                st.error(f"Error adding enterprise: {response.json()}")


elif page == "Add Revenue":
    st.title("Add Revenue")
    st.markdown("### Enter the details of the revenue below:")

    # Create a form for adding revenue
    with st.form(key='revenue_form'):
        # User inputs
        entreprise = 1  # Always set to 1
        expense_type = st.selectbox("Type of Expense", ["Dépenses d'exploitation", "Salaires", "Loyer", "Impôts et taxes", "Dépenses financières", "autre"])
        type_flux_tresorerie = st.selectbox("Type of Cash Flow", ["opérationnelle" ,"investissement","financement"])  # Select from choices

        montant = st.number_input("Montant", min_value=0.0, format="%.2f")
        date = st.date_input("Date", value=pd.to_datetime("today"))
        categorie = st.selectbox("Catégorie", ['Vente', 'Service', 'Autre'])
        description = st.text_area("Description", "")

        # Submit button
        submit_button = st.form_submit_button(label='Add Revenue')

        if submit_button:
            # Prepare data to send
            revenue_data = {
               
                'entreprise': entreprise,  # Always set to 1
                'type': expense_type,
                'type_flux_tresorerie': type_flux_tresorerie, 
                'montant': montant,
                'date': str(date),  # Convert date to string
                'categorie': categorie,
                'description': description,
                 # Fixed type
            }
            # Send POST request to your API
            response = requests.post('http://localhost:8000/api/add-revenue/', json=revenue_data)

            if response.status_code == 201:
                st.success("Revenue added successfully!")
            else:
                st.error(f"Error adding revenue: {response.json()}")







