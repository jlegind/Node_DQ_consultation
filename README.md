# Node_DQ_consultation

This code makes data quality issues breakdown for the specified issues categories. The result comes in xlsx spreadsheet files format for the chosen country node.

The line:  
`#initiation of script`  
`master_node = 'US'`  
`jayson = get_facets(master_node, 'https://api.gbif.org/v1/occurrence/search?publishingCountry={}&limit=0&facet=issue&facetLimit=100')`  

These lines are enough to get the ball rolling. If other issues are of interest they can be added to the enumerations and topical categories.  
This excel file is an example of the output for the US node: https://github.com/jlegind/Node_DQ_consultation/blob/master/master_node_DQ_nodes_checklist_US.xlsx

![sample image](https://github.com/jlegind/Node_DQ_consultation/blob/master/sample_xlsx_file.png)  
Format: !(url)
