*** Settings ***
| Resource | tests/keywords/miscKeywords.robot

| Suite Setup    | Start rfhub | ${PORT}
| Suite Teardown | Stop rfhub
