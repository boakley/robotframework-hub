# Welcome to Robot Framework Hub

This is a very early version of a server for the robot framework
testing framework. The hub uses flask to provide both a RESTful
interface and a browser-based UI for accessing test assets. 

It's crazy easy to get started. To install and run from a PyPi
package, do the following:

```
    $ pip install robotframework-hub
    $ python -m rfhub
```

To run from source it's the same, except intead of installing,
you cd to the folder that has this file. 

That's it! You can now browse documentation by visiting the url
http://localhost:7070/doc/

Want to browse your local robotframework assets? Just include
the path to your test suites or resource files on the command
line:

```
    $ python -m rfhub /path/to/test/suite
```


## Websites

Source code, screenshots, and additional documentation can be found here:

 * Source code: https://github.com/boakley/robotframework-hub
 * Project wiki: https://github.com/boakley/robotframework-hub/wiki

## Acknowledgements

A huge thank-you to Echo Global Logistics (echo.com) for supporting
the development of this package.
