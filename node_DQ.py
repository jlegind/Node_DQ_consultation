import pandas
import requests
import json
from tabulate import tabulate
from openpyxl import load_workbook

#---------------------------------------------------------------------
#  ---- Enumerated issues vars
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
#---------------
issues_list = [taxonMatchNone, taxonMatchHigherrank, zeroCoordinate, countryCoordinateMismatch, countryInvalid, coordinateOutOfRange, recordedDateInvalid, recordedDateUnlikely, wktFootprintInvalid, basisOFRecord, individualCount]
taxon_issues = [taxonMatchNone, taxonMatchHigherrank]
geospatial_issues = [zeroCoordinate, countryCoordinateMismatch, countryInvalid, coordinateOutOfRange, wktFootprintInvalid]
temporal_issues = [recordedDateInvalid, recordedDateUnlikely]
other_issues = [basisOFRecord, individualCount]
#-------------------------------------------------------------------------

def get_facets(node, api_url):
    """
    Count the number of dataset or collections for which GBIF has occurrences of preserved specimens
    """
    base_request = api_url.format(node)
    print('Base request = ', base_request)
    response = requests.get(base_request)
    return response

the_response = get_facets('DK', api_url='https://api.gbif.org/v1/occurrence/search?publishingCountry={}&limit=0&facet=issue&facetLimit=100')

master_dict = {}
def make_issues_dicts(particular_list, category, j_resp):
    #issue = topical issue
    #plist is taxon_issues and so...
    print('currrrr ', particular_list)
    current_dict = dict.fromkeys(particular_list, '')
    print('current____dict', current_dict)
    resp = j_resp.json()
    counts = resp['facets'][0]['counts']
    print('COOOOUNTSS= ', counts)
    for j in counts:
        for k in particular_list:
            if j['name'] == k:
                cnt = j['count']
                print('COUUUNT = ', cnt)
                print('MATCH ', j['name'], k, j['count'])
                current_dict[k] = cnt
    first_dict = {category:'format me'}
    new_dict = {**first_dict, **current_dict}
    print('final == ', new_dict)
    master_dict.update(new_dict)
    return new_dict

rr = make_issues_dicts(taxon_issues, 'taxon issues', the_response)
print(master_dict)
df = pandas.DataFrame.from_dict(master_dict, orient='index')
print(df.to_string)
print(tabulate(df, headers='keys', tablefmt='psql'))
r2 = make_issues_dicts(geospatial_issues, 'geospatial issues', the_response)
df2 = pandas.DataFrame.from_dict(master_dict, orient='index')
print(tabulate(df2, headers='keys', tablefmt='psql'))
r3 = make_issues_dicts(temporal_issues, 'temporal issues', the_response)
df3 = pandas.DataFrame.from_dict(master_dict, orient='index')
print(tabulate(df3, headers='keys', tablefmt='psql'))

name = 'DQ_nodes10.xlsx'
writer = pandas.ExcelWriter(name, engine='xlsxwriter')

df3.to_excel(writer, sheet_name='sheet1', startrow=2, header=False)
workbook = writer.book
worksheet = writer.sheets['sheet1']
worksheet.merge_range('A1:E1', 'Checklist for Nodes Data Quality Service | Node title: DK')
#--
number_rows = len(df3.index) + 1




format1 = workbook.add_format({'bg_color': '#FFC7CE',
                              'font_color': '#9C0006'})

worksheet.conditional_format("$A$1:$B$%d" % (number_rows),
                             {"type": "formula",
                              "criteria": '=INDIRECT("B"&ROW())="format me"',
                              "format": format1
                             }
)
# workbook.close()
#--
fontfmt = workbook.add_format({'font_name': 'Arial', 'font_size': 16})
worksheet.set_row(0, None, fontfmt)
worksheet.set_column(0,4,26)
writer.save()
# maybeees v v
# # df = pandas.DataFrame.from_dict(current_list, orient='index', columns=['A', 'count'])
# df = pandas.DataFrame.from_dict(current_dict, orient='index')
# # df.columns = ['TAXON ISSUES', 'count']
# print('inside make_ df: ', df.to_string)
# print('INFO!; ', len(df.columns))
# print(tabulate(df, headers='keys', tablefmt='psql'))
# # return df.items()