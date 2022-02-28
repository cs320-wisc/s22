import os, sys, importlib, json, re
from subprocess import Popen
import traceback
import pandas as pd

if len(sys.argv) > 1:
    scrape = importlib.import_module(student_file_name.split(".")[0])
    with open(student_file_name) as f:
        code = f.read()
else:
    import scrape
    with open("scrape.py") as f:
        code = f.read()

expected_travellog = pd.read_csv("part3.csv")

dfs_points = 0
bfs_points = 0
web_points = 0
ind_points = 0

driver = None
port = "5001"

def browser():
    global driver

    if not driver:
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium import webdriver
        os.system("pkill -f -9 chromium")
        options = Options()
        options.headless = True
        service = Service(executable_path="chromium.chromedriver")
        driver = webdriver.Chrome(options=options, service=service)
    return driver

def dfs_test():
    global dfs_points

    df = pd.DataFrame([
        [0,1,0,0],
        [0,0,1,1],
        [0,0,0,1],
        [0,0,1,0],
    ], index=["A", "B", "C", "D"], columns=["A", "B", "C", "D"])

    m = scrape.MatrixSearcher(df)
    dfs_points += 2
    assert m.go("B") == ["C", "D"]
    dfs_points += 3

    m.dfs_search("C")
    assert m.order == ['C', 'D']
    dfs_points += 5

    m.dfs_search("D")
    assert m.order == ['D', 'C']
    dfs_points += 5

    m.dfs_search("B")
    assert m.order == ['B', 'C', 'D']
    dfs_points += 5

    m.dfs_search("A")
    assert m.order == ['A', 'B', 'C', 'D']
    dfs_points += 5

def bfs_test():
    global bfs_points

    # test go
    f = scrape.FileSearcher()
    bfs_points += 5
    assert f.go("1.txt") == ['2.txt', '4.txt']
    bfs_points += 5

    # test bfs
    f = scrape.FileSearcher()
    f.bfs_search("1.txt")
    msg = f.message()
    bfs_points += 5
    assert msg == "MADCITY"
    bfs_points += 5

    # test dfs
    f = scrape.FileSearcher()
    f.dfs_search("1.txt")
    msg = f.message()
    assert msg == "MACTIDY"
    bfs_points += 5

def web_test():
    global web_points

    ws = scrape.WebSearcher(browser())
    url = f"http://localhost:{port}/Node_1.html"
    assert ws.go(url) == [f'http://localhost:{port}/Node_2.html',
                          f'http://localhost:{port}/Node_4.html']
    web_points += 5

    ws = scrape.WebSearcher(browser())
    ws.bfs_search(url)
    assert ws.order == [f'http://localhost:{port}/Node_1.html',
                        f'http://localhost:{port}/Node_2.html',
                        f'http://localhost:{port}/Node_4.html',
                        f'http://localhost:{port}/Node_3.html',
                        f'http://localhost:{port}/Node_5.html',
                        f'http://localhost:{port}/Node_6.html',
                        f'http://localhost:{port}/Node_7.html']
    web_points += 5
    actual = ws.table()
    expected = expected_travellog

    # how much overlap was there between the clues?
    both = len(set(expected["clue"]).intersection(actual["clue"]))
    either = len(set(expected["clue"]).union(actual["clue"]))
    web_points += int(both / either * 10)

    # did everything match?
    assert expected.shape == actual.shape
    assert (expected.reset_index() == actual.reset_index()).all().all()
    web_points += 5

def ind_test():
    global ind_points
    if os.path.exists("Current_Location.jpg"):
        os.remove("Current_Location.jpg")

    location = scrape.reveal_secrets(browser(), f'http://localhost:{port}', expected_travellog)
    ind_points += 5

    assert location == 'BASCOM HALL'
    ind_points += 10

    assert os.path.exists("Current_Location.jpg")
    ind_points += 5

    with open("Current_Location.jpg", "rb") as f:
        assert len(f.read()) == 99951
    ind_points += 5

def main():
    # we'll return this summary at the end
    result = {
        "score": None,
        "errors": [],
    }

    # check they aren't hardcoding
    matches = re.findall(r"((\d{1,3}\.){3}\d{1,3})", code)
    if matches:
        result["errors"].append(f"You are not allowed to hardcode IP addresses like {matches[0][0]} in your code.")
        return result
    if "localhost" in code.lower():
        result["errors"].append(f"'localhost' may not appear in your code.")
        return result

    # launch application.py
    f = open("web.log", "a")
    p = Popen(["python3", "application.py", port], stdout=f, stderr=f, stdin=f)

    # run tests, as far as we can
    for test in [dfs_test, bfs_test, web_test, ind_test]:
        print("RUN:", test.__name__)
        try:
            test()
        except Exception as e:
            result["errors"].append(traceback.format_exc().split("\n"))

    # shut down application.py 
    p.terminate()

    # summarize results
    assert max(dfs_points, bfs_points, web_points, ind_points) <= 25
    result["dfs_points"] = dfs_points
    result["bfs_points"] = bfs_points
    result["web_points"] = web_points
    result["ind_points"] = ind_points
    result["score"] = dfs_points + bfs_points + web_points + ind_points
    return result

if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
