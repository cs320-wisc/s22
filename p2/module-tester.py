import traceback

loans = None
search = None

loans_points = 0
search_points = 0

race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}

def loans_test():
    global loans_points
    loans_points = 0

    # TEST: Applicant class
    
    # +1 for just getting started by creating class
    loans.Applicant
    loans_points += 1

    # check race attribute filled correctly
    codes = sorted(race_lookup.keys()) + ["999"]
    for i in range(len(codes) + 3):
        codes_subset = codes[max(0, i-3):i]
        applicant = loans.Applicant("20-30", codes_subset)
        expected = {race_lookup[code] for code in codes_subset if code in race_lookup}
        assert applicant.race == expected
    loans_points += 1

    # repr
    applicant = loans.Applicant("80-90", [])
    assert repr(applicant) == "Applicant('80-90', [])"
    applicant = loans.Applicant("90+", ["25"])
    assert repr(applicant) == "Applicant('90+', ['Korean'])"
    loans_points += 1

    # lower_age
    assert loans.Applicant("<25", []).lower_age() == 25
    assert loans.Applicant("20-30", []).lower_age() == 20
    assert loans.Applicant(">75", []).lower_age() == 75
    loans_points += 1

    # __lt__
    applicants = sorted([
        loans.Applicant(">75", ["43", "44"]),
        loans.Applicant("20-30", ["1", "3"]),
        loans.Applicant("35-44", ["22"]),
        loans.Applicant("<25", ["5"]),
    ])
    assert [a.lower_age() for a in applicants] == [20, 25, 35, 75]
    loans_points += 1

    # TEST: Loan class

def search_test():
    search_points = 0
    pass

def main():
    global search, loans

    # import modules that are here
    try:
        import loans as tmp
        loans = tmp
    except ModuleNotFoundError:
        pass

    try:
        import search as tmp
        search = tmp
    except ModuleNotFoundError:
        pass

    # we'll return this summary at the end
    result = {
        "score": None,
        "errors": [],
    }

    # run tests on both modules, as far as we can
    if loans:
        try:
            loans_test()
        except Exception as e:
            result["errors"].append(traceback.format_exc())
    else:
        result["errors"].append("could not find loans module")

    if search:
        try:
            search_test()
        except Exception as e:
            result["errors"].append(traceback.format_exc())
    else:
        result["errors"].append("could not find search module")

    # summarize results
    result["score"] = (loans_points + search_points) / 10 * 100
    return result

if __name__ == "__main__":
    print(main())
