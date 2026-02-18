import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

#Welcome text
st.write('hello world!')
st.write("Welcome to my mega money analysis!!!!")

#Page setup

st.set_page_config(page_title="John Money's Money Analysis", page_icon="💳", layout="wide")

#Transaction Categorization (Please work)

def categorize_transaction(description, credit) :
    desc = description.upper()
    
    if any (word in desc for word in ['C/C','CREDIT CARD', 'AMEX BILL', 'VISA BILL', 'MASTERCARD BILL', 'CREDIT']):
        return 'Credit Card Payment'

    elif 'DRAFT' in desc:
        return 'Draft'
    
    elif '6125141' in desc:
        return 'SAVINGS'

    elif any (word in desc for word in ['NSLSC', 'OSAP', 'OUAC', 'STUDENT LOAN']):
        return 'Student Loans'

    elif any (word in desc for word in ['CHATR', 'TEKK', 'SAVVY', 'ROGERS', 'TSI', 'EQUIFAX', 'VESTA']):
        return 'Bills'
    
    elif any (word in desc for word in ['FEE', 'NSF', 'INTEREST', 'OVERDRAFT',]) :
        return 'Fees'
    
    elif any (word in desc for word in ['PLANET', 'SPORT CLIPS', 'CUT', 'VISION',]) :
        return 'Self Improvement'
    
    elif 'UBER EAT' in desc or 'UBER*EAT' in desc:
        return 'Dining'
     
    elif any(word in desc for word in ['TIM HORTONS', 'MCDONALD', 'WENDY', 'PIZZA', 'A&W', 'MARY BROWNS', 'BURGER KING', 'SUBWAY', 'CHICKEN', 'KFC', 'STARBUCKS', 'COFFEE', 'DUNKIN', 'DOMINO', 'PIZZA HUT', 'OSMOW', 'BAXTER', 'RAMEN' 'BEANS', 'BIRDS', 'WING','SECORD', 'KUNG PAO', 'WOK', 'POPEYES' ]):
        return 'Dining'
    
    elif any(word in desc for word in ['AMAZON', 'EBAY', 'ALIBABA', 'SHOPIFY', 'AMZN', 'EBAY', 'ALIBABA', 'SHOPIFY']):
        return 'Online Shopping'
    
    elif any(word in desc for word in ['APPLE', 'GOOGLE', 'MICROSOFT', 'SOFTWARE']):
        return 'Tech'
    
    #### Weird spacing below because i wanted it to fit on my screen lol
    elif any(word in desc for word in ['CINEPLEX', 'NETFLIX', 'SPOTIFY', 'DISNEY', 'AMAZON PRIME', 'HULU', 'YOUTUBE', 
                                       'GAMING', 'STEAM' , 'XBOX', 'PLAYSTATION' , 'NINTENDO', 'WEED', 'ALCOHOL', 'CANABIS',
                                         'CANN', 'BEER', 'WINE', 'LIQUOR', 'LCBO', 'DISCORD']):
        return 'Entertainment' 
    
    elif any(word in desc for word in ['ATM', 'WITHDRAWAL', 'DEPOSIT']):
        return 'ATM Transactions'

    elif any(word in desc for word in ['FRESHCO', 'WALMART', 'SHOPPERS', 'DOLLARAMA']):
        return 'Groceries'
    
    elif any(word in desc for word in ['UBER', 'ESSO', 'SHELL']):
        return 'Transport'
    
    elif any(word in desc for word in ['BET365', 'ENDZIN', 'FANDUEL', 'BETWAY', 'DRAFTKINGS', 'GAMBLING']):
        return 'Gambling'
    
    elif any(word in desc for word in ['E-TRANSFER','TFR-', 'TRANSFER', 'INTERAC', 'SEND E-TFR', 'E-TFR']):
        return 'Transfer'
    
    elif (any(word in desc for word in ['PAY','EI', 'EMPL INS']) and pd.notna(credit) and credit != "-" and not any(word in desc for word in [
        'C/C','CREDIT CARD', 'AMEX BILL', 'VISA BILL', 'MASTERCARD BILL', 'CREDIT',
        'E-TRANSFER','E-TFR', 'TRANSFER', 'INTERAC', 'SEND E-TFR', ])):
        return 'PAY'
    
    else:
        return 'Other'



#Function to load transactions and check for errors n shit

def load_transactions(file):
    ####st.subheader("All transactions")   <--- remove hashtags and correct spacing to toggle the main DF being loaded in
    try:
        df = pd.read_csv(file, thousands=',', header=None)  #to read the csv file, skip first 5 rows
        df.columns = ["Date (Y/M/D)", "Transaction Type", "Debit", "Credit","Balance" ]#to add collumn names
        df.columns = [col.strip() for col in df.columns]  #to strip excess white space, (strips whatever in the collums, in the object df.columns (df))                   
  
        df = df.fillna(value= "-") #To fill null values with a dash :)

        ##df['Category'] = df['Transaction Type'].apply(categorize_transaction) #new transaction type line of code
        df['Category'] = df.apply(
            lambda row: categorize_transaction(row['Transaction Type'], row['Credit']),
            axis=1
        )

        return df
    except Exception as e:
        st.error(f"Ayo bruh we got a file processing error: {str(e)}")
        return None


def main():
    st.title("John's Money's Money Analysis")

    st.subheader("Upload your CSV data here!!!")
    uploaded_file = st.file_uploader("info.csv", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)

        if df is not None:
            debits_df = df[df["Debit"].astype(str).str.replace(',', '').str.strip() != "-" ].copy()
            debits_df = debits_df[["Date (Y/M/D)", "Transaction Type", "Category", "Debit", "Balance"]]
            credits_df = df[df["Credit"].astype(str).str.replace(',', '').str.strip() != "-" ].copy()
            credits_df = credits_df[["Date (Y/M/D)", "Transaction Type", "Category", "Credit", "Balance"]]

            #Financial overview sec

            st.header("Financial overview")

            col1,col2,col3 = st.columns(3)

            with col1:
                st.subheader("Outflow breakdown")
                debits_clean = debits_df.copy()
                debits_clean['Debit'] = pd.to_numeric(debits_clean['Debit'].astype(str).str.replace(',', ''), errors='coerce')
                category_totals = debits_clean.groupby('Category')['Debit'].sum().reset_index()
                exclude_list = ['Transfer', 'Other', 'Fees', 'ATM Transactions', 'Draft']
                filtered_data = category_totals[~category_totals['Category'].isin(exclude_list)]
            
                fig =px.pie(filtered_data, names="Category", values="Debit")
                fig.update_traces(hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>')
                st.plotly_chart(fig, use_container_width=True)


                #fig = go.Figure(data=go.Pie(labels=df[Category], values=debits_df)) 

            with col2:
                st.subheader("Cash Inflows")
                credits_clean = credits_df.copy()
                credits_clean['Credit'] = pd.to_numeric(credits_clean['Credit'].astype(str).str.replace(',', ''), errors='coerce')
                category_totals = credits_clean.groupby('Category')['Credit'].sum().reset_index()
                exclude_list1 = ['Transfer', 'Other', 'Fees', 'ATM Transactions', 'Draft', 'Transport']
                filtered_data = category_totals[~category_totals['Category'].isin(exclude_list1)]

                ####PX.BAR USES x= AND y=, PX.PIE USES names= AND values=, REMEMBER THIS

                fig =px.bar(filtered_data, x="Category", y="Credit")
                fig.update_traces(hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>')
                st.plotly_chart(fig, use_container_width=True)

            with col3: 
                st.subheader("temp")

            #2nd row
            col4,col5,col6 = st.columns(3)
            
            with col4:
                st.subheader("temp")
            
            with col5:
                st.subheader("temp")

            with col6:
                st.subheader("temp")

            tab1, tab2, tab3= st.tabs(["Debit (Cash Outflow) Tracker", "Credit (Cash Inflow) Tracker", "Overall Transactions"])
            with tab1:
                st.write(debits_df)
            
            with tab2:
                st.write(credits_df)
            
            with tab3:
                st.write(df)

main()

