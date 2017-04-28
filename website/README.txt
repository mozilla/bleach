Scripts for a Bleach demo/test website

Usage:

from the project root:

# generate testcases.json
python website/data_to_json.py tests/data > testcases.json

# run the test server
cd website && python server.py &

# open the page in browsers python can find
python open_test_page.py

# inspect bleached html and iframe
