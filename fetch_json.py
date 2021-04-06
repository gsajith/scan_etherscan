import urllib, json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_json.py <output_file_name>")
        return

    print("\n\n")
    print("Will write to output file: " + sys.argv[1])
    f = open(sys.argv[1], "w")
    f.close()
    load_dotenv()
    api_key = os.getenv('API_KEY')
    print("API KEY: " + api_key)
    print("\n\n")

    # If transaction topic is less than this number (0xfffff), consider it as a zero for determining to/from transactions
    max_empty_topic = 1048575
    # First block this year at Jan-01-2021 12:00:01 AM +UTC
    last_block = 11565020
    last_timestamp = 0

    base_url = "https://api.etherscan.io/api?"
    getVars = {'module':'logs', 'action':'getLogs'}
    # Foundation eth address
    getVars['address'] = '0xcda72070e455bb31c7690a170224ce43623d0b6f'
    getVars['toBlock'] = 'latest'
    getVars['apikey'] = api_key
    getVars['fromBlock'] = last_block

    # Flag to print starting block
    first_block = True

    # Store transactions per day
    counts = {}
    while True:
        url = base_url + urllib.urlencode(getVars)
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        results = data['result']
        print(url)

        print("status: " + data['status'])
        print("len: " + str(len(results)))

        # Break on error or invalid results
        if data['status'] != "1" or len(results) < 1:
            break

        for result in results:
            # print(int(result['blockNumber'], 0))
            last_block = max(last_block, int(result['blockNumber'], 0))
            last_timestamp = max(last_timestamp, int(result['timeStamp'], 0))
            if first_block:
                first_block = False
                print("scanning from block: " + str(int(result['blockNumber'], 0)) + " at " + datetime.utcfromtimestamp(int(result['timeStamp'], 0)).strftime('%B %d, %Y %H:%M:%S'))

            if len(result['topics']) >= 4:
                # Completed transaction if len(topics) >= 4
                day_string = datetime.utcfromtimestamp(int(result['timeStamp'], 0)).strftime('%Y-%m-%d')
                is_out_transaction = int(result['topics'][1], 0) < max_empty_topic
                if day_string not in counts:
                    counts[day_string] = {"in": 0, "out":0}
                if is_out_transaction:
                    counts[day_string]['out'] += 1
                else:
                    counts[day_string]['in'] += 1

        print("scanned to block: " + str(last_block) + " at " + datetime.utcfromtimestamp(last_timestamp).strftime('%B %d, %Y %H:%M:%S') + "\n")

        # Break if we got fewer than 1000 results, since that means we've reached the end
        if len(results) < 1000:
            break

        getVars['fromBlock'] = last_block
        # Safe rate limit <5 requests/second
        time.sleep(0.3)

    print("\n\n========== SCAN DONE ===========")
    print("Writing to file: " + sys.argv[1])
    f = open(sys.argv[1], "w")
    f.write("Date,Transactions in,Transactions out\n")
    for key in sorted(counts):
        print "%s: %s" % (key, counts[key])
        f.write(key + "," + str(counts[key]['in']) + "," + str(counts[key]['out']) + "\n")
    f.close()

if __name__ == "__main__":
    main()
