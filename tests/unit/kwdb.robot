*** Settings ***
| Documentation | Unit tests for the keyword database library 
| Library       | Collections
| Library | OperatingSystem
| Resource      | ${KEYWORD_DIR}/KWDBKeywords.robot
| Force tags    | kwdb
| Suite Setup   | Initialize suite variables

*** Test Cases ***

| Verify we can create an instance of the keyword database object
| | [Tags] | smoke
| | Create new KWDB instance
| | Should be true | ${KWDB} | # "True" as in "the object exists"

| Verify the initial keyword database is empty
| | [Tags] | smoke
| | Create new KWDB instance
| | ${keywords}= | Get keywords from KWDB
| | Length should be | ${keywords} | 0

| Verify we can add a resource file
| | [Documentation]
| | ... | Verify that we can load a single resource file
| | ... | This also verifies we can retrieve the expected number of keywords. 
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/onekeyword.robot
| | ${keywords}= | Get keywords from KWDB
| | ${num keywords}= | Get length | ${keywords}
| | Should be equal as integers | ${num keywords} | 1
| | ... | Expected 1 keyword but found ${num keywords} | values=False

| Verify we can add a resource file with .resource extension
| | [Documentation]
| | ... | Verify that we can load a single resource file with .resource extension.
| | ... | This also verifies we can retrieve the expected number of keywords.
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/threekeywords.resource
| | ${keywords}= | Get keywords from KWDB
| | ${num keywords}= | Get length | ${keywords}
| | Should be equal as integers | ${num keywords} | 3
| | ... | Expected 3 keyword but found ${num keywords} | values=False

| Verify we can add more than once resource file
| | [Documentation]
| | ... | Verify that we can load more than one resource file at a time.
| | ... | This also verifies we can retrieve the expected number of keywords. 
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/onekeyword.robot
| | Load a resource file into KWDB | ${DATA_DIR}/twokeywords.robot
| | ${keywords}= | Get keywords from KWDB
| | ${num keywords}= | Get length | ${keywords}
| | Should be equal as integers | ${num keywords} | 3
| | ... | Expected 3 keywords but found ${num keywords} | values=False

| Verify we can get a list of loaded resource files
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/onekeyword.robot
| | Load a resource file into KWDB | ${DATA_DIR}/twokeywords.robot
| | ${libraries}= | Call method | ${KWDB} | get_collections  | *
| | Length should be  | ${libraries} | 2
| | Dictionary should contain value | ${libraries[0]} | onekeyword
| | Dictionary should contain value | ${libraries[1]} | twokeywords

| Verify that a query returns the library name for each keyword
| | [Documentation]
| | ... | Verify that the library name is correct for each result from a query
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/twokeywords.robot
| | ${keywords}=      | Get keywords from KWDB
| | ${num keywords}=  | Get length | ${keywords}
| | 
| | # the list of keywords will be made up of (id, library, keyword, doc, args)
| | # tuples; make sure the library is correct for all items
| | :FOR | ${kw} | IN | @{keywords}
| | | Length should be | ${kw} | 5
| | | ... | expected the result to contain 4 elements but it did not. 
| | | Should be equal | ${kw[1]} | twokeywords
| | | ... | Expected the keyword library name to be "twokeywords" but it was "${kw[0]}"
| | | ... | values=False

| Verify that a query returns the expected keyword names
| | [Documentation]
| | ... | Verify that the keyword names returned from a query are correct.
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/twokeywords.robot
| | # the returned value is a list of tuples; this gives us
| | # a list of just keyword names
| | ${keywords}=      | Get keywords from KWDB
| | ${keyword names}= | Evaluate | [x[2] for x in ${keywords}]
| | List should contain value | ${keyword names} | Keyword #1
| | List should contain value | ${keyword names} | Keyword #2

| Verify that a query returns keyword documentation
| | [Documentation] 
| | ... | Verify that documentation is returned for each keyword
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/twokeywords.robot
| | ${keywords}= | Get keywords from KWDB
| | # Assume these are in sorted order....
| | Should be equal | ${keywords[0][3]} | Documentation for Keyword #1
| | Should be equal | ${keywords[1][3]} | Documentation for Keyword #2

| Verify that we can fetch a single keyword
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/twokeywords.robot
| | # we assume that since we only load one file, it has an id of 1...
| | ${keyword}= | Call method | ${KWDB} | get_keyword | 1 | Keyword #1
| | Should not be empty | ${keyword}

| Verify that a query returns a keyword with the expected data
| | [Tags] | smoke
| | Create new KWDB instance
| | Load a resource file into KWDB | ${DATA_DIR}/twokeywords.robot
| | # we assume that since we only load one file, it has an id of 1...
| | ${keyword}= | Call method | ${KWDB} | get_keyword | 1 | Keyword #1
| | Dictionary should contain item | ${keyword} | name           | Keyword #1
| | Dictionary should contain item | ${keyword} | collection_id  | 1
| | Dictionary should contain item | ${keyword} | doc            | Documentation for Keyword #1
| | Dictionary should contain item | ${keyword} | args           | []
| | # Do it again, for another keyword
| | ${keyword}= | Call method | ${KWDB} | get_keyword | 1 | Keyword #2
| | Dictionary should contain item | ${keyword} | name           | Keyword #2
| | Dictionary should contain item | ${keyword} | collection_id  | 1
| | Dictionary should contain item | ${keyword} | doc            | Documentation for Keyword #2
| | Dictionary should contain item | ${keyword} | args           | []

*** Keywords ***

| Initialize suite variables
| | [Documentation]    | Define some global variables used by the tests in this suite
| | ${test dir}=       | Evaluate | os.path.dirname(r"${SUITE SOURCE}") | os
| | set suite variable | ${KEYWORD DIR} | ${test dir}/keywords
| | set suite variable | ${DATA_DIR}    | ${test dir}/data

    