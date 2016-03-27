*** Settings ***
| Resource | tests/keywords/miscKeywords.robot

| Suite Setup    | Start rfhub | --port | ${PORT}
| Suite Teardown | Stop rfhub

*** Variables ***
| ${HOST} | localhost
| ${PORT} | 7071
| ${ROOT} | http://${HOST}:${PORT}