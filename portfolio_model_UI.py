import streamlit as st
import pandas as pd
import pickle
import warnings
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os
from datetime import date
import random
import yfinance as yf

warnings.filterwarnings('ignore')

st.title('Options Model')
st.header('We will predict future option price')

def scrap_options_data(company_name, link_dict, types):
    link_company = link_dict[company_name]
    # Define the company dictionary with company name and link
    company = {company_name: link_company}
    service = Service(ChromeDriverManager().install())

    # Initialize WebDriver with the service object
    driver = webdriver.Chrome(service=service)
    for indicator, link in company.items():

        try:
            driver.get(link)

            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[starts-with(@id, 'showMore')]")))
            # Check if the element is visible


            while element.is_displayed() : 
                element.click()
                #print('Clicked')
            else:
                print('End of ', indicator)

        except WebDriverException as e:
            # Handle the exception
            print("An error occurred:", '-----------------------------------------------------')

        soup = bs(driver.page_source, 'html.parser')
        table = soup.find_all('table')[1]

    # Find expiration date elements
    expiration_date_elements = driver.find_elements(By.ID, "selectDate")

    # Extract expiration dates
    expiration_dates = []
    for element in expiration_date_elements:
        expiration_dates.append(element.text)

    # # Iterate and select expiration dates
    # for expiration_date in expiration_dates:
    #     select.select_by_visible_text(expiration_date)



    expiration_dates

    # Print the extracted expiration dates
    for expiration_date in expiration_dates:
        print(expiration_date )

    expiration_date
    if(types=='Call'):
        selected_type = 'Calls'
        first_name = f'{company_name} {types} '
        second_name = f'Symbol{company_name}'
        delta = "CDelta"
    else:
        selected_type = 'Puts'
        first_name =  f'{company_name} {types} '
        second_name = f'Symbol{company_name}'
        delta = 'PDelta'
    dropdown = driver.find_element(By.ID, "selectShow")
    # Create a Select object
    select = Select(dropdown)
    select.select_by_visible_text(selected_type)

    dropdown = driver.find_element(By.ID, "selectStrike")
    select = Select(dropdown)
    select.select_by_visible_text('All')

    dropdown = driver.find_element(By.ID, "selectDate")
    select = Select(dropdown)

    try:
        
        options = select.options
        data = []
        for option in options:
            select.select_by_visible_text(option.text)
            soup = bs(driver.page_source, 'html.parser')
            table = soup.find_all('table')[1]
            # Extract the table headers
            headers = table.find_all('th')
            column_names = [header.get_text(strip=True) for header in headers]

                    # Extract the table data into a list of lists
            for row in table.find_all('tr'):
                row_data = [cell.get_text(strip=True) for cell in row.find_all('td')]
                if row_data:
                    data.append(row_data)
            # Create the DataFrame
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    print(cell.text)


        df = pd.DataFrame(data, columns=column_names)
        print("______________________________________________________________________________________First_try")
    except Exception as e:
        options = select.options
        data = []
        for option in options:
            select.select_by_visible_text(option.text)
            soup = bs(driver.page_source, 'html.parser')
            table = soup.find_all('table')[1]
            # Extract the table headers
            headers = table.find_all('th')
            column_names = [header.get_text(strip=True) for header in headers]

                    # Extract the table data into a list of lists
            for row in table.find_all('tr'):
                row_data = [cell.get_text(strip=True) for cell in row.find_all('td')]
                if row_data:
                    data.append(row_data)
            # Create the DataFrame
            for row in table.find_all('tr'):
                for cell in row.find_all('td'):
                    print(cell.text)


        df = pd.DataFrame(data, columns=column_names)
        print("______________________________________________________________________________________Second_try")

    df['Symbol'] = df['Symbol'].fillna('NaN')
    df = df[~df['Symbol'].str.contains('Price @')]

    df.to_csv('company_option.csv',index=False)

    df_1=pd.read_csv("company_option.csv")
    df=df_1

    first_column = df.iloc[:, 0]
    print(first_column)

    first_row = first_column.iloc[-1]
    print(first_row)

    first_row = first_row.split(sep=".", maxsplit=1)[1]
    print(first_row[6:18])

    n=len(first_column)
    print(n)

    EXP_Date = { "Exp_date": [], }

    for i in range(1, n, 2):
        first_row = first_column.iloc[i]
        first_row = first_row.split(sep=".", maxsplit=1)[1]
        data=first_row[6:18]
    #     data=first_row[20:32]
        EXP_Date["Exp_date"].append(data)
    print(EXP_Date)


    for key, value in EXP_Date.items():
      print(f" {key}: {len(value)}")

    data_df_1 = {
      first_name: [],
      delta: [],
      "Imp Vol": [],
      "Bid": [],
      "Gamma": [],
      "Theoretical":[],
      "Ask": [],
      "Theta": [],
      "Intrinsic Value": [],
        "Volume":[],
      "Vega": [],
      "Time Value": [],
        "Open Interest":[],
        "Rho":[],
      " Theta": [],

        "Exp":[],
        "Mar ":[],
        "Apr ":[],
        "May ":[],
        "Jun ":[],
        "Jul ":[],
        "Aug ":[],
        "Sep ":[],
        "Oct ":[],
        "Nov ":[],
        "Dec ":[],
        "Jan ":[],
        'Feb ':[],

        "Chg":[],
        second_name:[],
        "Delta ":[],
        " ":[],
        "Last":[],


    }


    for i in range(1, n, 2):
        data = first_column[i]
        matches = re.findall(r'([A-Za-z\s]+)(?:(-?[\d.]+))', data)
        print("\n")


        for match in matches:
            print(match[0], match[1])
            data_df_1[match[0]].append(match[1])

    value = data_df_1.get("Theta")
    del data_df_1[" Theta"]
    data_df_1["Delta/Theta"] = value

    for key, value in data_df_1.items():
      print(f" {key}: {len(value)}")


    for key, value in data_df_1.items():
        if len(value) != len(list(data_df_1.values())[0]):
            if len(value) > len(list(data_df_1.values())[0]):
                value = value[:len(list(data_df_1.values())[0])]
            else:
                value.extend([None] * (len(list(data_df_1.values())[0]) - len(value)))

    new_df = pd.DataFrame.from_dict(data_df_1)

    for i in range(len(df)):
          if i % 2 == 1:
            df.drop(index=i, inplace=True )

    df = df.drop(['Ask','Volume','Open Interest','Bid'], axis=1)

    df.to_csv('symbol.csv')

    new_df = new_df.assign(**EXP_Date)
    new_df = new_df.drop(['Delta ','Chg',second_name,' ','Exp','Mar ',"Apr ",
        "May ","Jun ","Jul ","Aug ","Sep ","Oct ","Nov ","Dec ","Jan ","Feb ",first_name,"Last"], axis=1)

    new_df.to_csv('exp.csv')

    sympol = pd.read_csv("symbol.csv")
    sympol = sympol.drop(['Unnamed: 0'], axis=1)
    exp = pd.read_csv("exp.csv")
    exp = exp.drop(['Unnamed: 0'], axis=1)

    final_df= pd.concat([sympol, exp], axis=1)
    final_df = final_df.rename(columns={'Chg.': 'Chg', 'CDelta': 'Delta', 'PDelta': 'Delta'})
    today_date = date.today()
    final_df['Date'] = today_date
    final_df['option_type'] = types
    final_df['Exp_date'] = pd.to_datetime(final_df['Exp_date'])
    final_df['Date'] = pd.to_datetime(final_df['Date'])

    os.remove('symbol.csv')
    os.remove('exp.csv')
    os.remove('company_option.csv')
    driver.quit()
    return final_df

link_dict = {
    'AAPL': 'https://www.investing.com/equities/apple-computer-inc-options',
    'ADBE': 'https://www.investing.com/equities/adobe-sys-inc-options',
    'AEYE': 'https://www.investing.com/equities/second-sight-medical-products-options',
    'AMD': 'https://www.investing.com/equities/adv-micro-device-options',
    'AMZN': 'https://www.investing.com/equities/amazon-com-inc-options',
    'ANET': 'https://www.investing.com/equities/arista-networks-options',
    'ARKG': 'https://www.investing.com/etfs/ark-genomic-revolution-options',
    'ARKK': 'https://www.investing.com/etfs/ark-innovation-options',
    'ASML': 'https://www.investing.com/equities/asml-holdings-options',
    'BILL': 'https://www.investing.com/equities/bill.com-options',
    'CELH': 'https://www.investing.com/equities/celsius-holdings-options',
    'CMG': 'https://www.investing.com/equities/chipotle-mexican-grill-options',
    'COIN': 'https://www.investing.com/equities/coinbase-global-options',
    'COST': 'https://www.investing.com/equities/costco-whsl-options',
    'CRM': 'https://www.investing.com/equities/salesforce-com-options',
    'CRWD': 'https://www.investing.com/equities/crowdstrike-holdings-options',
    'CYBR': 'https://www.investing.com/equities/cyberark-options',
    'DDOG': 'https://www.investing.com/equities/datadog-options',
    'DKNG': 'https://www.investing.com/equities/draftkings-inc-options',
    'DT': 'https://www.investing.com/equities/dynatrace-options',
    'ELF': 'https://www.investing.com/equities/elf-beauty-options',
    'FTI': 'https://www.investing.com/equities/technipfmc-options',
    'FTNT': 'https://www.investing.com/equities/fortinet-options',
    'GOOGL': 'https://www.investing.com/equities/google-inc-options',
    'GTEK': 'https://www.investing.com/etfs/tekla-healthcare-investors-options',
    'HUBS': 'https://www.investing.com/equities/hubspot-options',
    'INTC': 'https://www.investing.com/equities/intel-corp-options',
    'KLAC': 'https://www.investing.com/equities/kla-tencor-options',
    'LCID': 'https://www.investing.com/equities/lucid-group-options',
    'LLY': 'https://www.investing.com/equities/lilly-eli-options',
    'LPLA': 'https://www.investing.com/equities/lpl-financial-options',
    'MA': 'https://www.investing.com/equities/mastercard-inc-options',
    'MELI': 'https://www.investing.com/equities/mercadolibre-options',
    'META': 'https://www.investing.com/equities/facebook-inc-options',
    'MLTX': 'https://www.investing.com/equities/molecular-templates-options',
    'MRVL': 'https://www.investing.com/equities/marvell-tech-group-options',
    'MSFT': 'https://www.investing.com/equities/microsoft-corp-options',
    'MSI': 'https://www.investing.com/equities/motorola-solutions-options',
    'NIO': 'https://www.investing.com/equities/nio-inc-options',
    'NVDA': 'https://www.investing.com/equities/nvidia-corp-options',
    'ORCL': 'https://www.investing.com/equities/oracle-corp-options',
    'OXY': 'https://www.investing.com/equities/occidental-petroleum-options',
    'PANW': 'https://www.investing.com/equities/palo-alto-networks-options',
    'PATH': 'https://www.investing.com/equities/uipath-options',
    'RBLX': 'https://www.investing.com/equities/roblox-corp-options',
    'RIVN': 'https://www.investing.com/equities/rivian-automotive-options',
    'ROIV': 'https://www.investing.com/equities/roivant-sciences-options',
    'ROKU': 'https://www.investing.com/equities/roku-options',
    'SMCI': 'https://www.investing.com/equities/super-micro-computer-options',
    'SMH': 'https://www.investing.com/etfs/van-eck-vectors-semiconductor-etf-options',
    'SOUN': 'https://www.investing.com/equities/soundhound-ai-options',
    'SPCE': 'https://www.investing.com/equities/virgin-galactic-options',
    'SQ': 'https://www.investing.com/equities/square-inc-options',
    'SYM': 'https://www.investing.com/equities/symbotic-options',
    'TEAM': 'https://www.investing.com/equities/atlassian-corp-options',
    'TSLA': 'https://www.investing.com/equities/tesla-motors-options',
    'TSM': 'https://www.investing.com/equities/taiwan-semiconductor-options',
    'TWLO': 'https://www.investing.com/equities/twilio-options',
    'U': 'https://www.investing.com/equities/unity-software-options',
    'UBER': 'https://www.investing.com/equities/uber-technologies-options',
    'UNH': 'https://www.investing.com/equities/unitedhealth-group-options',
    'V': 'https://www.investing.com/equities/visa-inc-options',
    'VKTX': 'https://www.investing.com/equities/viking-therapeutics-options',
    'VRT': 'https://www.investing.com/equities/vertiv-options',
    'WDAY': 'https://www.investing.com/equities/workday-options',
    'XLE': 'https://www.investing.com/etfs/spdr-energy-select-sector-options',
    'XLF': 'https://www.investing.com/etfs/spdr-financial-select-sector-options',
    'ZM': 'https://www.investing.com/equities/zoom-video-communications-options',
    'ARM': 'https://www.investing.com/equities/arm-holdings-options',
    'AVGO': 'https://www.investing.com/equities/avago-tech-options',
    'LRCX': 'https://www.investing.com/equities/lam-research-options',
    'MARA': 'https://www.investing.com/equities/marathon-digital-options',
    'MSTR': 'https://www.investing.com/equities/microstrategy-options',
    'MU': 'https://www.investing.com/equities/micron-tech-options',
    'NFLX': 'https://www.investing.com/equities/netflix-options',
    'NOW': 'https://www.investing.com/equities/servicenow-options',
    'QCOM': 'https://www.investing.com/equities/qualcomm-options',
    'RIOT': 'https://www.investing.com/equities/riot-blockchain-options'
}

def designPortfolio(resulted_df, company_name, types,current_invest):
    if resulted_df.empty:
        print('The DataFrame is empty')
        return pd.DataFrame()
    
    df = resulted_df.copy() 
    # Use predicted future points instead of actual future points for decision-making
    Current_point = list(df['Option_price'])
    predicted_future_point = list(df['future_option_price'])  # You can change to the required week
    Stock_price = list(df['Stock_price'])
    Strike = list(df['Strike_Price'])
    option_type = list(df['Option_type'])
    Exp_date = list(df['Exp_date'])
    delta = list(df['delta'])
    theta = list(df['theta'])
    rho = list(df['rho'])
    
    model_decision = []
    resulted_op_money = []
    resulted_op_shares = []
    rest_op_money = []
    N_shares = []
    commission = []
    sp_portfolio = []
    
    teade_yet = False
    starting = True
    starting_cashs = current_invest

    for c, p, s, o in zip(Current_point, predicted_future_point, Strike, option_type):
        # Default values in case no conditions are met
        default_money = 0
        default_shares = 0
        default_portfolio = starting_cashs

        # Buy operation at the start
        if starting:
            starting_cash, _, starting_shares = buy_operation(starting_cashs, c)
            starting = False

        # Simulate the decision-making based on predictions
        if teade_yet:
            last_decision = model_decision[-1] if model_decision else None
            if p >= c:
                if last_decision == f'BUY_{o}' or last_decision == f'HOLD_{o}':
                    model_decision.append(f'HOLD_{o}')
                    prev_shares = N_shares[-1]
                    commission.append(0)
                    resulted_op_money.append(prev_shares * c + rest_op_money[-1])
                    resulted_op_shares.append(prev_shares * c)
                    N_shares.append(prev_shares)
                    sp_portfolio.append(prev_shares * c)
                    rest_op_money.append(rest_op_money[-1] if rest_op_money else default_money)
                else:
                    model_decision.append(f'BUY_{o}')
                    traded_money, rest_money, n_shares = buy_operation(resulted_op_money[-1], c)
                    resulted_op_money.append(n_shares * c + rest_money)
                    resulted_op_shares.append(n_shares * c)
                    rest_op_money.append(rest_money)
                    N_shares.append(n_shares)
                    sp_portfolio.append(n_shares * c)
                    commission.append(max(n_shares * 0.01, 3.5))
            elif p <= c:
                if last_decision == f'SELL_{o}' or last_decision == f'SKIP_{o}':
                    model_decision.append(f'SKIP_{o}')
                    commission.append(0)
                    resulted_op_money.append(resulted_op_money[-1])
                    resulted_op_shares.append(resulted_op_shares[-1])
                    N_shares.append(N_shares[-1])
                    sp_portfolio.append(sp_portfolio[-1])
                    rest_op_money.append(rest_op_money[-1] if rest_op_money else default_money)
                else:
                    model_decision.append(f'SELL_{o}')
                    prev_shares = N_shares[-1]
                    resulted_op_money.append(prev_shares * c + rest_op_money[-1])
                    resulted_op_shares.append(prev_shares * c)
                    rest_op_money.append(rest_op_money[-1])
                    N_shares.append(0)
                    sp_portfolio.append(prev_shares * c)
                    commission.append(max(n_shares * 0.01, 3.5))
        else:
            if p > c:
                teade_yet = True
                model_decision.append(f'BUY_{o}')
                traded_money, rest_money, n_shares = buy_operation(starting_cashs, c)
                resulted_op_money.append(n_shares * c + rest_money)
                resulted_op_shares.append(n_shares * c)
                rest_op_money.append(rest_money)
                N_shares.append(n_shares)
                sp_portfolio.append(n_shares * c)
                commission.append(max(n_shares * 0.01, 3.5))
            else:
                model_decision.append(f'SKIP_{o}')
                resulted_op_money.append(starting_cashs)
                resulted_op_shares.append(default_shares)
                commission.append(0)
                N_shares.append(default_shares)
                sp_portfolio.append(default_portfolio)
                rest_op_money.append(default_money)


    
    data = {
        'Date': df['Date'],
        'C_point': Current_point, 
        'PN_point': predicted_future_point,
        'Strike': Strike,
        'options': option_type,
        'Exp_date': Exp_date,
        'delta': delta,
        'theta': theta,
        'rho': rho,
        'Model-Decision': model_decision,
        'resulted_op_money': resulted_op_money,
        'rest_op_money': rest_op_money,
        'resulted_op_shares': resulted_op_shares,
        'N_shares': N_shares,
        'commission': commission,
        'portfolio': sp_portfolio
    }

    # Check lengths
    for key, value in data.items():
        print(f"{key}: {len(value)} : {value}")
    
    porto_df = pd.DataFrame(data)
    return porto_df


def buy_operation(cash, current_price):
    try:
        n_shares = (cash // current_price)
    except ZeroDivisionError:
        # Handle the case where current_price is zero
        return 0, cash, 0
    n_shares_adjusted = n_shares - (n_shares % 100)  # Adjust n_shares to be divisible by 100
    traded_money = n_shares_adjusted * current_price
    rest_money = cash - traded_money
    return traded_money, rest_money, n_shares_adjusted

def get_str(df,ron):
    df_call1_filtered = df.iloc[ron]
    strike = df_call1_filtered['Strike_Price']
    Exp_date = df_call1_filtered['Exp_date'].strftime('%Y-%m-%d')  # Ensure the date is formatted
    return strike, Exp_date

def test_portfolio(df, company_name, current_invest):
    # Initialize empty DataFrames for final results
    final_df_call_IN = pd.DataFrame()
    final_df_call_OUT = pd.DataFrame()
    final_df_call_NEAR = pd.DataFrame()

    # Get row numbers based on the first week's data to ensure they're calculated only once
    df_week1 = df['week1']
    df_call_IN_week1 = df_week1[(df_week1['Strike_Price'] < ((df_week1['Stock_price'][0]) - 80))]
    df_call_OUT_week1 = df_week1[(df_week1['Strike_Price'] > ((df_week1['Stock_price'][0]) + 80))]
    df_call_NEAR_week1 = df_week1[(df_week1['Strike_Price'] > ((df_week1['Stock_price'][0]) - 80)) & 
                                  (df_week1['Strike_Price'] < ((df_week1['Stock_price'][0]) + 80))]

    # Check if each filtered DataFrame is non-empty before getting row numbers
    row_number_in = random.randint(0, len(df_call_IN_week1) - 5) if not df_call_IN_week1.empty else None
    row_number_out = random.randint(0, len(df_call_OUT_week1) - 5) if not df_call_OUT_week1.empty else None
    row_number_near = random.randint(0, len(df_call_NEAR_week1) - 5) if not df_call_NEAR_week1.empty else None
    print(row_number_in)
    print(row_number_out)
    print(row_number_near)

    # Loop through each week's DataFrame in df
    for week in range(1, len(df) + 1):
        # Access the week's DataFrame
        df_week = df[f'week{week}']

        # Filter the IN, OUT, and NEAR options
        df_call_IN_week = df_week[(df_week['Strike_Price'] < (df_week['Stock_price'][0] - 80))]
        df_call_OUT_week = df_week[(df_week['Strike_Price'] > (df_week['Stock_price'][4] + 80))]
        df_call_NEAR_week = df_week[(df_week['Strike_Price'] > df_week['Stock_price'][2] - 80) & 
                                    (df_week['Strike_Price'] < df_week['Stock_price'][3] + 80)]
        df_call_IN_week = df_call_IN_week.reset_index(drop=True)
        df_call_OUT_week = df_call_OUT_week.reset_index(drop=True)
        df_call_NEAR_week = df_call_NEAR_week.reset_index(drop=True)
        # Get consistent strike and expiration date for each filtered DataFrame
        if row_number_in is not None:
            strike_in, Exp_date_in = get_str(df_call_IN_week, row_number_in)
            df_call_IN_week = df_call_IN_week[(df_call_IN_week['Strike_Price'] == strike_in) & 
                                              (df_call_IN_week['Exp_date'] == Exp_date_in)]
            # Select only the row that matches row_number_in
            df_call_IN_week = df_call_IN_week.loc[[row_number_in]]
            final_df_call_IN = pd.concat([final_df_call_IN, df_call_IN_week], axis=0)

        if row_number_out is not None:
            strike_out, Exp_date_out = get_str(df_call_OUT_week, row_number_out)
            df_call_OUT_week = df_call_OUT_week[(df_call_OUT_week['Strike_Price'] == strike_out) & 
                                                (df_call_OUT_week['Exp_date'] == Exp_date_out)]
            # Select only the row that matches row_number_out
            df_call_OUT_week = df_call_OUT_week.loc[[row_number_out]]
            final_df_call_OUT = pd.concat([final_df_call_OUT, df_call_OUT_week], axis=0)

        if row_number_near is not None:
            strike_near, Exp_date_near = get_str(df_call_NEAR_week, row_number_near)
            df_call_NEAR_week = df_call_NEAR_week[(df_call_NEAR_week['Strike_Price'] == strike_near) & 
                                                  (df_call_NEAR_week['Exp_date'] == Exp_date_near)]
            # Select only the row that matches row_number_near
            df_call_NEAR_week = df_call_NEAR_week.loc[[row_number_near]]
            final_df_call_NEAR = pd.concat([final_df_call_NEAR, df_call_NEAR_week], axis=0)
            
#             final_df_call_NEAR = final_df_call_NEAR[final_df_call_NEAR.index == row_number_near]

    # Add additional columns and finalize the output
    print(len(final_df_call_IN))
    print(len(final_df_call_OUT))
    print(len(final_df_call_NEAR))
    final_df_call_IN['Symbol'] = company_name
    final_df_call_IN['difference'] = final_df_call_IN['future_option_price'] - final_df_call_IN['Option_price']
    final_df_call_OUT['Symbol'] = company_name
    final_df_call_OUT['difference'] = final_df_call_OUT['future_option_price'] - final_df_call_OUT['Option_price']
    final_df_call_NEAR['Symbol'] = company_name
    final_df_call_NEAR['difference'] = final_df_call_NEAR['future_option_price'] - final_df_call_NEAR['Option_price']

    # Call designPortfolio on each final DataFrame
    print("Final DataFrame (Call OUT):")
    final_df_call_OUT = designPortfolio(final_df_call_OUT, company_name, 'call_OUT', current_invest)
    print("________________________________________________________________________________________________________________")
    print("Final DataFrame (Call IN):")
    final_df_call_IN = designPortfolio(final_df_call_IN, company_name, 'call_IN', current_invest)
    print("________________________________________________________________________________________________________________")
    print("Final DataFrame (Call NEAR):")
    final_df_call_NEAR = designPortfolio(final_df_call_NEAR, company_name, 'call_NEAR', current_invest)
    print("________________________________________________________________________________________________________________")
    
    return final_df_call_OUT, final_df_call_IN, final_df_call_NEAR


# Input fields
link_dict = link_dict
available_companies = list(link_dict.keys())

# Multi-select dropdown for company choices
selected_companies = st.multiselect("Select Companies (choose one or more)", options=available_companies)
interest_Rate = st.text_input("Enter 10y treasury")
Inflation_Rate = st.text_input("Enter Inflation Rate")
CPI = st.text_input("Enter CPI")
CCI = st.text_input("Enter CCI")

# Function to check for missing fields
def check_missing_fields(selected_companies, interest_Rate, Inflation_Rate, CPI, CCI):
    missing = []
    if not selected_companies:
        missing.append("Company Name")
    if not interest_Rate:
        missing.append("Interest Rate")
    if not Inflation_Rate:
        missing.append("Inflation Rate")
    if not CPI:
        missing.append("CPI")
    if not CCI:
        missing.append("CCI")
    return missing

# Function to get test data for a specific company
def get_test_data(company_name, link_dict, interest_Rate, Inflation_Rate, CPI, CCI):
    df_call = scrap_options_data(company_name, link_dict, 'Call')
    df_put = scrap_options_data(company_name, link_dict, 'Put')
    df_test = pd.concat([df_call, df_put], axis=0, ignore_index=True)
    df_test.rename(columns={'Strike': 'Strike_Price', 'Last': 'Option_price', 'option_type': 'Option_type',
                            'Imp Vol': 'implied_volatility', 'Vega': 'Vega', 'Theta': 'theta',
                            'Rho': 'rho', 'Delta': 'delta'}, inplace=True)
    
    stock = yf.Ticker(company_name)
    stock_data = stock.history(period="1d")
    Stock_price = stock_data['Close'].iloc[0]
    Beta = stock.info['beta']
    
    df_test['Stock_price'] = Stock_price
    df_test['Rate'] = interest_Rate
    df_test['Inflation_Rate'] = Inflation_Rate
    df_test['CCI'] = CCI
    df_test['CPI'] = CPI
    df_test['Assets Management Beta'] = Beta
    return df_test

# Check for missing fields
missing_fields = check_missing_fields(selected_companies, interest_Rate, Inflation_Rate, CPI, CCI)

# If there are missing fields, prompt the user to complete them
if missing_fields:
    st.write(f"Please enter the following fields: {', '.join(missing_fields)}")
else:
    # Initialize session state for each company if not already done
    for company in selected_companies:
        test_data_key = f'test_data_options_{company}'
        if test_data_key not in st.session_state:
            st.session_state[test_data_key] = pd.DataFrame()
            
    # If all fields are present, show the button
    if st.button('Get data for options'):
        # Retrieve data for each selected company
        for company in selected_companies:
            if company not in link_dict:
                st.write(f"Error: The company name '{company}' is not in the link dictionary.")
            else:
                st.session_state[f'test_data_options_{company}'] = get_test_data(
                    company, link_dict, interest_Rate, Inflation_Rate, CPI, CCI
                )

    # Display the data for each company if it's been populated
    for company in selected_companies:
        test_data_key = f'test_data_options_{company}'
        if test_data_key in st.session_state and not st.session_state[test_data_key].empty:
            st.write(f"Data for {company}:")
            st.write(st.session_state[test_data_key])

target = 'Option_price'

# Input fields for prediction
number_of_weeks = st.number_input('Enter number of weeks you want to predict')
current_invest = st.number_input('Enter current invest price:')

features = ["Strike_Price", "Stock_price", 'Option_price', "Rate",
            'Option_type', "implied_volatility",
            "Vega", "theta", "rho", 'delta', 'Inflation_Rate',
            'CCI', 'Assets Management Beta', "CPI"]

# Function to load and test the model sequentially by weeks
def load_and_test_model_weekly_sequential(model, test_data, included_features, target, number_of_weeks, date_col='Date'):
    final_data = pd.DataFrame()

    # Replace option types with numerical values for consistency
    test_data.replace({'Option_type': {'call': 0, 'put': 1, 'Call': 0, 'Put': 1}}, inplace=True)
    test_data[date_col] = pd.to_datetime(test_data[date_col], errors='coerce')

    for week in range(1, int(number_of_weeks) + 1):
        test_data[f'predicted_{week}_week'] = None

        for week in range(1, int(number_of_weeks) + 1):
            if week == 1:
                X_test = test_data[included_features]
            else:
                test_data['Option_price'] = test_data[f'predicted_{week - 1}_week']
                X_test = test_data[included_features]

            test_data[f'predicted_{week}_week'] = model.predict(X_test)
            test_data = test_data.loc[(test_data[f'predicted_{week}_week'] >= 0)]
        
        final_data = test_data.drop(['Symbol', 'Chg', 'implied_volatility', 'Bid', 'Gamma', 'Theoretical', 'Ask',
                                     'Intrinsic Value', 'Volume', 'Vega', 'Time Value', 'Open Interest', 'Delta/Theta',
                                     'Rate', 'Inflation_Rate', 'CCI', 'Assets Management Beta', 'CPI'], axis=1)
        final_data.replace({'Option_type': {0: 'Call', 1: 'Put'}}, inplace=True)
    return final_data

# Loop through each selected company and upload the model
for company in selected_companies:
    model_key = f"model_{company}"
    
    st.write(f"Upload model file for {company}")
    model_file = st.file_uploader(f"Upload model for {company}", type=["pkl"], key=company)

    # Load and store each model in session state
    if model_file is not None:
        st.session_state[model_key] = pickle.load(model_file)

# Check if models and data are loaded for each selected company
for company in selected_companies:
    model_key = f"model_{company}"
    test_data_key = f'test_data_options_{company}'
    
    if model_key in st.session_state and test_data_key in st.session_state and not st.session_state[test_data_key].empty:
        st.write(f"Results for {company}:")
        st.session_state[f'result_df_{company}'] = load_and_test_model_weekly_sequential(
            st.session_state[model_key], st.session_state[test_data_key], features, target, number_of_weeks
        )
        st.write(st.session_state[f'result_df_{company}'])
    else:
        st.write(f"Please ensure both model and test data are loaded for {company}.")        
       
        
def calculate_combined_portfolio(selected_companies):
    # Initialize a dictionary to hold return data for each company and type
    returns_data = {}

    # Loop through each selected company
    for company in selected_companies:
        # Fetch the individual portfolio DataFrames from session state
        df_out = st.session_state.get(f'result_df_{company}_out', pd.DataFrame())
        df_in = st.session_state.get(f'result_df_{company}_in', pd.DataFrame())
        df_near = st.session_state.get(f'result_df_{company}_near', pd.DataFrame())

        # Collect returns from each DataFrame
        if not df_out.empty and 'return' in df_out.columns:
            returns_data[f'{company}_OUT'] = df_out['return']
        if not df_in.empty and 'return' in df_in.columns:
            returns_data[f'{company}_IN'] = df_in['return']
        if not df_near.empty and 'return' in df_near.columns:
            returns_data[f'{company}_NEAR'] = df_near['return']

    # Create a DataFrame from the returns data
    if returns_data:
        returns_df = pd.DataFrame(returns_data)
    else:
        st.write("No return data found for any companies.")
        return pd.DataFrame()  # Return an empty DataFrame if no data is collected

    # Calculate weights for each row by dividing each element by the row sum
    weights_df = returns_df.div(returns_df.sum(axis=1), axis=0).fillna(0)

    return weights_df ,returns_df

if st.button("Portfolio"):
    # Loop through each selected company for portfolio analysis
    for company in selected_companies:
        result_key = f'result_df_{company}'

        # Check if result_df for the company is available in session state
        if result_key in st.session_state:
            result_df = st.session_state[result_key]
            result_df['Date'] = pd.to_datetime(result_df['Date'], errors='coerce')
            result_df['Exp_date'] = pd.to_datetime(result_df['Exp_date'], errors='coerce')
            result_df = round(result_df, 3)
            result_df = result_df[~result_df['Option_type'].str.contains(f'Put')]

            df_weeks = {}

            # Loop over the weeks (1 to number_of_weeks)
            for week in range(1, int(number_of_weeks) + 1):
                df_week = pd.DataFrame()

                if week == 1:
                # For the first week, use 'predicted_1_week' for 'future_option_price'
                    df_week[['Strike_Price', 'Option_type', 'delta', 'theta', 'rho', 'Exp_date',
                            'Date', 'Option_price', 'Stock_price', 'future_option_price']] = result_df[['Strike_Price', 'Option_type', 'delta', 'theta', 'rho', 'Exp_date',
                            'Date', 'Option_price', 'Stock_price', 'predicted_1_week']]
                else:
                    # For subsequent weeks, use 'predicted_(week-1)_week' and 'predicted_(week)_week'
                    df_week[['Strike_Price', 'Option_type', 'delta', 'theta', 'rho', 'Exp_date',
                            'Date', 'Option_price', 'Stock_price', 'future_option_price']] = result_df[['Strike_Price', 'Option_type', 'delta', 'theta', 'rho', 'Exp_date',
                            'Date', f'predicted_{week-1}_week', 'Stock_price', f'predicted_{week}_week']]

                # Store the DataFrame in the dictionary with the key 'weekX'
                df_weeks[f'week{week}'] = df_week

            #st.write(df_weeks['week1'])
            df_out, df_in, df_near = test_portfolio(df_weeks, company, current_invest)

            # Displaying the out of the money portfolio DataFrame
            st.write(f"Portfolio for Out of the Money (Company: {company}):")
            df_out = df_out.reset_index(drop=True)
            df_out['return'] = 0.0  # Initialize the column
            for i in range(len(df_out)):
                if i == 0:
                    df_out.loc[i, 'return'] = ((df_out.iloc[i]['resulted_op_money'] - current_invest) / current_invest) * 100
                else:
                    df_out.loc[i, 'return'] = ((df_out.iloc[i]['resulted_op_money'] - df_out.iloc[i-1]['resulted_op_money']) / df_out.iloc[i-1]['resulted_op_money']) * 100
            df_out = df_out.round(3)
            st.session_state[f'result_df_{company}_out'] = df_out
            st.dataframe(df_out)
            out_return = (((df_out['portfolio'].iloc[-1] + df_out['rest_op_money'].iloc[-1]) - current_invest) - df_out['commission'].sum()) / current_invest * 100
            st.write(f"Portfolio for Out of the Money Return: {out_return:.2f}%")
            fig_out_per = px.bar(df_out, x=df_out.index, y='portfolio', title=f"Portfolio Over Time (Company: {company})")
            st.plotly_chart(fig_out_per, use_container_width=True, key=f"out_per_{company}")
            fig_out_return = px.line(df_out, x=df_out.index, y='return', title=f"Return Over Time (Company: {company})")
            st.plotly_chart(fig_out_return, use_container_width=True, key=f"out_return_{company}")

            # Displaying the in the money portfolio DataFrame
            st.write(f"Portfolio for In the Money (Company: {company}):")
            df_in = df_in.reset_index(drop=True)
            df_in['return'] = 0.0  # Initialize the column
            for i in range(len(df_in)):
                if i == 0:
                    df_in.loc[i, 'return'] = ((df_in.iloc[i]['resulted_op_money'] - current_invest) / current_invest) * 100
                else:
                    df_in.loc[i, 'return'] = ((df_in.iloc[i]['resulted_op_money'] - df_in.iloc[i-1]['resulted_op_money']) / df_in.iloc[i-1]['resulted_op_money']) * 100
            df_in = df_in.round(3)
            st.session_state[f'result_df_{company}_in'] = df_in
            st.dataframe(df_in)
            in_return = (((df_in['portfolio'].iloc[-1] + df_in['rest_op_money'].iloc[-1]) - current_invest) - df_in['commission'].sum()) / current_invest * 100
            st.write(f"Portfolio for In the Money Return: {in_return:.2f}%")
            fig_in_per = px.bar(df_in, x=df_in.index, y='portfolio', title=f"Portfolio Over Time (Company: {company})")
            st.plotly_chart(fig_in_per, use_container_width=True, key=f"in_per_{company}")
            fig_in_return = px.line(df_in, x=df_in.index, y='return', title=f"Return Over Time (Company: {company})")
            st.plotly_chart(fig_in_return, use_container_width=True, key=f"in_return_{company}")

            # Displaying the near the money portfolio DataFrame
            st.write(f"Portfolio for Near the Money (Company: {company}):")
            df_near = df_near.reset_index(drop=True)
            df_near['return'] = 0.0  # Initialize the column
            for i in range(len(df_near)):
                if i == 0:
                    df_near.loc[i, 'return'] = ((df_near.iloc[i]['resulted_op_money'] - current_invest) / current_invest) * 100
                else:
                    df_near.loc[i, 'return'] = ((df_near.iloc[i]['resulted_op_money'] - df_near.iloc[i-1]['resulted_op_money']) / df_near.iloc[i-1]['resulted_op_money']) * 100
            df_near = df_near.round(3)
            st.session_state[f'result_df_{company}_near'] = df_near
            st.dataframe(df_near)
            near_return = (((df_near['portfolio'].iloc[-1] + df_near['rest_op_money'].iloc[-1]) - current_invest) - df_near['commission'].sum()) / current_invest * 100
            st.write(f"Portfolio for Near the Money Return: {near_return:.2f}%")
            fig_near_per = px.bar(df_near, x=df_near.index, y='portfolio', title=f"Portfolio Over Time (Company: {company})")
            st.plotly_chart(fig_near_per, use_container_width=True, key=f"near_per_{company}")
            fig_near_return = px.line(df_near, x=df_near.index, y='return', title=f"Return Over Time (Company: {company})")
            st.plotly_chart(fig_near_return, use_container_width=True, key=f"near_return_{company}")
        else:
            st.write(f"Error: No results found for {company}.")
            
    weights_df,returns_df = calculate_combined_portfolio(selected_companies) 
    total_values = []
    for i in range(len(weights_df)):
        if i == 0:
            invest_amount = current_invest
        else:
            invest_amount = total_values[-1]
        row_investment = weights_df.iloc[i] * invest_amount
        row_return = row_investment * (returns_df.iloc[i] / 100)
        total = row_return + row_investment
        if(total.sum() == 0):
            total_values.append(current_invest)
        else:
            total_values.append(total.sum())
    df_totals = pd.DataFrame({'Total': total_values})
    st.write("Combined Portfolio Weights:")
    st.dataframe(weights_df)
    st.write("Combined Portfolio returns:")
    st.dataframe(returns_df)  
    st.write("Combined Portfolio performance:")
    st.dataframe(df_totals)
    weights_df.index.name = 'Index'
    st.line_chart(weights_df)  
    fig_performance_df = px.line(df_totals, x=df_totals.index, y='Total', title="Return Over Time")
    st.plotly_chart(fig_performance_df, use_container_width=True)
    
