import traceback, re, sys
import json
from zipfile import ZipFile

with open("expected_filings.json") as f:
    expected_filings = json.load(f)

lookup_region_points = 0
max_lookup_region_points = 33
lookup_region_percent = 33

filing_points = 0
max_filing_points = sum(len(v) for v in expected_filings.values())
filing_percent = 67

edgar_utils = None

errors = []


cleanup_whitespace = lambda s: re.sub("\s+", " ", s) if type(s) is str else s

def process(extracted_data):
   if type(extracted_data) is list: 
      return [cleanup_whitespace(item) for item in extracted_data] 

   return cleanup_whitespace(extracted_data)


def compare_lists(actual, expected):
    score = 0
    first_error = None

    for i, (act, exp) in enumerate(zip(actual, expected)):
        act = process(act)
        exp = process(exp)

        if exp is None:
            match = act is None
        elif type(exp) is list:
            match = set(act) == set(exp)
        else:
            match = act == exp

        if match:
            score += 1
        elif first_error is None:
            first_error = i, act, exp

    return score, first_error


def lookup_region_test():
    global lookup_region_points, errors

    ips = [
        '197.185.2.213',
        '197.147.81.89',
        '206.186.216.116',
        '213.218.150.177',
        '156.52.62.225',
        '57.88.237.101',
        '139.151.85.225',
        '103.202.68.190',
        '129.125.128.124',
        '249.174.115.73',
        '134.151.203.32',
        '245.79.200.240',
        '9.231.165.137',
        '147.200.118.8',
        '163.151.73.125',
        '134.47.218.173',
        '51.246.226.73',
        '236.80.62.13',
        '214.43.177.213',
        '117.42.105.186',
        '82.5.108.3',
        '11.15.245.52',
        '21.163.153.171',
        '225.146.49.188',
        '28.247.16.183'
    ]

    expected = [
        'South Africa',
        'Morocco',
        'Canada',
        'France',
        'Norway',
        'Syrian Arab Republic',
        'United States of America',
        'China',
        'Netherlands',
        '-',
        'United Kingdom of Great Britain and Northern Ireland',
        '-',
        'United States of America',
        'Australia',
        'United States of America',
        'Norway',
        'United Kingdom of Great Britain and Northern Ireland',
        '-',
        'United States of America',
        'China',
        'United Kingdom of Great Britain and Northern Ireland',
        'United States of America',
        'United States of America',
        '-',
        'United States of America'
    ]

    score, first_error = compare_lists(
        (edgar_utils.lookup_region(ip) for ip in ips), 
        expected
    )

    if first_error is not None:
        i, actual, expected = first_error

        errors.append(
            f"Error found in lookup_region on ip {ips[i]}: actual {actual}," \
                f" but expected {expected}"
        )

    lookup_region_points += score

    anonymized_ips =  [
        "1x3.1y4.2.2bc",
        "2xx.7y.z.2w",
        "1x.128.6.z",
        "7d.53.1z7.8z",
        "2z6.2g.8h.9z",
        "213.64.1.h",
        "57.1xy.9z.p",
        "9x.8z.2gh.12p"
    ]

    clean_ips = [
        "103.104.2.200",
        "200.70.0.20",
        "10.128.6.0",
        "70.53.107.80",
        "206.20.80.90",
        "213.64.1.0",
        "57.100.90.0",
        "90.80.200.120"
    ]

    score, first_error = compare_lists(
        (edgar_utils.lookup_region(ip) for ip in anonymized_ips), 
        (edgar_utils.lookup_region(ip) for ip in clean_ips)
    )

    if first_error is not None:
        i, _, _ = first_error

        errors.append(
            f"Error found in lookup_region: expected the regions for {anonymized_ips[i]} and {clean_ips[i]} to match."
        )

    lookup_region_points += score

def test_filing_attribute(filings, expected, attr):
    global filing_points, errors

    if attr.endswith("()"):
        attribute = attr[:-2]
        function = True
    else:
        attribute = attr
        function = False

    call_if_function = lambda x: x() if function else x

    # check if the regex for attribute has been implemented yet
    first_filing = next(iter(filings.values()))
    if hasattr(first_filing, attribute):
        expected_keys = expected.keys()
        expected_values = expected.values()

        actual_values = (
            call_if_function(getattr(filings[k], attribute))
            for k in expected_keys
        )

        score, first_error = compare_lists(actual_values, expected_values)

        if first_error is not None:
            i, actual, expected = first_error

            errors.append(
                f"Error found in Filing (path {list(expected_keys)[i]}): actual value of {attr} was {actual}" \
                    f" but expected {expected}"
            )

        filing_points += score
    else:
        errors.append(f"Filing test: {attr} not yet implemented.")

def read_filing(zf, filename):
    with zf.open(filename) as f:
        return str(f.read(), encoding="utf8")

def filing_test():
    filings = {}

    with ZipFile("docs.zip") as zf:
        for file in zf.filelist:
            if not file.is_dir():
                filename = file.filename

                filings[filename] = edgar_utils.Filing(read_filing(zf, filename))

    attributes =  [
        "dates",
        "sic",
        "addresses",
        "state()",
    ]

    for attribute in attributes:
        test_filing_attribute(
            filings,
            expected_filings[attribute],
            attribute
        )

def run_test(test):
    global errors

    try:
        test()
    except Exception as e:
        errors.append(traceback.format_exc())
    

def main():
    global edgar_utils, errors

    # import modules that are here
    try:
        import edgar_utils as tmp
        edgar_utils = tmp
    except ModuleNotFoundError:
        pass

    # run tests on the module
    if edgar_utils:
        run_test(lookup_region_test)
        run_test(filing_test)
    else:
        errors.append("could not find edgar_utils module")

    lookup_region_score = (lookup_region_points/max_lookup_region_points)*lookup_region_percent
    filing_score = (filing_points/max_filing_points)*filing_percent
    score = lookup_region_score + filing_score

    print(f"MODULE SCORE: {score}")
    for err in errors:
        print(err + "\n")

    # print/return a summary
    return {
        "score": score,
        "errors": errors
    } 

if __name__ == "__main__":
    main()
