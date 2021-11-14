# Scripts to track investments

## Getting Started

### Prerequisites

Python, Sqlite3, http://www.ch-werner.de/sqliteodbc/

### Installation

1. Create the database
```bash
sqlite3 transactions/transactions.db < transactions.sql
```

### Import transaction files

1. Download transactions in CSV format from Swedbank
2. Place the statement files in transactions directory
3. Run import.py script
4. Add tickers and prices to instruments table
5. Fix amount for bonds
6. 
7. Profit

### Calculate XIRR in Excel

1. Add a 64 bit ODBC Data Source pointing to transactions.db (Database name is file location)
2. Open Excel
3. Select Data -> Get Data -> From Other Sources -> From ODBC
4. Select your Data Source
5. Select cash_flow
6. In Power Query Editor (Select Transofrm Data) set correct data types for the columns 
```
= Odbc.DataSource("dsn=Transactions", [HierarchicalNavigation=true])
= Source{[Name="cash_flow",Kind="View"]}[Data]
= Table.ReplaceValue(cash_flow_View,".",",",Replacer.ReplaceText,{"quantity", "price", "cash_flow"})
= Table.TransformColumnTypes(#"Replaced Value",{{"price", Currency.Type}, {"cash_flow", Currency.Type}, {"quantity", type number}})
```
7. Load the data
8. XIRR can be calculated with 
```
=XIRR(cash_flow[cash_flow];cash_flow[settlement_date])
```
