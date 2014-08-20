*** Settings ***
| Library | Process
| Library | Selenium2Library
| Library | RequestsLibrary

| Suite Setup    | Start rfhub | ${PORT}
| Suite Teardown | Stop rfhub

*** Variables ***
| # this may be overridden in default.args
| ${PORT} | 7071

*** Keywords ***
| Start rfhub
| | [Arguments] | ${PORT}
| | [Documentation]
| | ... | Starts rfhub on the port given in the global variable ${PORT}
| | ... | As a side effect this creates a suite variable named ${rfhub process},
| | ... | which is used by the 'Stop rfhub' keyword.
| | 
| | ${rfhub process}= | Start process | python | -m | rfhub | --port | ${PORT}
| | Set suite variable | ${rfhub process}
| | Wait until keyword succeeds | 20 seconds | 1 second
| | ... | Verify URL is reachable | /ping

| Stop rfhub
| | [Documentation]
| | ... | Stops the rfhub process created by "Start rfhub"
| | 
| | Terminate Process | ${rfhub process}

| Verify URL is reachable
| | # This could be useful in more places than just API tests.
| | # Maybe it should be moved to a different file...
| | [Arguments] | ${URL}
| | [Documentation]
| | ... | Fail if the given URL doesn't return a status code of 200.
| | Create Session | tmp | http://localhost:${PORT}
| | ${response}= | Get | tmp | ${url}
| | Should be equal as integers | ${response.status_code} | 200


