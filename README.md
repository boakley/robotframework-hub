# Welcome to Robot Framework Hub

This is a very early version of a server for the robot framework
testing framework. The hub uses flask to provide both a RESTful
interface and a browser-based UI for accessing test assets. 

The hub currently provides the following services: 

* RESTful API for retrieving the documentation for all available
  keywords
* Website for viewing the documentation for all keywords
  available on the system

The hub will eventually provide the following services:

* Web-based front-end to the robot test runner (pybot)
* Web-based dashboard for coordinating testing efforts
* Website for browsing test cases
* Website for browsing test results
* RESTful API for all of the above
* Plug-in architecture


For more documentation see https://github.com/boakley/robotframework-hub/wiki

## How to install and run the hub

After installation you will have a new module named "rfhub". 

### Using pip

```
    $ pip install robotframework-hub
```

### Install using the source

cd to where the source code is located, then run setup.py:

```
    $ cd /path/to/repository
    $ python ./setup.py install 
```

It is recommended that you use a virtualenv, though strictly speaking
it's not necessary.

### Dependencies

The hub is dependent on the following packages:

  - robotframework
  - flask
  - watchdog
  - sqlite3

### Start the server

To start the server, run the hub module:

```
    $ python -m rfhub 
```

By default the hub will run on port 7070, but that can be changed with
the --port option. 

The hub will serve up all built-in and installed robotframework
libraries that it can find. To include your own keyword libraries and
resource files, include a path to them on the command line. 

For example, if you have resource files in /myapp/keywords, include
that on the command line:

```
    $ python -m robotframework-hub /myapp/keywords
```

## Accessing the data

Presently, three uris are supported: 

- /api       - fetch JSON-formatted keyword data
- /doc       - UI for viewing keyword documentation
- /dashboard - a fairly useless (for now!) dashboard

### Read keyword documentation

Keyword documentation is available with URls like the following:

- http://localhost:7070/doc/keywords/
- http://localhost:7070/doc/keywords/BuiltIn/
- http://localhost:7070/doc/keywords/BuiltIn/Evaluate
- http://localhost:7070/doc/keywords?pattern=Should

### Get JSON data for keywords

JSON data is available on all of the keywords and libraries via
the "/api" url. For example:

- http://localhost:7070/api/keywords/
- http://localhost:7070/api/keywords/BuiltIn
- http://localhost:7070/api/keywords/BuiltIn/Evaluate
- http://localhost:7070/api/keywords?pattern=Should*
                     

## Acknowledgements

A huge thank-you to Echo Global Logistics (echo.com) for supporting
the development of this package.
