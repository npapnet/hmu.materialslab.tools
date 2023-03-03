# HISTORY

This is a file documenting the changes for the package. 

Mainly is used for documenting the TODO list.

# TODOList
## DIC 
- PRIORITY: when the DIC analsysis xlsx file is created, merge the meta-data info with the dic analysis results. 
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

## 2023-03-03
- Completed the code necessary to perform the DIC analysis from the imada files
  - NOTE: some steps are still performed manually