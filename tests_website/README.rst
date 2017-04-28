============
Test website
============

This holds infrastructure for running Bleach regression tests in a browser.


Usage
=====

From the repository root:

1. Generate the test cases::

      python tests_website/data_to_json.py tests/data > tests_website/testcases.json

2. Run the test server as a background process::

      cd tests_website && python server.py &

   You could also run it in a separate terminal by omitting the ``&`` at the
   end.

3. Open the page in browsers Python can find on your machine::

      python tests_website/open_test_page.py

4. Go through the web pages and inspect the bleached HTML.
