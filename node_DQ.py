import pandas
import requests
import json
from tabulate import tabulate
from openpyxl import load_workbook
import xlwt
import xlrd
from xlutils.copy import copy

#---------------------------------------------------------------------
#  ---- Enumerated issues variables
taxonMatchHigherrank = 'TAXON_MATCH_HIGHERRANK'
taxonMatchNone = 'TAXON_MATCH_NONE'
zeroCoordinate = 'ZERO_COORDINATE'
countryCoordinateMismatch = 'COUNTRY_COORDINATE_MISMATCH'
recordedDateInvalid = 'RECORDED_DATE_INVALID'
recordedDateUnlikely = 'RECORDED_DATE_UNLIKELY'
coordinateOutOfRange = 'COORDINATE_OUT_OF_RANGE'
countryInvalid = 'COUNTRY_INVALID'
wktFootprintInvalid = 'FOOTPRINT_WKT_INVALID'
basisOFRecord = 'BASIS_OF_RECORD_INVALID'
individualCount = 'INDIVIDUAL_COUNT_INVALID'
#---------------Topical categories lists
issues_list = [taxonMatchNone, taxonMatchHigherrank, zeroCoordinate, countryCoordinateMismatch, countryInvalid, coordinateOutOfRange, recordedDateInvalid, recordedDateUnlikely, wktFootprintInvalid, basisOFRecord, individualCount]
taxon_issues = [taxonMatchNone, taxonMatchHigherrank]
geospatial_issues = [zeroCoordinate, countryCoordinateMismatch, countryInvalid, coordinateOutOfRange, wktFootprintInvalid]
temporal_issues = [recordedDateInvalid, recordedDateUnlikely]
other_issues = [basisOFRecord, individualCount]
#-------------------------------------------------------------------------

def get_facets(node, api_url):
    """
    Count the number of issues for one node
    returns unprocessed response
    """
    base_request = api_url.format(node)
    print('Base request = ', base_request)
    response = requests.get(base_request)
    return response

# master_response = None
# #Contains all issues and is a reusable constant ^

def get_node_count(node):
    # A simple function to get the 'publishing node published records count'
    api_url = 'https://api.gbif.org/v1/occurrence/search?publishingCountry={}'.format(node)
    response = requests.get(api_url)
    rson = response.json()
    record_count = rson['count']
    print('The node count = ', record_count)
    return record_count

master_dict = {}
node_name = ''
#eventual dict going into the master dataframe

def make_issues_dicts(topical_list, category, j_resp, node):
    #particular_list : topical issue
    #category : title for the topic
    #jresp is the output of unprocessed API response
    node_name = node
    # master_response = get_facets(node,
    #            api_url='https://api.gbif.org/v1/occurrence/search?publishingCountry={}&limit=0&facet=issue&facetLimit=100')
    current_dict = dict.fromkeys(topical_list, '')
    #makes a dict from the list having no values
    print('current____dict', current_dict)
    response = j_resp.json()
    counts = response['facets'][0]['counts']
    #JSON of interest
    print('COOOOUNTSS= ', counts)
    #below loops to see which issues fit with the particular list key
    for j in counts:
        for k in topical_list:
            if j['name'] == k:
                cnt = j['count']
                print('COUUUNT = ', cnt)
                print('MATCH ', j['name'], k, j['count'])
                current_dict[k] = cnt
    recs = get_node_count(node)
    first_dict = {'total number of published records': recs, '':''}
    # ^creating top row + a blank row
    second_dict = {category: 'Records affected'}
    # ^Adding topical category row
    temp_dict = {**first_dict, **second_dict}
    # ^ stitching together dictionaries v
    new_dict = {**temp_dict, **current_dict}
    print('final == ', new_dict)
    master_dict.update(new_dict)
    return new_dict

# taxonomic section
jayson = get_facets('US', 'https://api.gbif.org/v1/occurrence/search?publishingCountry={}&limit=0&facet=issue&facetLimit=100')
rr = make_issues_dicts(taxon_issues, 'Taxon issues', jayson, node='US')
print(master_dict)
df = pandas.DataFrame.from_dict(master_dict, orient='index')
print(df.to_string)
print(tabulate(df, headers='keys', tablefmt='psql'))
#
# geospatial section
r2 = make_issues_dicts(geospatial_issues, 'Geospatial issues', jayson, node='US')
df2 = pandas.DataFrame.from_dict(master_dict, orient='index')
print(tabulate(df2, headers='keys', tablefmt='psql'))
# temporal section
r3 = make_issues_dicts(temporal_issues, 'Temporal issues', jayson, node='US')
df3 = pandas.DataFrame.from_dict(master_dict, orient='index')
print(tabulate(df3, headers='keys', tablefmt='psql'))
# other issues section
r4 = make_issues_dicts(other_issues, 'Other issues', jayson, node='US')
df4 = pandas.DataFrame.from_dict(master_dict, orient='index')
print(tabulate(df4, headers='keys', tablefmt='psql'))
#All these sections could usefully be rolled into one function

# output file name -v
name = 'US_DQ_nodes_checklist6.xlsx'

#Excel formatting below
writer = pandas.ExcelWriter(name, engine='xlsxwriter')

df4.to_excel(writer, sheet_name='sheet1', startrow=2, header=False)
#startrow is 2 to make place for the spreadsheet title
workbook = writer.book
worksheet = writer.sheets['sheet1']
merge_format = workbook.add_format({'bold': True})
worksheet.merge_range('A1:E1', 'Checklist for Nodes Data Quality Service // Node title: {}'.format('US'), merge_format)
#adding the title

number_rows = len(df4.index) + 1
format1 = workbook.add_format({'bg_color': '#111111','font_color': '#dddddd','underline':True})

worksheet.conditional_format("$A$1:$B$%d" % (number_rows),
                             {"type": "text",
                              # "criteria": '=INDIRECT("B"&ROW())="format me"',
                              "criteria": 'containing',
                              "value": "issues",
                              "format": format1
                             }
)
#formatting cell background color and underline via 'format1' var.

worksheet.set_column(0,1,35)
#set column width
#--end of excel formatting
writer.save()

