#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scrapes values from the Sqlite database file and writes out nice JSON objects
that map to either objects in Fluidinfo or rows in a relational database (for
the purposes of import)
"""
import json
import sqlite3
import sys
from decimal import Decimal

country_codes = {}
country_codes[1] = 'SC'
country_codes[2] = 'AO'
country_codes[3] = 'ZA'
country_codes[4] = 'TZ'
country_codes[5] = 'MW'
country_codes[6] = 'LS'
country_codes[7] = 'ZW'
country_codes[8] = 'MZ'
country_codes[9] = 'SZ'
country_codes[10] = 'NA'
country_codes[11] = 'CD'
country_codes[12] = 'BW'
country_codes[13] = 'ZM'

def normalisePrice(raw):
    """
    Takes a raw float value that represents the price of something and turns it
    into an integer representation of cents (USD).

    For example, the float value 4.49 will result in the integer value 449.
    """
    if raw:
        return Decimal(str(raw)).to_eng_string()
    else:
        return None


def scrapeCountries(conn):
    """
    Returns a list of countries
    """    
    query = "SELECT * FROM country"
    c = conn.cursor()
    c.execute(query)
    results = []
    for row in c:
        result={}
        country_fields = {}

        result['pk'] = country_codes[row[0]]
        result['model'] = "infohub.country"
        result['fields'] = country_fields
        country_fields['name'] = row[1]
        
        results.append(result)
    return results

def scrapeExchangeRate(conn):
    query = "SELECT * FROM exchange_rate"
    c = conn.cursor()
    c.execute(query)
    results = []
    counter = 0
    for row in c:
        result={}
        exchange_fields = {}

        result['pk'] = counter
        result['model'] = "infohub.exchangerate"
        result['fields'] = exchange_fields
        exchange_fields['symbol'] = row[0]
        exchange_fields['year'] = int(row[1])
        exchange_fields['rate'] = row[2]
        
        results.append(result)
        counter += 1
    return results
    

def scrapeProducts(conn):
    """
    Returns suppliers and products.

    conn - a connection to the Sqlite database
    """
    query = """SELECT c.name, f1.item, f1.product_name, f1.manufacturer,
        f1.supplier, c.id
        FROM form1_row AS f1
        INNER JOIN country AS c
        ON f1.country=c.id"""
    c = conn.cursor()
    c.execute(query)
    results = []
    for row in c:
        result={}
        result['country'] = row[0]
        result['formulation'] = row[1].replace('*', '')
        result['product'] = row[2]
        result['manufacturer'] = row[3]
        result['supplier'] = row[4] or None
        result['country_id'] = row[5]
        results.append(result)
    return results


def scrapeFormulations(conn):
    """
    Returns a list of formulation dicts to be turned into a JSON dump.

    conn - a connection to the Sqlite database.
    """
    c = conn.cursor()
    # Return the results as discussed with Adi
    query = """SELECT f10.description, f10.landed_cost_price, f10.fob_price,
        f10.period, f10.issue_unit, country.name, country.id,
        f10.fob_currency, f10.landed_cost_currency, f10.period
        FROM form10_row AS f10
        INNER JOIN country ON f10.country = country.id
        ORDER BY f10.description, country.name"""
    c.execute(query)
    results = []
    for row in c:
        result = {}
        result['formulation'] = row[0].replace('*', '')
        result['landed_cost_price'] = row[1] or None
        result['fob_price'] = row[2] or None
        result['period'] = row[3]
        result['unit'] = row[4]
        result['country'] = row[5]
        result['country_id'] = country_codes[row[6]]
        result['fob_currency'] = row[7]
        result['landed_currency'] = row[8]
        result['period'] = int(row[9])
        results.append(result)
    return results

def output_json(name, data):
    filename = '/home/martinb2/workspace/sarpaminfohub/django/sarpaminfohub/fixtures/%s.json' % name

    output = open(filename, 'w')
    json.dump(data, output, indent=2)
    output.close()

def scrape(db_file):
    """
    Opens the database, scrapes a bunch of data and writes it all out to JSON
    """
    conn = sqlite3.connect(db_file)
    formulations = scrapeFormulations(conn)
    products = scrapeProducts(conn)
    countries = scrapeCountries(conn)
    # Build Martin's schema
    exchange_rates = scrapeExchangeRate(conn)
    output_json("exchange_rates", exchange_rates)
    
    output_json("countries", countries)
    # formulations
    counter = 0
    form_counter = 0
    formulation_table = []
    price_table = []
    formulation_dict = {}
    for f in formulations:
        counter+=1
        if not f['formulation'] in formulation_dict:
            form_counter+=1
            formulation_fields = {}
            formulation_table.append({'pk': form_counter,
                                      'model': "infohub.formulation",
                                      'fields' : formulation_fields})
            
            formulation_fields['name'] = f['formulation']
#            formulation_fields['unit'] = f['unit']
            formulation_dict[f['formulation']] = form_counter
        price_record = {}
        price_fields = {}
        price_record['pk'] = counter
        price_record['fields'] = price_fields
        price_record['model'] = "infohub.price"
        price_fields['formulation'] = formulation_dict[f['formulation']]
        price_fields['country'] = f['country_id']
        price_fields['fob_price'] = normalisePrice(f['fob_price'])
        price_fields['landed_price'] = normalisePrice(f['landed_cost_price'])
        price_fields['fob_currency'] = f['fob_currency']
        price_fields['landed_currency'] = f['landed_currency']
        price_fields['issue_unit'] = f['unit']
        price_fields['period'] = f['period']
        price_table.append(price_record)
    output_json('formulations', formulation_table)
    output_json('prices', price_table)
    # Product
    product_table = []
    supplier_table = []
    product_dict = {}
    counter = 0
    unknown_formulations = set()
    for p in products:
        counter+=1
        if not p['product'] in product_dict:
            record = {}
            product_fields = {}
            record['pk'] = counter
            record['model'] = "infohub.product"
            record['fields'] = product_fields
            try:
                product_fields['formulation_id'] = formulation_dict[p['formulation']]
            except:
                unknown_formulations.add(p['formulation'])
                continue
            product_fields['name'] = p['product']
            product_fields['manufacturer'] = p['manufacturer']
            product_table.append(record)
            product_dict[p['product']] = counter
        supplier_record = {}
        supplier_fields = {}
        supplier_record['pk'] = counter
        supplier_record['fields'] = supplier_fields
        supplier_record['model'] = "infohub.supplier"
        supplier_fields['product_id'] = product_dict[p['product']]
        supplier_fields['name'] = p['supplier']
        supplier_fields['country_id'] = p['country_id']
        supplier_table.append(supplier_record)
    output_json('products', product_table)
    output_json('suppliers', supplier_table)

    output = open('unknownFormulationsInProducts.json', 'w')
    json.dump(list(unknown_formulations), output, indent=2)
    output.close()


if __name__ == "__main__":
    scrape(sys.argv[1])
