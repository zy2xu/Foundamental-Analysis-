import mysql.connector
from mysql.connector import MySQLConnection, Error
import requests

def insert_company():
    
    query = "INSERT INTO financials.Indicators (ID,Name) VALUES(%s,%s)"
    mydb = mysql.connector.connect(host="localhost",user="root")
    cursor = mydb.cursor()
    
    companies = requests.get("https://api.usfundamentals.com/v1/companies/xbrl?&format=json&token=moHx0ZmsuO49zm0R3GI1nA")
    companiesJson = companies.json()

    for company in companiesJson:
        args = (company['company_id'], company['name_latest'])
        try:
            cursor.execute(query, args)
        except Error as error:
            print(error)
     
    cursor.close()
    mydb.commit()
    mydb.close()

def update_indicator(year,indicator):
    
    query = "UPDATE financials.Indicators" + year + " set " + indicator + " = %s where ID = %s"
    mydb = mysql.connector.connect(host="localhost",user="root")
    cursor = mydb.cursor()
   
    apiString = "https://api.usfundamentals.com/v1/indicators/xbrl?indicators=" + indicator + "&periods=" + year + "&token=moHx0ZmsuO49zm0R3GI1nA"
    data = requests.get(apiString)
    indicatorData = data.text.splitlines()

    for i in range (1, len(indicatorData)):
        fields = indicatorData[i].split(",")
        args = (fields[2],fields[0])
        try:
            cursor.execute(query,args)
        except Error as error:
            print(error)
     
    cursor.close()
    mydb.commit()
    mydb.close()

def main():
#    insert_company()
    indicators = ["NetIncomeLoss", "AssetsCurrent", "LiabilitiesCurrent", "PropertyPlantAndEquipmentNet", "PropertyPlantAndEquipmentGross", "LongTermDebtCurrent", "LongTermDebtNoncurrent", "Liabilities", "StockholdersEquity", "RetainedEarningsAccumulatedDeficit", "GrossProfit", "SalesRevenueNet", "Revenues", "SellingGeneralAndAdministrativeExpense", "ResearchAndDevelopmentExpense", "DepreciationDepletionAndAmortization", "InterestExpense", "InterestExpenseDebt", "InterestPaid", "IncomeTaxExpenseBenefit", "IncomeTaxesPaidNet", "EarningsPerShareBasic", "EarningsPerShareDiluted", "Assets", "CashAndCashEquivalentsAtCarryingValue", "NetCashProvidedByUsedInFinancingActivities", "NetCashProvidedByUsedInInvestingActivities", "NetCashProvidedByUsedInOperatingActivities", "OperatingIncomeLoss", "Goodwill"]
    years = ["2010","2011","2012","2013","2014","2015","2016","2017"]
    for indicator in indicators:
        for year in years:
            update_indicator(year,indicator)

if __name__ == '__main__':
	main()



