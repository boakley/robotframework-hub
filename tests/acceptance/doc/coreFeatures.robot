*** Settings ***
| Library  | Collections
| Library | Selenium2Library
| Library | Dialogs
| Resource | ${KEYWORD_DIR}/APIKeywords.robot
| Suite Setup | Run keywords
| ... | Create session | rfhub | url=http://${host}:${port} | AND
| ... | Open Browser | ${ROOT} | ${BROWSER}
| Suite Teardown  | Run keywords
| ... | Delete All Sessions | AND
| ... | Close all browsers

*** Variables ***
| ${ROOT} | http://${HOST}:${PORT}

*** Test Cases ***
| Nav panel shows correct number of collections
| | [Documentation]
| | ... | Verify that the nav panel has the correct number of items
| | 
| | [Tags] | navpanel
| | [Setup] | Run keywords
| | ... | Get list of libraries via the API | AND
| | ... | Go to | ${ROOT}/doc/
| | 
| | ${actual} | Get matching xpath count | //*[@id="left"]/ul/li/label
| | # why 8? Because we explicitly load 5 libraries 
| | # and three resource files in the setup
| | Should Be Equal As Integers | ${actual} | 8
| | ... | Expected 8 items in navlist, found ${actual}

| Nav panel shows all libraries
| | [Documentation]
| | ... | Verify that the nav panel shows all of the libraries
| | 
| | [Tags] | navpanel
| | [Setup] | Run keywords
| | ... | Get list of libraries via the API | AND
| | ... | Go to | ${ROOT}/doc/
| | 
| | :FOR | ${lib} | IN | @{libraries}
| | | XPath should match X times
| | | ... | //*[@id="left"]/ul/li/label[./text()='${lib["name"]}']
| | | ... | 1

| Main panel shows correct number of libraries
| | [Documentation]
| | ... | Verify that the main panel has the correct number of items
| | 
| | [Tags] | navpanel
| | [Setup] | Run keywords
| | ... | Get list of libraries via the API | AND
| | ... | Go to | ${ROOT}/doc/
| | 
| | ${actual} | Get matching xpath count | //*[@id="right"]/div[1]/table/tbody/tr/td/a
| | # why 5? Because we explicitly load 5 libraries in the suite setup
| | Should Be Equal As Integers | ${actual} | 5
| | ... | Expected 5 items in navlist, found ${actual}


| Main panel shows all libraries
| | [Documentation] 
| | ... | Verify that the main panel shows all of the libraries
| | 
| | [Setup] | Run keywords
| | ... | Get list of libraries via the API | AND
| | ... | Go to | ${ROOT}/doc
| | 
| | :FOR | ${lib} | IN | @{libraries}
| | | ${name} | Get from dictionary | ${lib} | name
| | | XPath should match X times
| | | ... | //*[@id="right"]//a[./text()='${name}']
| | | ... | 1

| Main panel shows all library descriptions
| | [Documentation] 
| | ... | Verify that the main panel shows all of the library descriptions
| | 
| | [Setup] | Run keywords
| | ... | Get list of libraries via the API | AND
| | ... | Go to | ${ROOT}/doc
| | 
| | ${section}= | Set variable | 
| | :FOR | ${lib} | IN | @{libraries}
| | | ${expected}= | Get from dictionary | ${lib} | synopsis
| | | ${actual}=   | Get text | //*[@id="right"]//a[text()='${lib["name"]}']/../following-sibling::td
| | | Should be equal | ${expected} | ${actual}

*** Keywords ***
| Get list of libraries via the API
| | [Documentation] 
| | ... | Uses the hub API to get a list of libraries.
| | ... | The libraries are stored in a suite-level variable
| | 
| | # N.B. 'Do a git on' stores the response in a test variable named ${JSON}
| | Do a get on | /api/libraries
| | ${libraries}= | Get From Dictionary | ${JSON} | libraries
| | Set suite variable | ${libraries} 

