*** Settings ***
| Library | Selenium2Library
| Library | Dialogs 

| Suite Setup    | Open Browser | ${ROOT} | ${BROWSER}
| Suite Teardown | Close all browsers
| Force Tags | browser-${BROWSER}

*** Variables ***
| ${HOST} | localhost
| ${PORT} | 7071
| ${ROOT} | http://${HOST}:${PORT}

*** Test Cases ***
| Base URL 
| | [Documentation]
| | ... | Objective: verify base url returns a page
| | [Tags] | smoke
| | Go to | ${ROOT}/doc
| | Location should be | ${ROOT}/doc/
| | Element should contain  | //*[@id="right"]/div[@id='summary-libraries']/h1 | Libraries
| | Element should contain  | //*[@id="right"]/div[@id='summary-resources']/h1 | Resource Files
| | Capture page screenshot

| Search via search box redirects to /doc/keywords
| | [Documentation]
| | ... | Objective: search via the search box and verify that the correct page is loaded
| | [Tags] | smoke
| | Go to | ${ROOT}/doc
| | Search for | none shall pass
| | Location should be | ${ROOT}/doc/keywords/?pattern=none%20shall%20pass

| Search summary, no results (searching for X found 0 keywords)
| | [Documentation]
| | ... | Objective: visit a bookmarked search page and verify that
| | ... | the right number of search terms was found
| | [Tags] | smoke
| |
| | Go to | ${ROOT}/doc
| | Search for | -xyzzy-
| | Page should contain | Searching for '-xyzzy-' found 0 keywords

| Search summary, one result (searching for X found 1 keywords)
| | [Documentation]
| | ... | Objective: visit a bookmarked search page and verify that
| | ... | the right number of search terms was found
| | ... | 
| | ... | This test assumes the "Easter" library is installed.
| | [Tags] | smoke
| |
| | Go to | ${ROOT}/doc
| | Search for | none shall pass
| | Page should contain | Searching for 'none shall pass' found 1 keywords

| Search summary, multiple results (searching for X found 6 keywords)
| | [Documentation]
| | ... | Objective: visit a bookmarked search page and verify that
| | ... | the right number of search terms was found
| | [Tags] | smoke
| |
| | Go to | ${ROOT}/doc
| | Search for | Fatal
| | Page should contain | Searching for 'fatal' found 6 keywords

| Correct number of search results - zero results
| | [Documentation]
| | ... | Objective: validate that we get the proper number of rows in
| | ... | the table of keywords
| | 
| | Go to | ${ROOT}/doc
| | Search for | -xyzzy-
| | ${count}= | Get matching xpath count | xpath=//table[@id='keyword-table']/tbody/tr
| | Should be equal as integers | ${count} | 0
| | ... | Expected zero rows in the table body, got ${count} instead

| Correct number of search results - 1 result
| | [Documentation]
| | ... | Objective: validate that we get the proper number of rows in
| | ... | the table of keywords
| | 
| | Go to | ${ROOT}/doc
| | Search for | none shall pass
| | ${count}= | Get matching xpath count | xpath=//table[@id='keyword-table']/tbody/tr
| | Should be equal as integers | ${count} | 1 
| | ... | Expected one row in the table body, got ${count} instead

| Correct number of search results - several results
| | [Documentation]
| | ... | Objective: validate that we get the proper number of rows in
| | ... | the table of keywords
| | 
| | Go to | ${ROOT}/doc
| | Search for | fatal
| | ${count}= | Get matching xpath count | xpath=//table[@id='keyword-table']/tbody/tr
| | Should be equal as integers | ${count} | 6
| | ... | Expected six rows in the table body, got ${count} instead

| Keyword search URL goes to search page
| | [Documentation]
| | ... | Objective: verify that the keyword search URL works
| | [Tags] | smoke
| | 
| | Go to | ${ROOT}/doc
| | Search for | none shall pass
| | Page should contain | Searching for 'none shall pass' found 1 keywords
| | Page Should Contain Link | None Shall Pass

| Clicking search result link shows keyword
| | [Documentation]
| | ... | Objective: make sure that clicking a link causes the 
| | ... | correct library to be displayed and the clicked-on 
| | ... | keyword is scrolled into view
| | 
| | Go to | ${ROOT}/doc
| | Search for | none shall pass
| | Click link | link=None Shall Pass
| | Location should be | ${ROOT}/doc/keywords/Easter/None%20Shall%20Pass/

*** Keywords ***
| Search for
| | [Arguments] | ${pattern}
| | [Documentation]
| | ... | Perform a keyword search
| | ... | This keyword inserts the given pattern into the search
| | ... | box and then submits the search form
| | Input text | id=search-pattern | ${pattern}
| | # we know the search mechanism has a built-in delay, so wait
| | # until it has a chance to start working
| | Sleep | 500 ms
| | Wait Until Element Is Visible | id=result-count

