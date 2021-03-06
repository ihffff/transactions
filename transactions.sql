-- transactions
CREATE TABLE transactions (
    reference TEXT PRIMARY KEY,
    instrument TEXT, 
    transaction_type TEXT,
    settlement_date TEXT,
    service_fee TEXT,
    service_fee_currency TEXT,
    commission TEXT,
    commission_currency TEXT,
    oop_fee TEXT,
    oop_fee_currency TEXT,
    financial_transaction_tax TEXT,
    financial_transaction_tax_currency TEXT,
    transaction_amount TEXT,
    transaction_amount_currency TEXT,
    price TEXT,
    price_currency TEXT,
    quantity TEXT,
    cash_flow TEXT
);

-- instruments
CREATE TABLE instruments (
    instrument TEXT PRIMARY KEY,
    ticker TEXT,
    last_price TEXT
);

-- cash_flow
CREATE VIEW cash_flow
AS 
SELECT 
    instrument, settlement_date, quantity AS quantity, price, price_currency AS currency, cash_flow 
FROM transactions 
WHERE instrument NOT LIKE '%PENSION%'

UNION 

SELECT
    "TOTAL", date('now'), null, null, null, printf("%.2f", SUM(last_value))
FROM current_balance

ORDER BY settlement_date;

-- current_balance
CREATE VIEW current_balance
AS 
SELECT 
    t.instrument, SUM(t.quantity) AS quantity, i.last_price, ROUND(SUM(t.quantity) * last_price, 2) AS last_value
FROM transactions t 
LEFT JOIN instruments i on t.instrument = i.instrument
WHERE t.instrument NOT LIKE '%PENSION%' 
GROUP BY t.instrument
HAVING last_value > 0
ORDER BY t.instrument;

-- cash_flow
CREATE VIEW cash_flow_2021
AS 

SELECT 
    instrument, settlement_date, quantity AS quantity, price, price_currency AS currency, cash_flow 
FROM transactions 
WHERE instrument NOT LIKE '%PENSION%'
	AND settlement_date >= "2021-01-01"

UNION 

SELECT
	"INITIAL BALANCE", "2021-01-01", NULL, NULL, "EUR", printf("%.2f", SUM(cash_flow))
FROM transactions 
WHERE instrument NOT LIKE '%PENSION%'
	AND settlement_date < "2021-01-01"

UNION 

SELECT
    "TOTAL", date('now'), NULL, NULL, "EUR", printf("%.2f", SUM(last_value))
FROM current_balance

ORDER BY settlement_date