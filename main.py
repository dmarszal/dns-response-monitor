import dns.resolver
import pprint
from iteration_utilities import flatten
import requests
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time

HOST_LIST = ('wp.pl', 'gazeta.pl', 'ap-selfservice.com', 'yahoo.com', 'ebay.com', 'ebay.de', 'YouTube.com', 'Facebook.com', 'wikipedia.org')
THRESHOLD = 1

def resolve(host_list: []):
    resolver = dns.resolver.Resolver() 
    resolver.nameservers = ['1.1.1.1', '8.8.8.8']
    return list({round(resolver.resolve(host, 'A').response.time, 5) for host in host_list})

def average(list) -> float:
    return sum(list) / len(list)

def message_slack(msg):
    client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

    try:
        response = client.chat_postMessage(channel='#random', text="Hello world!")
        assert response["message"]["text"] == "Hello world!"
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    verbose = True if os.environ.get('DVERBOSE') == 'True' else False

    t = time.process_time()
    # Run resolve 5 times to get an average
    responses = list(map(lambda x: resolve(HOST_LIST), range(3)))
    # Flatten the arrays
    responses = list(flatten(responses))
    avg_time = average(responses)
    if verbose:
        pp = pprint.PrettyPrinter(width=41, compact=True)
        pp.pprint(responses)
        print(f"Average response time {round(avg_time,3)}sec")
        print(f"Complete processing time {time.process_time() - t}")

