*** Settings ***
| Documentation
| ... | Keywords related to the hub API

*** Keywords ***
| Start Test Server
| | [Documentation]
| | ... | Start a test server, and wait for it to come up
| | Start Process | python | -m | rfhub | --port | ${port}
| | Create session | server | url=http://${host}:${port}
| | Wait until keyword succeeds | 20 seconds | 1 second
| | ... | Verify URL is reachable | /ping

| Stop Test Server
| | [Documentation]
| | ... | Close all active server sessions, and stop all processes.
| | Delete all sessions
| | Terminate All Processes

| Verify URL is reachable
| | # This could be useful in more places than just API tests.
| | # Maybe it should be moved to a different file...
| | [Arguments] | ${URL}
| | [Documentation]
| | ... | Fail if the given URL doesn't return a status code of 200.
| | ${response}= | Get | server | ${url}
| | Status code should be | 200

| Do a GET on
| | [Arguments] | ${url}
| | [Documentation]
| | ... | Perform a GET on the given URL.
| | ... | 
| | ... | The response data will be stored in the suite variable
| | ... | ${response} and the payload will be converted to JSON
| | ... | and stored in the suite variable ${JSON}.
| | ... | Example:
| | ... | \| \| \| Do a get on \| http://www.google.com \| blah blah blah
| | ... | \| \| \| Do a get on \| blah blah blah blah blah 
| | ${response}= | Get | server | ${url}
| | ${JSON}= | Run keyword if | "${response.status_code}" == "200"
| | ... | To JSON | ${response.content} 
| | Set test variable | ${JSON}
| | Set test variable | ${response}

| Status code should be
| | [Arguments] | ${expected}
| | [Documentation]
| | ... | Verifies that the actual status code is the same as ${expected}
| | Should be equal as integers | ${response.status_code} | ${expected}
| | ... | Expected a status code of ${expected} but got ${response.status_code}
| | ... | values=false
