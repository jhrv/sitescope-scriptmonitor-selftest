import urllib2
import json
import sys

def main():
    if len(sys.argv) <= 1:
        raise Exception("No URL to selftest provided. Run script like this 'python check_selftest.py <url to selftest>")
    selftest_url = sys.argv[1]
    perform_selftest(selftest_url)

def perform_selftest(url):
    payload = urllib2.urlopen(url).read()
    selftest = json.loads(payload)
    aggregate_result = selftest['aggregate_result']
    if aggregate_result == 0:
        sys.exit(0)
    else:
        print("Failed checks on selftest (%s):\n" % url)
        print(gatherErrorMessages(selftest))
        sys.exit(-1)

def gatherErrorMessages(selftest):
    all_checks = selftest["checks"]
    failing_checks = filter(lambda x: x["result"] == 1, all_checks)
    error_msgs = ''
    for check in failing_checks:
            error_msg = "Failed check: %s\n Message: %s\n Endpoint: %s" % (check["description"], check["errorMessage"], check["endpoint"])
            error_msgs += error_msg + "\n\n"
            
    return error_msgs

main()
