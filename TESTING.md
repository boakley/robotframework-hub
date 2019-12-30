To run the acceptance tests, cd to the folder with this file and run the following command:

    robot -A tests/conf/default.args tests

If you want to run a single suite, you can use the --suite option. For example,
either of the following commands will run just the search suite:

    robot -A tests/conf/default.args --suite tests.acceptance.doc.search tests
    robot -A tests/conf/default.args --suite search tests

The output files will be placed in tests/results.

Note: The tests start up a hub running on port 7071, so you don't have
to stop any currently running hub (though it also means you can't run
two tests concurrently).
