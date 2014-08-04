*** Keywords ***
| Create new KWDB instance
| | [Documentation]
| | ... | Creates and returns a new instance of the kwdb object.
| | ... | This object will have no libraries added by default. The
| | ... | object is available in the suite variable ${KWDB}
| | ${KWDB}= | evaluate | rfhub.kwdb.KeywordTable() | rfhub
| | Set test variable | ${KWDB}

| Load installed keywords into KWDB
| | [Documentation] 
| | ... | This calls a method to add all installed libraries into
| | ... | the database referenced by the suite variable ${KWDB}
| | Call method | ${KWDB} | add_installed_libraries

| Get keywords from KWDB
| | [Documentation]
| | ... | This calls the get_keywords method of the kwdb object
| | ... | referenced by ${KWDB}. It returns the data returned
| | ... | by that method. 
| | ${keywords}= | Call method | ${KWDB} | get_keywords | *
| | [Return] | ${keywords}

| Load a resource file into KWDB
| | [Arguments] | ${name or path}
| | [Documentation]
| | ... | Loads one library by name, or resoure file by path
| | ... | to the database referenced by the suite variable ${KWDB}
| | Call method | ${KWDB} | add | ${name or path}
