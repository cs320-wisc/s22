# DON'T START YET -- DRAFT!

# Project 3: Find the Path!

## Overview

In this project you will practice inheritance, graph search, and web
scraping. You'll hand-in a module called `scrape.py`. It will contain
three classes `GraphScraper`, `FileScraper` and `WebScraper`.

Make sure to run the tests before handing in.  During development, we
recommend having a debug.ipynb notebook to make calls to your module.

# Group Part (75%)

For this portion of the project, you may collaborate with your group
members in any way (even looking at working code).  You may also seek
help from 320 staff (mentors, TAs, instructor).  You <b>may not</b>
seek receive help from other 320 students (outside your group) or
anybody outside the course.

If you just want to run `python3 tester.py` from the terminal you must
call your python script `scrape.py`. If you do not call it this you
must run tester as `python3 tester.py <your_filename_here>`.

## Part 1: Graph Search

Paste the following starter code to your Python module.  Your job is
complete:

1. the `go` method in the `FileScraper` class (don't change the
one in `GraphScraper`)
2. the `bfs_search` method
3. the `dfs_search` method.

The two search methods will call `self.go` to visit nodes.  This will
not work if called on a GraphScraper object directly (because that
class should not have a working `go` method), but `FileScraper` (which
does have a `go`) method will inherit them.

```python
import os, zipfile

class GraphScraper:
    def __init__(self):
        self.visited = set()
        self.BFSorder = []
        self.DFSorder = []
	self.travelLog = pandas.DataFrame() # Used for webscraping only

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        pass

    def bfs_search(self, node):
        pass

class FileScraper(GraphScraper):
    def go(self, node):
        pass
```

The "file_nodes" directory will only contain .txt files, each
corresponding to a node in a directed graph, and each containing four
lines, formatted like this:

1. name of the node
2. names of the children nodes, separated by spaces
3. "BFS: XXX" where "XXX" is a string
4. "DFS: XXX" where "XXX" is a string

Your task is to implement the `FileScraper` class to scrape the
content of this directory.

The `go` method in the `FileScraper` class should read one of the txt
files and return a list of its children.  Whenever `go` reads a file,
it should also append the BFS string (line 3 of the file) to the
`BFSorder` list and append the DFS string (line 4 of the file) to the
`DFSorder` list.  For example, you should be able to run the following
in your debug notebook:

```python
fs = FileScraper()
print(fs.go("1"))
print(fs.go("2"))
print(fs.BFSorder)
print(fs.DFSorder)
```

Expected output:

```
['2', '4']
['1', '3', '5']
['M', 'A']
['C', 'O']
```

Your `bfs_search` (non-recursive) and `dfs_search` (recursive) methods
inherited from `GraphScraper` will perform graph search, somewhat like
the `find` and `find_bfs` methods from the reading, respectively:
https://tyler.caraza-harter.com/cs320/f21/lec/15-graphsearch1/reading.html

There are a few differences, however (your version will be somewhat
simpler overall):

1. we are not looking for a path to any particular destination.  We just want to explore the graph and see what info about nodes we can discover.  This is why we don't have any `dst` parameter.  Our `search` methods will also not need to return anything or do any backtracking.
2. there is not a `Node` class; instead, the methods are in the `GraphScraper` class.  So `self` will no longer refer to a Node object.  Instead, we'll know what node we're on because the name is passed in to the `node` parameter of the search functions
3. also, as there is no `Node` class, we can't use something like `self.children` or `node.children` to learn the nodes of the class.  You should use the `go` method you just wrote for this purpose instead.

We will only ever do one search on your graph object, so there's no
need to ever clear out your `visited` list. (However, you will need to update `visited`, `BFSorder`, and `DFSorder` in the next class you make (`Webscraper`) to allow for multiple succesive searches.) 

We've arranged the extra info in each file so that the correct search order will lead to recognizable words.  For example, if you run:

```python
fs = FileScraper()
fs.dfs_search("1")
fs.DFSorder
```

You should get `['C', 'O', 'V', 'I', 'D', '1', '9']`.

## Part 2: Web Crawling

For this part of the project you will also need to install a
ChromeBrowser and ChromeDriver onto your VM. In this lab you will only
work with selenium. *Note that we will be assuming that you are using the version of selenium specified in the install command. 

```
pip3 install selenium==3.141.0 beautifulsoup4 Flask lxml
sudo apt -y install chromium-browser
```

When it's all done, run both of the following, and verify that both
versions is 90+ (like "9X.X.X.X"):

```
chromium-browser --version
chromium.chromedriver --version
```

**Note 1**: your virtual machine does not have a graphical user interface,
so you won't be able to follow some of the early examples until I show
how to run in "headless" mode (unrelated to git's headless) and take
screenshots, unless you figure out how to install selenium on your
laptop as well for fun (we don't require it, as it can often get quite
tricky except on the VMs).

**Note 2**: launching many web browsers via code can quickly eat up
  all the memory on your VM.  You can run the `htop` command to see
  how much memory you have (hit "q" to quit when done).  If you're low
  on memory (you might notice your VM being sluggish), you can run
  `pkill -f -9 chromium` shutdown all browser instances hanging around
  in the background.

### `WebScraper` class

You'll be scraping a website implemented as a web application built
using the flask framework (you don't need to know flask for this
project, though you'll learn it soon and get a chance to build your
own website in the next project).  In an SSH session, run the
following to launch it:

```
python3 application.py
```

Then, open `http://<YOUR-VM-IP>:5000` in your web browser. Do not use the IP address that is output to console in the ssh session. This is incorrect.It should look like this:

<img src="webpage.jpg" width=600>

Each page (under "TRAVEL HISTORY") contains information in the form of
a table.  If you do either a DFS or BFS search through the site and
concatenate the table rows from the pages in the order in which they're
visited, you'll get a completed table of locations.

Each row in the table contains a 'clue'. Combining these 'clues' in the order shown by the table (first row to last row), will give you a passcode. 

By performing both searches, you'll get two passwords.  Entering
either correct password on the home page will redirect you to a
different page.

Use selenium to do the scraping.  BeautifulSoup is probably also
helpful, though not required.  Start with the following:

```python
class WebScraper(GraphScraper):
    # required
    def	__init__(self, driver=None):
        super().__init__()
        self.driver = driver

    # these three can be done as groupwork
    def go(self, url):
        pass

    def dfs_pass(self, start_url):
        pass

    def bfs_pass(self, start_url):
        pass

    # write the code for this one individually
    def protected_df(self, url, password):
        pass
```


**Note**: Make sure to kill the application before running the tester.py. (The tester tries to open an application on the same port!) When you want to kill the application make sure to shut it down via CTRL-C in your ssh session. This will shut it down properly, any other way could result in hangtime errors, so you may have to re-ssh in. As well if your tester.py hangs (never throws an error and stops execution) make sure you kill the command via CTRL-C for the same reason as above. 

### `go` method

Treat each page as a node, and each hyperlink as a directed
edge. Implement the `go` method such that, each time a page is visited the table rows are appended to self.travelLog. 

### `dfs_pass` method

Use the inherited `dfs_search` method to return the DFS travel log (a data frame with rows ordered corresponding to the rows on the visited pages when performing a DFS). 

You may want to use this function: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html

The method should return the whole DataFrame. 

### `bfs_pass` method

Like the method above, but for BFS. 

### Manual Debugging

Here is a code snippet you can use as you write your methods to help
test whether they're working:

```python
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# kill previous chrome instance if still around (to conserve memory)
os.system("pkill -f -9 chromium")

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path="chromium.chromedriver")

# TODO: use IP address of your VM
start_url = "http://YOUR_IP_HERE:5000/Node_1.html"

s = WebScraper(driver)
print(s.go(start_url))

dtravellog = s.dfs_pass(start_url)
print("\nDFS Travel Log\n", dtravellog)

btravellog = s.bfs_pass(start_url)
print("\nBFS Travel Log\n", btravellog)

s.driver.close()
```

Expected output:

```
['http://YOUR_IP_ADDRESS:5000/Node_2.html', 'http://YOUR_IP_ADDRESS:5000/Node_4.html']

DFS Travel Log
    clue   latitude   longitude                          description
0     1  43.089034  -89.416128              Picnic Point in Madison
1     7  38.105507  126.910613               Silver Beach in Hawaii
0     1  65.044901  -16.712836  Shore of a Volcanic Lake in Iceland
1     3  48.860945    2.335773                  The Louvre in Paris
0     5  37.434183 -122.321990      Redwood forest in San Francisco
0     4  29.975300   31.137600        Great Sphinx of Giza in Egypt
1     1  47.557600   10.749800     Neuschwanstein Castle in Germany
2     5  38.624700   90.184800        The Gateway Arch in St. Louis
3     3  30.328500   35.444400                      Petra in Jordan
4     2  41.480800   82.683400                    Cedar Point in OH
0     2  27.987586   86.925002                 Mt. Everest in Nepal
1     4  34.134117 -118.321495                 Hollywood Sign in LA
2     5  38.655100   90.061800                 Cahokia Mounds in IL
3     9  40.748400   73.985700          Empire State Building in NY
0     8  51.180315   -1.829659                 Stonehenge in the UK
0     6  43.070010  -89.409450          Quick Trip on Monroe Street

BFS Travel Log
    clue   latitude   longitude                          description
0     1  43.089034  -89.416128              Picnic Point in Madison
1     7  38.105507  126.910613               Silver Beach in Hawaii
0     1  65.044901  -16.712836  Shore of a Volcanic Lake in Iceland
1     3  48.860945    2.335773                  The Louvre in Paris
0     8  51.180315   -1.829659                 Stonehenge in the UK
0     5  37.434183 -122.321990      Redwood forest in San Francisco
0     2  27.987586   86.925002                 Mt. Everest in Nepal
1     4  34.134117 -118.321495                 Hollywood Sign in LA
2     5  38.655100   90.061800                 Cahokia Mounds in IL
3     9  40.748400   73.985700          Empire State Building in NY
0     4  29.975300   31.137600        Great Sphinx of Giza in Egypt
1     1  47.557600   10.749800     Neuschwanstein Castle in Germany
2     5  38.624700   90.184800        The Gateway Arch in St. Louis
3     3  30.328500   35.444400                      Petra in Jordan
4     2  41.480800   82.683400                    Cedar Point in OH
0     6  43.070010  -89.409450          Quick Trip on Monroe Street
```

# Individual Part (25%)

You have to do the remainder of this project on your own.  Do not
discuss with anybody except 320 staff (mentors, TAs, instructor).

## Part 3: `protected_df` method

The method should navigate to the given URL, enter the password into
the keypad, click GO, and return a String identifying the current location. In addition, the method should scrape and download the image of the current location, saving it as 'Current_Location.jpg'. 

Note that after clicking a button, there might be a slight delay
before `driver.page_source` reflects the new page.  Consider how you
can use `time.sleep(...)` to reduce the chance that this will happen
on some systems (like our test machine).

You may consider using the urllibrequest.urlretrieve() function to download the image (https://docs.python.org/3/library/urllib.request.html)

```python
url = "http://YOUR_IP_ADDRESS:5000/"
print(s.protected_df(url, DFS_OR_BFS_PASSWORD_HERE))
```

Should produce this:

```
BASCOM HALL

*AND you should see a 'Current_Location.jpg' appear in your working directory containing the image of the above location. 
```
