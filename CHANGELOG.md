# Change Log

## 1.0 - 2019-12-29
- Now requires python 3 to run
- Upgraded Jinja2 due to security vulnerability
- deprecated --root option; /doc is now the default root

### Issues closed
- Issue #78 - Need to support python3

## 0.8.3 - 2015-06-26

### Issues closed
- Issue #44 - Ctrl-c won't stop the hub on windows
- Issue #45 - add -P/--pythonpath option
- Issue #46 - add -A/--argumentfile option

### Other changes
- status of this package has been upgraded to "Beta"

## 0.7 - 2015-03-18

The big change is support for multiple resource or library files
with the same name.

This has a backward-incompatibility. URLs used to be of the form
/doc/library_name/keyword_name, but that prevented you from having
more than one library or resource file with the same name. In this
version, each library or resource file is assigned an id, and that
is used in place of the library name.

The id is guaranteed to be unique while rfhub is running, but could
change when you stop and restart the hub.

### Issues closed
- Issue #41  - Files with duplicate names aren't handled properly
- Issue #17  - should be able to search for keywords by name

### Other changes
- Version and scope are only displayed for libraries
- For resource files, the file path is displayed for a particular
  resource file in place of the version and scope
- The file path appears as a tooltip over names in the nav panel
- Added -v/--version command line argument
- Use bullet points next to keyword names in nav panel
- This CHANGELOG.md file was added

## 0.6 - 2014-10-19

### Issues closed
- Issue #37 - support for .tsv files
- Issue #18 - "in:" for search

## 0.5 - 2014-08-29

### Issues closed
- Issue #33 - keyword queries can specify which fields to return

### Other changes
- added favicon
- switch to tornado web server rather than flask dev server

## 0.4 - 2014-08-24

### Other changes
- incremental search
- added the id attribute so that the pages are easier to test
