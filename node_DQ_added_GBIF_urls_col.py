import pandas
import requests
import json
from tabulate import tabulate


#---------------------------------------------------------------------
#  ---- Enumerated issues variables--- can be expanded to include more issues (See https://www.gbif.org/occurrence/search + 'Issues and flags')
taxonMatchHigherrank = 'TAXON_MATCH_HIGHERRANK'
taxonMatchNone = 'TAXON_MATCH_NONE'
zeroCoordinate = 'ZERO_COORDINATE'
countryCoordinateMismatch = 'COUNTRY_COORDINATE_MISMATCH'
recordedDateInvalid = 'RECORDED_DATE_INVALID'
recordedDateUnlikely = 'RECORDED_DATE_UNLIKELY'
coordinateInvalid = 'COORDINATE_INVALID'
coordinateOutOfRange = 'COORDINATE_OUT_OF_RANGE'
countryInvalid = 'COUNTRY_INVALID'
wktFootprintInvalid = 'FOOTPRINT_WKT_INVALID'
basisOFRecord = 'BASIS_OF_RECORD_INVALID'
individualCount = 'INDIVIDUAL_COUNT_INVALID'
#---------------Topical categories lists
issues_list = [taxonMatchNone, taxonMatchHigherrank, zeroCoordinate, coordinateInvalid, countryCoordinateMismatch, countryInvalid, coordinateOutOfRange, recordedDateInvalid, recordedDateUnlikely, wktFootprintInvalid, basisOFRecord, individualCount]
taxon_issues = [taxonMatchNone, taxonMatchHigherrank]
geospatial_issues = [zeroCoordinate,coordinateInvalid, countryCoordinateMismatch, countryInvalid, coordinateOutOfRange, wktFootprintInvalid]
temporal_issues = [recordedDateInvalid, recordedDateUnlikely]
other_issues = [basisOFRecord, individualCount]
#-------------------------------------------------------------------------

def get_facets(node, api_url):
    """
    Count the number of issues for one node
    returns unprocessed response
    """
    base_request = api_url.format(node)
    response = requests.get(base_request)
    return response


def get_node_count(node):
    # A simple function to get the 'publishing node published records count'
    api_url = 'https://api.gbif.org/v1/occurrence/search?publishingCountry={}'.format(node)
    response = requests.get(api_url)
    rson = response.json()
    record_count = rson['count']
    return record_count

master_dict = {}
#eventual dict going into the master dataframe

def make_issues_dicts(topical_list, category, j_resp, node):
    #particular_list : topical issue
    #category : title for the topic
    #jresp is the output of unprocessed API response
    #node is the country of interest (two char ISO country code)

    current_dict = dict.fromkeys(topical_list, '')
    #makes a dict from the list having no values

    response = j_resp.json()
    counts = response['facets'][0]['counts']
    #JSON of interest ^

    #below loops sees which issues fit with the topical list key
    for j in counts:
        for k in topical_list:
            if j['name'] == k:
                cnt = j['count']
                current_dict[k] = cnt
    recs = get_node_count(node)
    first_dict = {'total number of published records': recs, '':''}
    # ^creating top row + a blank row
    second_dict = {category: 'Records affected'}
    # ^Adding topical category row
    temp_dict = {**first_dict, **second_dict}
    # ^ stitching together dictionaries v
    new_dict = {**temp_dict, **current_dict}
    master_dict.update(new_dict)

    return new_dict

#initiation of script
master_node = 'PL'


jayson = get_facets(master_node, 'https://api.gbif.org/v1/occurrence/search?publishingCountry={}&limit=0&facet=issue&facetLimit=100')
#end of init.

# taxonomic section
rr = make_issues_dicts(taxon_issues, 'Taxon issues', jayson, node=master_node)
# print(master_dict)
df = pandas.DataFrame.from_dict(master_dict, orient='index')


# insert cell value ^
df = df.sort_index().reset_index(drop=True)
print('FIRST df: \n', tabulate(df, headers='keys', tablefmt='psql'))
#
# geospatial section
r2 = make_issues_dicts(geospatial_issues, 'Geospatial issues', jayson, node=master_node)
df2 = pandas.DataFrame.from_dict(master_dict, orient='index')
print(tabulate(df2, headers='keys', tablefmt='psql'))
# temporal section
r3 = make_issues_dicts(temporal_issues, 'Temporal issues', jayson, node=master_node)
df3 = pandas.DataFrame.from_dict(master_dict, orient='index')
print(tabulate(df3, headers='keys', tablefmt='psql'))
# other issues section
r4 = make_issues_dicts(other_issues, 'Other issues', jayson, node=master_node)
df4 = pandas.DataFrame.from_dict(master_dict, orient='index')
print('Final DF: ', tabulate(df4, headers='keys', tablefmt='psql'))
#All these sections could master_nodeefully be rolled into one function

# output file name -v
name = 'master_node_DQ_nodes_checklist3_{}.xlsx'.format(master_node)

#Add issue GBIF.org urls
api_issue = 'https://www.gbif.org/occurrence/search?issue={}&publishing_country={}&advanced=1'
url_dict = {}
for j in issues_list:
    gbif_issue_url = api_issue.format(j, master_node)
    url_dict[j] = gbif_issue_url

df_urls = pandas.DataFrame.from_dict(url_dict, orient='index')
df_list = [df4, df_urls]

final_df = pandas.concat(df_list, axis=1)
final_df.iloc[[2], [1]] = 'GBIF.org issue link'
#insert section header ^
print('FINAL DF::::', tabulate(final_df, tablefmt='psql', headers='keys'))

#Excel formatting below
writer = pandas.ExcelWriter(name, engine='xlsxwriter')

final_df.to_excel(writer, sheet_name='sheet1', startrow=2, header=False)
#startrow is 2 to make place for the spreadsheet title
workbook = writer.book
worksheet = writer.sheets['sheet1']
merge_format = workbook.add_format({'bold': True})
worksheet.merge_range('A1:E1', 'Checklist for Nodes Data Quality Service // Node title: {}'.format(master_node), merge_format)
#adding the title ^

number_rows = len(final_df.index) + 1
format1 = workbook.add_format({'bg_color': '#111111','font_color': '#dddddd','underline':True})

worksheet.conditional_format("$A$1:$B$%d" % (number_rows),
                             {"type": "text",
                              "criteria": 'containing',
                              "value": "issues",
                              "format": format1
                             }
)
#formatting cell background color and underline via 'format1' var.

worksheet.set_column(0,2,35)
#set column width
#--end of excel formatting
writer.save()

