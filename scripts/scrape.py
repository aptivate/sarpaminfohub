#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scrapes values from the Sqlite database file and writes out nice JSON objects
that map to either objects in Fluidinfo or rows in a relational database (for
the purposes of import)
"""

import os
import json
import sqlite3
import sys
import pprint

import csv

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

supplier_country_translations = {'holland' : 'NL',
                      'mozambique' : 'MZ',
                      'india' : 'IN',
                      'tanzania' : 'TZ',
                      'malawi' : 'MW',
                      'danmark' : 'DK',
                      'denmark' : 'DK',
                      'cyprus' : 'CY',
                      'lesotho' : 'LS',
                      'kenya' : 'KE',
                      'south africa' : 'ZA',
                      'rwanda' : 'RW',
                      'india/germany' : 'IG',
                      'uganda' : 'UG'}

supplier_countries = {'NL' : "Netherlands",
                      'MZ' : "Mozambique",
                      'IN' : "India",
                      'TZ' : "Tanzania",
                      'MW' : "Malawi",
                      'DK' : "Denmark",
                      'CY' : "Cyprus",
                      'LS' : "Lesotho",
                      'KE' : "Kenya",
                      'ZA' : "South Africa",
                      'RW' : "Rwanda",
                      'IG' : "India/Germany",
                      'UG' : "Uganda"}

fictitious_countries = {'XA' : "Azania",
                        'XB' : "Buranda",
                        'XC' : "Equatorial Kundu",
                        'XD' : "Kambawe",
                        'XE' : "Katanga",
                        'XF' : "Matobo",
                        'XG' : "Moloni Republic",
                        'XH' : "Nagonia",
                        'XI' : "Natumbe",
                        'XJ' : "Zambawi",
                        'XK' : "Samgola",
                        'XL' : "Sangala",
                        'XM' : "Nibia"}

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
    records = []
    for row in c:
        appendCountryRecord(records, country_codes[row[0]], row[1])
    return records

def createSupplierCountries():
    return createCountries(supplier_countries)

def createFictitiousCountries():
    return createCountries(fictitious_countries)

def createCountries(countries):
    records = []
    for country_code in countries:
        appendCountryRecord(records, country_code, countries[country_code])
        
    return records
    

def appendCountryRecord(records, country_code, country_name):
    record={}
    country_fields = {}

    record['pk'] = country_code
    record['model'] = "infohub.country"
    record['fields'] = country_fields
    country_fields['name'] = country_name

    records.append(record)
    

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

def appendSupplierAndReturnIndex(results, manufacturer_lookups, supplier_dict,
                                 cursor, counter):
    for row in cursor:
        name = getStandardisedManufacturerName(manufacturer_lookups, row[0])
        
        if name != "" and name not in supplier_dict:
            result = {}
            supplier_fields = {}
    
            result['pk'] = counter
            result['model'] = "infohub.supplier"
            result['fields'] = supplier_fields
            supplier_fields['name'] = name

            supplier_dict[name] = counter
    
            results.append(result)
            counter += 1
    
    return counter

def scrapeSuppliers(conn, manufacturer_lookups):
    query = "SELECT DISTINCT supplier FROM form1_row"
    cursor = conn.cursor()
    cursor.execute(query)

    results = []
    
    counter = 1
    supplier_dict = {}

    counter = appendSupplierAndReturnIndex(results, manufacturer_lookups, 
                                           supplier_dict, cursor, counter)
    
    query = "SELECT DISTINCT supplier FROM form10_row"
    cursor = conn.cursor()
    cursor.execute(query)
    
    counter = appendSupplierAndReturnIndex(results, manufacturer_lookups, 
                                           supplier_dict, cursor, counter)

    return results, supplier_dict

def scrapeManufacturers(conn, manufacturer_lookups):
    query = "SELECT DISTINCT manufacturer FROM form1_row"
    c = conn.cursor()
    c.execute(query)
    results = []
    counter = 1
    manufacturer_dict = {}
    
    for row in c:
        name = getStandardisedManufacturerName(manufacturer_lookups, row[0])
        
        if name != "" and name not in manufacturer_dict:
            result = {}
            manufacturer_fields = {}
        
            result['pk'] = counter
            result['model'] = "infohub.manufacturer"
            result['fields'] = manufacturer_fields

            manufacturer_fields['name'] = name
        
            manufacturer_dict[name] = counter
        
            results.append(result)
            counter += 1
        
    return results, manufacturer_dict

def getStandardisedManufacturerName(manufacturer_lookups, name):
    name = name.strip()
    
    name = manufacturer_lookups.get(name.lower(), name)
        
    return name


def scrapeProductRegistrations(conn, drug_lookups, manufacturer_lookups):
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
        result['formulation'] = getStandardisedFormulationName(row[1])       
        result['product'] = getStandardisedDrugName(drug_lookups, row[2])
        result['manufacturer'] = getStandardisedManufacturerName(manufacturer_lookups,
                                                                 row[3])
        result['supplier'] = getStandardisedManufacturerName(manufacturer_lookups, 
                                                             row[4]) or None
        result['country_id'] = country_codes[row[5]]
        results.append(result)
    return results

def scrapeFormulations(conn, drug_lookups, manufacturer_lookups):
    """
    Returns a list of formulation dicts to be turned into a JSON dump.

    conn - a connection to the Sqlite database.
    """
    c = conn.cursor()
    # Return the results as discussed with Adi
    query = """SELECT f10.description, f10.landed_cost_price, f10.fob_price,
        f10.period, f10.issue_unit, country.name, country.id,
        f10.fob_currency, f10.landed_cost_currency, f10.period,
        f10.incoterm, f10.volume, f10.supplier, f10.supplier_country,
        f10.manufacture_country
        FROM form10_row AS f10
        INNER JOIN country ON f10.country = country.id
        ORDER BY f10.description, country.name"""
    c.execute(query)
    results = []
    for row in c:
        result = {}
        
        result['formulation'] = getStandardisedFormulationName(row[0])
        result['landed_cost_price'] = row[1] or None
        result['fob_price'] = row[2] or None
        result['period'] = row[3]
        result['unit'] = row[4]
        result['country'] = row[5]
        result['country_id'] = country_codes[row[6]]
        result['fob_currency'] = row[7]
        result['landed_currency'] = row[8]
        result['period'] = int(row[9])
        result['incoterm'] = row[10].strip()
        result['volume'] = row[11]
        result['supplier'] = getStandardisedManufacturerName(manufacturer_lookups, row[12])
        result['supplier_country'] = row[13].lower()
        result['manufacture_country'] = row[14]
        
        results.append(result)
    return results


def getStandardisedFormulationName(name):
    return name.replace('*', '')

def getStandardisedDrugName(drug_lookups, name):
    if name in drug_lookups:
        name = drug_lookups[name]
        
    return name

def outputJson(data_dir, name, data):
    fixtures_path = '%s/fixtures/initial_data' % (data_dir)
    filename = '%s/%s.json' % (fixtures_path, name)

    output = open(filename, 'w')
    json.dump(data, output, indent=2)
    output.close()

def scrape(data_dir):
    """
    Opens the database, scrapes a bunch of data and writes it all out to JSON
    """
    db_file = '%s/file.db' % (data_dir)
    conn = sqlite3.connect(db_file)

    drug_lookups = loadAndReturnDrugLookups(data_dir)
    manufacturer_lookups = loadAndReturnManufacturerLookups(data_dir)
    
    formulations = scrapeFormulations(conn, drug_lookups, manufacturer_lookups)
    registrations = scrapeProductRegistrations(conn, drug_lookups, 
                                               manufacturer_lookups)
    countries = scrapeCountries(conn)
    supplier_country_records = createSupplierCountries()
    fictitious_country_records = createFictitiousCountries()
    exchange_rates = scrapeExchangeRate(conn)
    suppliers, supplier_dict = scrapeSuppliers(conn, manufacturer_lookups)
    manufacturers, manufacturer_dict = scrapeManufacturers(conn,
                                                           manufacturer_lookups)

    outputJson(data_dir, "00_exchange_rates", exchange_rates)

    # Temporarily disabled - using fictitious names instead
    outputJson(data_dir, "00_countries", countries)
#    outputJson(data_dir, "00_fictitious_countries", fictitious_country_records)
    outputJson(data_dir, "00_supplier_countries", supplier_country_records)
    outputJson(data_dir, "00_suppliers", suppliers)
    outputJson(data_dir, "00_manufacturers", manufacturers)

    # formulations
    form_counter = 0
    formulation_table = []
    formulation_dict = {}

    price_counter = 0
    price_table = []

    incoterm_counter = 0
    incoterm_table = []
    incoterm_dict = {}
    
    for f in formulations:
        price_counter+=1
        if not f['formulation'] in formulation_dict:
            form_counter+=1
            formulation_fields = {}
            formulation_table.append({'pk': form_counter,
                                      'model': "infohub.formulation",
                                      'fields' : formulation_fields})

            formulation_fields['name'] = f['formulation']
            formulation_dict[f['formulation']] = form_counter
            
        incoterm = f['incoterm']
        if incoterm == "":
            incoterm = "FOB"

        if not incoterm in incoterm_dict:
            incoterm_counter+=1
            incoterm_fields = {}
            incoterm_table.append({'pk' : incoterm_counter,
                                   'model' : "infohub.incoterm",
                                   'fields' : incoterm_fields})
            incoterm_fields['name'] = incoterm
            incoterm_dict[incoterm] = incoterm_counter
                   
        incoterm_id = incoterm_dict[incoterm]
            
        price_record = {}
        price_fields = {}
        price_record['pk'] = price_counter
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
        price_fields['incoterm'] = incoterm_id
        price_fields['volume'] = f['volume']
        
        supplier_name = f['supplier'] or None
        supplier_id = None
        
        if supplier_name in supplier_dict:
            supplier_id = supplier_dict[supplier_name]
        elif supplier_name is not None:
            print "Unknown formulation supplier: %s" % supplier_name 

        price_fields['supplier'] = supplier_id

        supplier_country = f['supplier_country'] or None
        country_id = None
        
        if supplier_country is not None:
            if supplier_country not in supplier_country_translations:
                print "Unknown country: %s" % supplier_country
            else:
                country_id = supplier_country_translations[supplier_country]
        
        price_table.append(price_record)
    outputJson(data_dir,'00_formulations', formulation_table)
    outputJson(data_dir,'10_prices', price_table)
    outputJson(data_dir,'00_incoterms', incoterm_table)

    # Product
    product_table = []
    product_dict = {}
    product_counter = 0
    
    registration_table = []
    registration_counter = 0
    
    unknown_formulations = set()
    pp = pprint.PrettyPrinter(indent=4)

    num_dup = 0
    num_unknown = 0

    for registration in registrations:
        try:
            formulation_id = formulation_dict[registration['formulation']]
        except:
            unknown_formulations.add(registration['formulation'])
            num_unknown+=1
            continue
        
        registration_counter+=1
        
        registration_record = {}
        registration_fields = {}
        registration_record['pk'] = registration_counter
        registration_record['model'] = 'infohub.productregistration'
        registration_record['fields'] = registration_fields
        
        product_name = registration['product']
        
        if not product_name in product_dict:
            product_counter+=1
            product_dict[product_name] = product_counter
            product_record = {}
            product_fields = {}
            product_record['pk'] = product_counter
            product_record['model'] = "infohub.product"
            product_record['fields'] = product_fields

            product_fields['formulation'] = formulation_id
            product_fields['name'] = product_name
            product_table.append(product_record)
        else:
            num_dup+=1

        registration_fields['product'] = product_dict[product_name] 

        supplier_name = registration['supplier']    
        if supplier_name in supplier_dict:
            supplier_id = supplier_dict[supplier_name]
            registration_fields['supplier'] = supplier_id
        elif supplier_name is not None:
            print "Unknown product supplier: %s" % supplier_name
                        
        manufacturer_name = registration['manufacturer'] or None
        if manufacturer_name in manufacturer_dict:
            manufacturer_id = manufacturer_dict[manufacturer_name]
            registration_fields['manufacturer'] = manufacturer_id
        elif manufacturer_name is not None:
            print "Unknown product manufacturer: %s" % manufacturer_name

        registration_fields['country'] = registration['country_id']

        registration_table.append(registration_record)

    outputJson(data_dir, '10_products', product_table)
    outputJson(data_dir, '20_product_registrations', registration_table) 

    output = open('unknownFormulationsInProducts.json', 'w')
    json.dump(list(unknown_formulations), output, indent=2)
    output.close()

    print "Number of duplicate products: %d" % num_dup
    print "Number of unknown formulations: %d" % num_unknown

def loadAndReturnDrugLookups(data_dir):
    csv_reader = getCsvReader(data_dir, 'drugs2')
    
    return loadAndReturnNameStandardisedNameEntries(csv_reader)

def loadAndReturnManufacturerLookups(data_dir):
    csv_reader = getCsvReader(data_dir, 'manufacturers')
    
    return loadAndReturnStandardisedNameNameEntries(csv_reader)

def loadAndReturnNameStandardisedNameEntries(csv_reader):
    lookups = {}
    
    for row in csv_reader:
        (name, standardised_name) = row
        lookups[name.lower()] = standardised_name
        
    return lookups 

def loadAndReturnStandardisedNameNameEntries(csv_reader):
    lookups = {}
    
    for row in csv_reader:
        (standardised_name, name) = row
        
        if standardised_name == "":
            standardised_name = name
            
        lookups[name.lower()] = standardised_name
        
    return lookups 

def getCsvReader(data_dir, filename):
    lookup_file = '%s/%s.csv' % (data_dir, filename)
    return csv.reader(open(lookup_file), delimiter="\t")
    
    
    
if __name__ == "__main__":
    scrape(sys.argv[1])
