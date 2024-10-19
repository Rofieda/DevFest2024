import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import requests

# Streamlit Page Configuration
st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
    layout='wide'
)

# Title and Subheader
st.title("ProfitPath: Real-Time Financial Dashboard")
st.markdown("#### Monitor your financial metrics in real time! 🔍")

# Creating a single-element container for updates
placeholder = st.empty()

# Function to fetch data from API
def fetch_data():
    response_expenses = requests.get('http://localhost:8000/api/depenses/')  # Change this URL as needed
    response_revenues = requests.get('http://localhost:8000/api/revenues/')  # Endpoint for revenue data
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

                # Table for last 6 Revenues
                st.markdown("#### Last 6 Revenues")
                st.dataframe(df_revenues_last_6)

            with col6:
                st.metric(label="Total Expenses 💰", value=f"${total_expenses:,.2f}")
                st.markdown("#### Expenses by Category")
                fig_expenses = px.pie(
                    expenses_by_category,
                    names='type',
                    values='montant',
                    title='Expenses by Category',
                    color='type',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    hole=0.3,
                    labels={'montant': 'Amount', 'type': 'Expense Type'},
                    hover_data=['montant'],
                )
                fig_expenses.update_traces(textinfo='percent+label', textfont_size=12)
                fig_expenses.update_layout(margin=dict(l=100, r=100, t=100, b=100))
                st.plotly_chart(fig_expenses, use_container_width=True, key=f'fig_expenses_{seconds}')  # Unique key

                # Table for last 6 Expenses
                st.markdown("#### Last 6 Expenses")
                st.dataframe(df_depenses_last_6)

    # Sleep to mimic real-time updates
    time.sleep(5)  # Update every 5 seconds
