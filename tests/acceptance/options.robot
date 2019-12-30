*** Settings ***
| Library | OperatingSystem

*** Test Cases ***
| Help for option --root
| | [Documentation]
| | ... | Verify that the help message includes help for --root
| | Start the hub with options | --help
| | Output should contain
| | ... | --root ROOT
| | ... | (deprecated) Redirect root url (http://localhost:port/) to this url

| Help for option -l/--library
| | [Documentation]
| | ... | Verify that the help message includes help for -i/--interface
| |
| | Start the hub with options | --help
| | Output should contain
| | ... | -l LIBRARY, --library LIBRARY
| | ... | load the given LIBRARY (eg: -l DatabaseLibrary)

| Help for option -i/--interface
| | [Documentation]
| | ... | Verify that the help message includes help for -i/--interface
| |
| | Start the hub with options | --help
| | Output should contain
| | ... | -i INTERFACE, --interface INTERFACE
| | ... | use the given network interface
| | ... | (default=127.0.0.1)

| Help for option -p / --port
| | [Documentation]
| | ... | Verify that the help message includes help for -p/--port
| |
| | Start the hub with options | --help
| | Output should contain
| | ... | -p PORT, --port PORT
| | ... | run on the given PORT
| | ... | (default=7070)

| Help for option -no-installed-keywords
| | [Documentation]
| | ... | Verify that the help message includes help for --no-installed-keywords
| |
| | Start the hub with options | --help
| | Output should contain
| | ... | --no-installed-keywords
| | ... | do not load some common installed keyword libraries

| Help for option -M/--module
| | [Documentation]
| | ... | Verify that the help message includes help for -M/--module
| |
| | Start the hub with options | --help
| | Output should contain
| | ... | -M MODULE, --module MODULE
| | ... | give the name of a module that exports one or more

| Help for option --poll
| | [Documentation]
| | ... | Verify that the help message includes help for --poll
| |
| | Start the hub with options | --help
| | Output should contain
| | ... | --poll
| | ... | use polling behavior instead of events to reload
| | ... | keywords on changes (useful in VMs)

*** Keywords ***
| Start the hub with options
| | [Arguments] | ${options}
| | [Documentation]
| | ... | Attempt to start the hub with the given options
| | ... |
| | ... | The stdout of the process will be in a test suite
| | ... | variable named \${output}
| |
| | ${output} | Run | python -m rfhub ${options}
| | Set test variable | ${output}

| Output should contain
| | [Arguments] | @{patterns}
| | [Documentation]
| | ... | Fail if the output from the previous command doesn't contain the given string
| | ... |
| | ... | This keyword assumes the output of the command is in
| | ... | a test suite variable named \${output}
| | ... |
| | ... | Note: the help will be automatically wrapped, so
| | ... | you can only search for relatively short strings.
| |
| | :FOR | ${pattern} | IN | @{patterns}
| | | Run keyword if | '''${pattern}''' not in '''${output}'''
| | | ... | Fail | expected '${pattern}'\n\ \ \ \ \ got '${output}'
