import mysql.connector
from mysql.connector import MySQLConnection, Error
import requests

def insert_company(year):
    
    query = "INSERT INTO financials.Indicators" + year + "(ID,Name) VALUES(%s,%s)"
    mydb = mysql.connector.connect(host="localhost",user="root")
    cursor = mydb.cursor()
    
    companies = requests.get("https://api.usfundamentals.com/v1/companies/xbrl?&format=json&token=moHx0ZmsuO49zm0R3GI1nA")
    companiesJson = companies.json()

    for company in companiesJson:
        args = (company['company_id'], company['name_latest'])
        try:
            cursor.execute(query, args)
            mydb.commit()
        except Error as error:
            print(error)
     
    cursor.close()
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
            mydb.commit()
        except Error as error:
            print(error)
     
    cursor.close()
    mydb.close()

def main():
  #  insert_company("2018")
    indicators = ["PropertyPlantAndEquipmentNet", "Revenues", "Goodwill", "NetIncomeLoss"]
    years = ["2010","2011","2012","2013","2014","2015","2016","2017","2018"]
    for indicator in indicators:
        for year in years:
            update_indicator(year,indicator)

if __name__ == '__main__':
    main()



