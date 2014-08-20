*** Settings ***
| Documentation
| ... | Keywords related to the hub API

*** Keywords ***

| Do a GET on
| | [Arguments] | ${url}
| | [Documentation]
| | ... | Perform a GET on the given URL.
| | ... | 
| | ... | The response data will be stored in the suite variable
| | ... | ${response}. The payload will be converted to JSON and
| | ... | stored in the suite variable ${JSON}.
| | ... | 
| | ... | Example:
| | ... | \| \| \| Do a get on \| http://www.google.com \| blah blah blah
| | ... | \| \| \| Do a get on \| blah blah blah blah blah 
| | 
| | ${response}= | Get | rfhub | ${url}
| | ${JSON}= | Run keyword if | "${response.status_code}" == "200"
| | ... | To JSON | ${response.content} 
| | Set test variable | ${JSON}
| | Set test variable | ${response}

| Status code should be
| | [Arguments] | ${expected}
| | [Documentation]
| | ... | Verifies that the actual status code is the same as ${expected}
| | 
| | Should be equal as integers | ${response.status_code} | ${expected}
| | ... | Expected a status code of ${expected} but got ${response.status_code}
| | ... | values=false
