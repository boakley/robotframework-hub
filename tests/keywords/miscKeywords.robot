*** Settings ***
| Library | Process
| Library | RequestsLibrary



*** Keywords ***
| Start rfhub
| | [Arguments] | ${PORT}
| | [Documentation]
| | ... | Starts rfhub on the port given in the global variable ${PORT}
| | ... | As a side effect this creates a suite variable named ${rfhub process},
| | ... | which is used by the 'Stop rfhub' keyword.
| | 
| | # make sure we use the same python executable used by the test runner
| | ${python}= | Evaluate | sys.executable | sys
| | ${rfhub process}= | Start process | ${python} | -m | rfhub | --port | ${PORT}
| | Set suite variable | ${rfhub process}
| | Wait until keyword succeeds | 20 seconds | 1 second
| | ... | Verify URL is reachable | /ping

| Stop rfhub
| | [Documentation]
| | ... | Stops the rfhub process created by "Start rfhub"
| | 
| | Terminate Process | ${rfhub process}
| | ${result}= | Get process result
| | Run keyword if | len('''${result.stderr}''') > 0
| | ... | log | rfhub stderr: ${result.stderr} | DEBUG


| Verify URL is reachable
| | # This could be useful in more places than just API tests.
| | # Maybe it should be moved to a different file...
| | [Arguments] | ${URL}
| | [Documentation]
| | ... | Fail if the given URL doesn't return a status code of 200.
| | Create Session | tmp | http://localhost:${PORT}
| | ${response}= | Get | tmp | ${url}
| | Should be equal as integers | ${response.status_code} | 200
