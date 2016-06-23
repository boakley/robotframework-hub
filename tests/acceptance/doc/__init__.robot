*** Settings ***
| Resource | tests/keywords/miscKeywords.robot

| Suite Setup    | Start rfhub | --port | ${PORT}
| # we want to control pricisely which libraries are loaded,
| # so we aren't so dependent on what is actually installed
| ... | --no-installed-keywords
| ... | tests/keywords
| ... | BuiltIn
| ... | Collections
| ... | Easter
| ... | Screenshot
| ... | Selenium2Library
| Suite Teardown | Stop rfhub

*** Variables ***
| ${HOST} | localhost
| ${PORT} | 7071
| ${ROOT} | http://${HOST}:${PORT}