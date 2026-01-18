
# Transforms
The current available transforms are as follows:

|Name|JSON Fields|Description|
|-----|------|-----|
|Date|`type` -> `date` <br/> `columns` -> `[column1, column2, ...]` <br/> `date_format` -> date format in csv document (e.g. `"%B %d, %Y"`)|Reads the specified date format from the columns listed in columns array.|
|Drop Columns|`type` -> `drop_columns` <br/> `columns` -> `[column1, column2, ...]`|Drop the columns specified in columns.|
|Reorder Columns|`type` -> `reorder_columns` <br/> `columns` -> `[column1, column2, ...]`|Rearranges the current columns in the data set into the specified order in the provided list. Note that all columns in the list must exist. You cannot add a non-existing column and you cannot omit an existing column.|
|Trim Strings|`type` -> `trim_strings` <br/> `columns` -> `[column1, column2, ...]`|Trims the white space around the entry of the specified columns. Columns must contain a string.|
|Rename Columns|`type` -> `rename_columns` <br/> `columns` -> `[column1, column2, ...]` or `{"columnA":"columnAA", "columnB":"columnBB", ...}`|Transform for renaming columns. If the columns do not have names you can provided a list in the order of the columns to add labels. If the columns are labelled you must provide the original column name paired with the desired column name.|
|Create Column|`type` -> `create_column` <br/> `name` -> *name of the column to be added* (`string`) <br/> `default_value` -> *default value to initiate column to* (`string`,`int`,`float`)||
|Conditional Update|`type` -> `conditional_update` <br/> `filters` -> `[filter1, filter2, ...]` <br/> `assignments` -> `[assignment1, assignment2, ...]`|Filters the data according to the passed filters. Currently only supports logically combining the filters with the `&&` operator. The specified assignments are then applied to the rows that match the filter. For more about the structure of assignments and filters see the **Filters** and **Assignments** sections below.|

## Filters

Filters are basic boolean operations. They are used as a part of the **Conditional Update** transform. The filters which are available are as follows:

|Name|JSON Fields|Description|
|-----|-----|-----|
|Not Null|`type` -> `not_null` <br/> `column` -> *column name or index* (`string`, `int`)|Returns `true` if the specified field is `null`. Otherwise returns false.|
|Greater Than|`type` -> `greater_than` <br/> `column` -> *column name or index* (`string`, `int`) <br/> `threshold` -> *value to compare to* (`float`, `int`)|Returns `true` if the field is greater than the value specified by the threshold.|

## Assignments

Assignments describe operations for assigning a new value to a specified field. They are used as a part of the **Conditional Update** transform. They are often used in conjunction with **filters** to control what rows have their field updated.

|Name|JSON Fields|Description|
|-----|-----|-----|
|String|`type` -> `string` <br/> `column` -> *name or index of the column to assign the value to* (`string`,`int`) <br/> `value` -> *value to assign to the field* (`string`)|Assigns **value** to the field specified by **column**|
|Column|`type` -> `column` <br/> `column` -> *name or index of the column to assign the value to* (`string`, `int`) <br/> `value` -> *name or index of the column to read the value from* (`string`, `int`)|Assign the value from one field to another field on a given row.|
