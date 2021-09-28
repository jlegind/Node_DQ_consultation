import string
import pandas
from pandas import util
import seaborn
import requests
import json
from tabulate import tabulate
from openpyxl import load_workbook


def get_facets(base_request, step=1000):
    """
    Count the number of dataset or collections for which GBIF has occurrences of preserved specimens
    """
    offset = 0
    end_of_records = False
    nb_facet = 0
    print('Base request = ', base_request)
    response = requests.get(base_request + "&facetOffset=" + str(offset))

    return response

# df = seaborn.load_dataset('iris')
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
#
# d1 = df.head()
# d2 = df.tail(3)
#
# lss = [d1, d2]
# res = pandas.concat(lss)
# res = res.sample(frac=1).reset_index(drop=True)
# print(res.to_string)
# res = res.drop(res[res.species == 'virginica'].index)
# print(res.to_string)

#______NODE DQ USING THE API !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# api_url = 'https://api.gbif.org/v1/occurrence/search?publishingCountry={}&limit=0&facet={}&facetLimit=100'
# url_ops = url.format('DK', 'issue')
# jayce = get_facets(url_ops)
# facets = jayce.json()['facets']
# print('#---- ', facets)
#
# counts = facets[0]['counts']
# print(counts)
# print(len(issues_list))

def make_issues_dicts(particular_list, category, node, facet, api_url='https://api.gbif.org/v1/occurrence/search?publishingCountry={}&limit=0&facet={}&facetLimit=100'):
    #issue = topical issue
    current_dict = dict.fromkeys(particular_list, '')
    print('current____dict', current_dict)
    api_url = api_url.format(node, facet)
    resp = get_facets(api_url).json()
    print('counts respose', resp)
    counts = resp['facets'][0]['counts']
    for j in counts:

        for k in particular_list:
            if j['name'] == k:
                cnt = j['count']
                print('COUUUNT = ', cnt)
                print('MATCH ', j['name'], k, j['count'])
                current_dict[k] = cnt
    print('final == ', current_dict)

    # df = pandas.DataFrame.from_dict(current_list, orient='index', columns=['A', 'count'])
    df = pandas.DataFrame.from_dict(current_dict, orient='index')
    # df.columns = ['TAXON ISSUES', 'count']
    print('inside make_ df: ', df.to_string)
    print('INFO!; ', len(df.columns))
    print(tabulate(df, headers='keys', tablefmt='psql'))
    # return df.items()

    return df

res = make_issues_dicts(taxon_issues, 'Taxon issues', 'DK', 'issue')
print('RES _ _ _ _', res.to_string)

# final_dict = res.items()
# print('itemized : ', final_dict)
# final_dict = list(final_dict)
# print('final ?? ', final_dict[0], 'end F.')


# for rec in final_dict:
#     print(rec)
# res2 = make_issues_df(geospatial_issues, 'Geospat issues')
#TURN INTO A FUNCTION !!!!!!!!!!
df_list = []
categories = []
# writer = pandas.ExcelWriter('candidate.xlsx', engine='openpyxl')
def add_1st_row(df, category):
    # df = pandas.DataFrame.from_records(topical_d)
    df.loc[-1] = [category]  # adding a row
    df.index = df.index + 1  # shifting index
    df = df.sort_index()
    return df
#     # df.to_excel(writer, sheet_name='sheet1', startrow=2, index=False)
#     writer.book = load_workbook('candidate.xslx')
#     writer.sheets =
#     # workbook = main_frame.book
#     # worksheet = main_frame.sheets['sheet1']
#     worksheet.merge_range('A1:E1', 'Checklist for Nodes Data Quality Service | Node title: DK')
#     cell_format = workbook.add_format()
#     cell_format.set_bold()
#     df_list.append(df)
#     categories.append(category)

# res = add_1st_row(res, 'Taxon issues')

init_writer = pandas.ExcelWriter('candidate11.xlsx', engine='xlsxwriter')
res.to_excel(init_writer, sheet_name='sheet1', startrow=2, index=True, header=False)
worksheet = init_writer.sheets['sheet1']
worksheet.set_column(0,4,20)

# cell_format_font.set_font_size(15)

workbook = init_writer.book
format_top = workbook.add_format({'bg_color': 'yellow', 'bold':True})

cell_format_font = workbook.add_format()
cell_format_font.set_font_name('Arial')
# merge_format = workbook.add_format() cell_format_font.set_font_size(15)
worksheet.merge_range('A1:E1', 'Checklist for Nodes Data Quality Service | Node title: DK')
worksheet.set_row(0, 15, format_top)
worksheet.set_column(0, 5, 27)
init_writer.save()
# add_1st_row(final_dict, 'Taxon_issues')

print('df_list: ', df_list, '\n cats: ', categories)
# df.loc[0] = 'GEospat issues', ''
# df = df.sort_index().reset_index(drop=True)
# print('to string: ', df.to_string)
# print(tabulate(df, headers='keys', tablefmt='psql'))

