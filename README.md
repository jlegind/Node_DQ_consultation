# Node_DQ_consultation

This code makes data quality issues breakdown for the specified issues categories. The result comes in xlsx spreadsheet files format for the chosen country node.

This line is enough to get the ball rolling.:  
`node = 'DK'  `  
`file_name = 'my_file_name_{}.xlsx'.format(node)`  
`end_df = init_nodes_dq('DK', file_name)`  

The 'node' determines for which country node the stats are going to be created and is the only parameter that needs changing.
If other issues are of interest they can be added to the enumerations and topical categories. The def init_nodes_dq() function needs to be updated with new section(s) that will be somewhat similar to the existing ones.
Execution time is ~ 1 second for one node.  
This excel file is an example of the output for the US node: https://github.com/jlegind/Node_DQ_consultation/blob/master/master_node_DQ_nodes_checklist_US.xlsx

![sample image](https://github.com/jlegind/Node_DQ_consultation/blob/master/Consultation_sample_sheet_US.png)  
Format: !(url)
