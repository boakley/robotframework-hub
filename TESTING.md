To run the acceptance tests, cd to the folder with this file and run the following command:

    pybot -A tests/conf/default.args tests

If you want to run a single suite, you can use the --suite option. For example, 
either of the following commands will run just the search suite:

    pybot -A tests/conf/default.args --suite tests.acceptance.doc.search tests
    pybot -A tests/conf/default.args --suite search tests

The output files will be placed in tests/results.
