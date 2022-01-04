#!/usr/bin/python3

import csv, sqlite3, glob, datetime
from decimal import *

con = sqlite3.connect("transactions/transactions.db")
cur = con.cursor()

sql = """INSERT OR IGNORE INTO transactions
         VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""


def to_eur(amount, currency) -> Decimal:
    if amount == "" or amount == 0:
        return Decimal(0)

    amount = Decimal(amount)

    if currency == "EUR":
        return amount
    elif currency == "EEK":
        return amount / Decimal("15.6466")
    elif currency == "LTL":
        return amount / Decimal("3.4528")
    else:
        raise Exception("Unknown currency " + currency)


for file in sorted(glob.glob("transactions/*.csv")):
    with open(file) as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)

        start_block = True

        for row in reader:
            if start_block:
                block_header = row
                start_block = False
            else:
                if not row[0]:
                    start_block = True
                else:
                    # remove empty column which is in the end of csv
                    row = row[:16]

                    # format date
                    row[2] = datetime.datetime.strptime(row[2], "%d.%m.%Y").strftime(
                        "%Y-%m-%d"
                    )

                    # add instrument
                    row.insert(1, block_header[0])

                    # transaction_amount
                    cash_flow = to_eur(row[12], row[13])

                    # TODO
                    # fun fact, for bonds this value represent face value,
                    # so we end up with 1000 * 1000 instead of 1000 * 1
                    # it would be nice to fix that automatically
                    quantity = Decimal(row[16])

                    # if we bought something then cash flow is negative
                    if quantity > 0:
                        cash_flow = cash_flow * -1

                    fees = 0

                    # service_fee
                    fees += to_eur(row[4], row[5])

                    # commission
                    fees += to_eur(row[6], row[7])

                    # oop_fee
                    fees += to_eur(row[8], row[9])

                    # financial_transaction_tax
                    fees += to_eur(row[10], row[11])

                    # "add" fees
                    cash_flow = cash_flow - fees

                    # cash_flow, round to cents
                    row.append(str(cash_flow.quantize(Decimal(10) ** -2)))

                    cur.execute(sql, row)

# TODO would be nice to add price ...
cur.execute(
    """INSERT OR IGNORE INTO instruments (instrument) 
       SELECT DISTINCT instrument FROM transactions"""
)

con.commit()
