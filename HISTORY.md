# HISTORY

This is a file documenting the changes for the package. 

Mainly is used for documenting the TODO list.

# TODOList
## DIC 
- move result.dic file inside the output
- Move DIC-imada analysis and processing into the package.
  - consider how to make agnostic the two parts.
- Create a GUI to make easier the selection
- create a class that performs the actions for the grids (e.g. GridContainer).
  - e.g. create a method that extracts the mean strain values.
- Create a class for merging the results between the imada and DIC
- Cleanup further the pydic part of the repository.
  - area, cropping move into file
  - check init function and consider replacing it with a class.
  - see if read is necessary
- Investigate further the mechanism for the area of interest.
  - Investigate if it is possible and reliable to use the argument in the init class.

## OTHER
- PRIORITY: consider the structure of the folder for each analysis to be able to automate it.
- Consider developing a guide for the steps of the analysis

# Completed
## 2023-03-06

Starting working on a JSON (I also considered YAML) as a input file for each dic analysis. 

I started working on a skeleton and modified the existing py files with that in mind. 

Removed **convert_image_times2meta_data.py** and moved the function into the package under **dic.misc**

In **post_1_obtain_dic_strain.py**:
- All references to file names and directories were replaced by constants. 
- Commented out code that was not relevant anymore.

In **post_2_merge_dic_ut.py**:
- All references to file names and directories were replaced by constants.
- Moved all functions to the top of the file
- commented out code not relevant. 



## 2023-03-05
- PRIORITY: when the DIC analsysis xlsx file is created, merge the meta-data info with the dic analysis results. 
- File structure:
  - data-tensile: the csv from the imada
  - img_png: the folder with the imgs

convert_image_times2meta_data.py
- Added image data directory  
- renamed "meta-data.txt" --> "_meta-data.txt"
post_1_obtain_dic_strain.py
- changed the column names to the dic export file
- exported data file with time column 
- moved time into H column from I in the output file
post_2_merge_dic_ut.py
- created plot_synced_graph function to verify the sync time

## 2023-03-03
- Completed the code necessary to perform the DIC analysis from the imada files
  - NOTE: some steps are still performed manually