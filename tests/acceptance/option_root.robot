*** Settings ***
| Library | Selenium2Library
| Resource | tests/keywords/miscKeywords.robot

*** Variables ***
| ${ROOT} | http://${HOST}:${PORT}

*** Test Cases ***
| Specify --root /doc
| | [Documentation]
| | ... | Verify that --root /doc works properly
| | [Setup] | run keywords
| | ... | start rfhub | --port | ${PORT} | --root | /doc
| | ... | AND | open browser | ${ROOT} | ${BROWSER}
| | [Teardown] | run keywords
| | ... | stop rfhub
| | ... | AND | close all browsers
| | go to | ${ROOT}/
| | location should be | ${ROOT}/doc/

| Use default root (no --root option)
| | [Documentation]
| | ... | Verify that when --root is not supplied, we go to dashboard
| | [Setup] | run keywords
| | ... | start rfhub | --port | ${PORT}
| | ... | AND | open browser | ${ROOT} | ${BROWSER}
| | [Teardown] | run keywords
| | ... | stop rfhub
| | ... | AND | close all browsers
| | go to | ${ROOT}/
| | location should be | ${ROOT}/dashboard/


