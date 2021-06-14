This is an experiment, to create a data driven test where the test
name is the test data. Clever, or too clever? It certainly reads nice.

*** Settings ***
| Library         | RequestsLibrary
| Library         | Collections
| Resource        | ${KEYWORD_DIR}/APIKeywords.robot
| Suite Setup     | Create session | rfhub | url=http://${host}:${port}
| Suite Teardown  | Delete All Sessions
| Test Template   | Verify URL return codes
| Force Tags      | smoke | api

*** Keywords ***
| Verify URL return codes
| | [Arguments] | ${expected return code}
| | Do a GET on | ${TEST_NAME} | ${expected return code}
| | Status code should be | ${expected return code}

*** Test Cases ***
| # url                                         | # expected response code
| /api/keywords/                                | 200 
| /api/keywords                                 | 200 
| /api/keywords?library=builtin                 | 200
| /api/keywords?pattern=Should*                 | 200 
| /api/keywords/builtin/Should%20be%20equal     | 200
| /keyword                                      | 404
| /api/keywords/unknown_library/unknown_keyword | 404
| /api/keywords/builtin/unknown_keyword         | 404
| /api/libraries                                | 200
| /api/libraries/BuiltIn                        | 200

# need to move these to a separate file since
# this template keyword expects JSON output
#| /doc                                          | 200
#| /doc/keywords/BuiltIn                         | 200
#| /doc/keywords/BuiltIn#Evaluate                | 200

