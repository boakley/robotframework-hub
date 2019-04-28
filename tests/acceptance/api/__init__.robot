*** Settings ***
| Resource | ${KEYWORD_DIR}/miscKeywords.robot

| Suite Setup    | Start rfhub | --port | ${PORT}
| Suite Teardown | Stop rfhub
