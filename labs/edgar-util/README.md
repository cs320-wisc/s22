# Lab: EDGAR Utilities Module

In the US, public companies need to regularly file various statements
and reports to the SEC's (Securities and Exchange Commission) EDGAR
database.  EDGAR data is publicly available online; furthermore, web
requests to EDGAR from around the world are logged and published.  For
P5, you'll analyze both SEC filing HTML pages and a log of web
requests from around the world for those pages.

In this lab, you'll create an `edgar_utils.py` to help with analyzing
the pages and logs.  It will contain two things: a `lookup_region`
function and a `Filing` class.

## Practice for `lookup_region`

For "practice" components of this lab, you'll do exercises in a
notebook to get the code and logic correct.  You'll then use what you
learn to write your `edgar_utils.py` module.

### Exercise 1: replace letters

For the project dataset, you'll be working with some IP addresses
where some of the digits have been replaced with letters for
anonymization.

For some calculations, we need only digits, so we'll replace any
letters with "0".  Complete the following regex code to get back
"101.1.1.abc":

```python
import re
ipaddr = "101.1.1.abc"
re.sub(????, ????, ipaddr)
print(ipaddr)
```

### Exercise 2: integer IPs

Note if you haven't installed netaddr yet from p5, please install it from the command line via: 
``` pip3 install netaddr```

IP addresses are commonly represented as four-part numbers, like
"34.67.75.25".  To convert an address like this to an integer, you can
use the following::
```python
import netaddr
int(netaddr.IPAddress("34.67.75.25"))
```

Modify the above to lookup the integer representation of your virtual
machine's IP address.

### Exercise 3: binary search

Consider the following sorted list:

```python
L = [1, 2, 100, 222, 900]
```

Running `150 in L` would loop over every element in the list.  This is
slow, and doesn't take advantage of the fact that the list is sorted.
A better strategy when we know it is sorted would be to check the
middle (100) and infer 150 must be in the second half of the list, if
it's in the list at all; no need to check the first half.

A famous algorithm that uses this strategy is called *binary search*, and it's implemented by this function: https://docs.python.org/dev/library/bisect.html#bisect.bisect

Try it:
```python
from bisect import bisect
idx = bisect(L, 150)
idx
```

You should get `3` -- this means that if you wanted to add 150 to the
list and keep it in sorted order, you would insert 150 at index 3
(after 1, 2, and 100).  This also means `L[idx-1]` is the biggest
number in the list that is **less than or equal** to 150.

*What will bisect of `L` be for 225?* Write down your prediction, then
run code to check your answer.

### Exercise 4: country/region lookup

You can generally guess what country or region a computer is in based
on its IP address.  Read in `ip2location.csv` from the project to see
the IP ranges assigned to each region (this is borrowed from
https://lite.ip2location.com/database/ip-country).

```python
ips = pd.read_csv("ip2location.csv")
ips
```

Can you use (a) `bisect` on the `low` column of `ips` and (b) the
integer representation of your VM's IP address to (c) find an `idx`
for the row in `ips` corresponding to your VM?

Look at `ips.iloc[idx]` to make sure you found the correct row.

## `lookup_region` function

Write an efficient `lookup_region` function in your `edgar_utils.py`
module that takes an IP address (in string form) and returns the
country or region the corresponding computer is in.  You can import it
and test it in Jupyter notebooks or Python interactive mode.

Example usage:
```python
>>> lookup_region("1.1.1.x")
'United States of America'
>>> lookup_region("101.1.1.abc")
'China'
```

Requirements:
* it needs to worked with anonymized IPs
* don't read the CSV file each time `lookup_region` is called
* don't loop over every row each time `lookup_region` is called -- your code needs to be faster than O(N)

## Practice for `Filing` class

Copy/paste the following string to a notebook:

```python
html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Last-Modified" content="Fri, 12 Feb 2016 00:05:37 GMT" />
<title>EDGAR Filing Documents for 0001050470-16-000051</title>
<link rel="stylesheet" type="text/css" href="/include/interactive.css" />
</head>
<body style="margin: 0">
<!-- SEC Web Analytics - For information please visit: https://www.sec.gov/privacy.htm#collectedinfo -->
<noscript><iframe src="//www.googletagmanager.com/ns.html?id=GTM-TD3BKV"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TD3BKV');</script>
<!-- End SEC Web Analytics -->
<noscript><div style="color:red; font-weight:bold; text-align:center;">This page uses Javascript. Your browser either doesn't support Javascript or you have it turned off. To see this page as it is meant to appear please use a Javascript enabled browser.</div></noscript>
<!-- BEGIN BANNER -->
<div id="headerTop">
   <div id="Nav"><a href="/index.htm">Home</a> | <a href="/cgi-bin/browse-edgar?action=getcurrent">Latest Filings</a> | <a href="javascript:history.back()">Previous Page</a></div>
   <div id="seal"><a href="/index.htm"><img src="/images/sealTop.gif" alt="SEC Seal" border="0" /></a></div>
   <div id="secWordGraphic"><img src="/images/bannerTitle.gif" alt="SEC Banner" /></div>
</div>
<div id="headerBottom">
   <div id="searchHome"><a href="/edgar/searchedgar/webusers.htm">Search the Next-Generation EDGAR System</a></div>
   <div id="PageTitle">Filing Detail</div>
</div>
<!-- END BANNER -->


<!-- BEGIN BREADCRUMBS -->
<div id="breadCrumbs">
   <ul>
      <li><a href="/index.htm">SEC Home</a> &#187;</li>
      <li><a href="/edgar/searchedgar/webusers.htm">Search the Next-Generation EDGAR System</a> &#187;</li>
      <li><a href="/edgar/searchedgar/companysearch.html">Company Search</a> &#187;</li>
      <li class="last">Current Page</li>
   </ul>
</div>
<!-- END BREADCRUMBS -->

<div id="contentDiv">
<!-- START FILING DIV -->
<div id="formDiv">
   <div id="formHeader">
      <div id="formName">
         <strong>Form SC 13G</strong> - Statement of acquisition of beneficial ownership by individuals: 
      </div>
      <div id="secNum">
         <strong><acronym title="Securities and Exchange Commission">SEC</acronym> Accession <acronym title="Number">No.</acronym></strong> 0001050470-16-000051
      </div>
   </div>
   <div class="formContent">
      <div class="formGrouping">
         <div class="infoHead">Filing Date</div>
         <div class="info">2016-02-12</div>
         <div class="infoHead">Accepted</div>
         <div class="info">2016-02-11 19:05:37</div>
         <div class="infoHead">Documents</div>
         <div class="info">1</div>
      </div>
      <div style="clear:both"></div>
   </div>
</div>
<!-- END FILING DIV -->
<!-- START DOCUMENT DIV -->
<div id="formDiv">
   <div style="padding: 0px 0px 4px 0px; font-size: 12px; margin: 0px 2px 0px 5px; width: 100%; overflow:hidden">
      <p>Document Format Files</p>
      <table class="tableFile" summary="Document Format Files">
         <tr>
            <th scope="col" style="width: 5%;"><acronym title="Sequence Number">Seq</acronym></th>
            <th scope="col" style="width: 40%;">Description</th>
            <th scope="col" style="width: 20%;">Document</th>
            <th scope="col" style="width: 10%;">Type</th>
            <th scope="col">Size</th>
         </tr>
         <tr>
            <td scope="row">1</td>
            <td scope="row">LSV13G123115MEDALLION.TXT</td>
            <td scope="row"><a href="/Archives/edgar/data/1000209/000105047016000051/lsv13g123115medallion.txt">lsv13g123115medallion.txt</a></td>
            <td scope="row">SC 13G</td>
            <td scope="row">8314</td>
         </tr>
         <tr class="blueRow">
            <td scope="row">&nbsp;</td>
            <td scope="row">Complete submission text file</td>
            <td scope="row"><a href="/Archives/edgar/data/1000209/000105047016000051/0001050470-16-000051.txt">0001050470-16-000051.txt</a></td>
            <td scope="row">&nbsp;</td>
            <td scope="row">9803</td>
         </tr>
      </table>	
   </div>
</div>
<!-- END DOCUMENT DIV -->
<!-- START FILER DIV -->
<div id="filerDiv">
   <div class="mailer">Mailing Address
      <span class="mailerAddress">437 MADISON AVENUE</span>
      <span class="mailerAddress">38TH FLOOR</span>
      <span class="mailerAddress">
NEW YORK NY 10022      </span>
   </div>
   <div class="mailer">Business Address
      <span class="mailerAddress">437 MADISON AVE 38 TH FLOOR</span>
      <span class="mailerAddress">
NEW YORK NY 10022      </span>
      <span class="mailerAddress">2123282153</span>
   </div>
<div class="companyInfo">
  <span class="companyName">MEDALLION FINANCIAL CORP (Subject)
 <acronym title="Central Index Key">CIK</acronym>: <a href="/cgi-bin/browse-edgar?CIK=0001000209&amp;action=getcompany">0001000209 (see all company filings)</a></span>
<p class="identInfo"><acronym title="Internal Revenue Service Number">IRS No.</acronym>: <strong>043291176</strong> | State of Incorp.: <strong>DE</strong> | Fiscal Year End: <strong>1231</strong><br />Type: <strong>SC 13G</strong> | Act: <strong>34</strong> | File No.: <a href="/cgi-bin/browse-edgar?filenum=005-48473&amp;action=getcompany"><strong>005-48473</strong></a> | Film No.: <strong>161413579</strong><br /><acronym title="Standard Industrial Code">SIC</acronym>: <b><a href="/cgi-bin/browse-edgar?action=getcompany&amp;SIC=6199&amp;owner=include">6199</a></b> Finance Services<br />Office of Finance</p>
</div>
<div class="clear"></div>
</div>
<div id="filerDiv">
   <div class="mailer">Mailing Address
      <span class="mailerAddress">155 NORTH WACKER DRIVE</span>
      <span class="mailerAddress">SUITE 4600</span>
      <span class="mailerAddress">
CHICAGO IL 60606      </span>
   </div>
   <div class="mailer">Business Address
      <span class="mailerAddress">155 NORTH WACKER DRIVE</span>
      <span class="mailerAddress">SUITE 4600</span>
      <span class="mailerAddress">
CHICAGO IL 60606      </span>
      <span class="mailerAddress">312-460-2443</span>
   </div>
<div class="companyInfo">
  <span class="companyName">LSV ASSET MANAGEMENT (Filed by)
 <acronym title="Central Index Key">CIK</acronym>: <a href="/cgi-bin/browse-edgar?CIK=0001050470&amp;action=getcompany">0001050470 (see all company filings)</a></span>
<p class="identInfo"><acronym title="Internal Revenue Service Number">IRS No.</acronym>: <strong>232772200</strong> | State of Incorp.: <strong>DE</strong> | Fiscal Year End: <strong>1231</strong><br />Type: <strong>SC 13G</strong></p>
</div>
<div class="clear"></div>
</div>
<!-- END FILER DIV -->
</div>"""
```

### Exercise 1: dates

Write a regular expression finding all the dates with the `YYYY-MM-DD`
format in the document.  It's OK if you have extra groups within your
matches.

```python
import re
re.findall(r"????", html)
```

You might have some extra matches like `0470-16-00` that are clearly
not dates.  Add some additional filtering so that you only count
4-digit numbers as years if they start as 19XX or 20XX.  You could do
this in the regular expression itself, or in some additional Python
code that loops over the results of the regular expression.

### Exercise 2: Standard Industrial Classification (SIC) codes

Take a look at the industry codes defined here: https://www.sec.gov/corpfin/division-of-corporation-finance-standard-industrial-classification-sic-code-list

Write a regular expression to find the first number following the text
"SIC" in `html`.  There may be other characters (not digits) between
"SIC" and the number, so be sure to allow that.  You should find 6199
in this case.

### Exercise 3: Addresses

To find addresses, we'll look at the HTML.  We want to find the
contents between `<div class="mailer">` and `</div>`.  We want the
non-greedy version (meaning that if there are multiple `</div>`
instances, we want to match the first one possible).

Write a regular expression to do this:

```python
for addr_html in re.findall(????, html):
    print(addr_html)
```

Note, the text between the opening and closing `div` tags generally
spans multiple lines.  Remember that `.` does not match newlines.  One
way to match anything is with `[\s\S]` (meaning whitespace or not
whitespace; in other words, everything).  If you get very stuck on
this one, you can scroll past the expected output to see one solution
for finding `addr_html` matches.

Expected output:

```
Mailing Address
      <span class="mailerAddress">437 MADISON AVENUE</span>
      <span class="mailerAddress">38TH FLOOR</span>
      <span class="mailerAddress">
NEW YORK NY 10022      </span>
   
Business Address
      <span class="mailerAddress">437 MADISON AVE 38 TH FLOOR</span>
      <span class="mailerAddress">
NEW YORK NY 10022      </span>
      <span class="mailerAddress">2123282153</span>
   
Mailing Address
      <span class="mailerAddress">155 NORTH WACKER DRIVE</span>
      <span class="mailerAddress">SUITE 4600</span>
      <span class="mailerAddress">
CHICAGO IL 60606      </span>
   
Business Address
      <span class="mailerAddress">155 NORTH WACKER DRIVE</span>
      <span class="mailerAddress">SUITE 4600</span>
      <span class="mailerAddress">
CHICAGO IL 60606      </span>
      <span class="mailerAddress">312-460-2443</span>
```

Now, extend your above loop so that a further regex search is
conducted for address lines within each `addr_html` match.  Address
lines are between `<span class="mailerAddress">` and `</span>`:

```python
for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
    lines = []
    for line in re.findall(????, addr_html):
        lines.append(line.strip())
    print("\n".join(lines))
    print()
```

## `Filing` class

Add a `Filing` class to your `edgar_utils.py` like this:

```python
class Filing:
    def __init__(self, html):
        self.dates = ????
        self.sic = ????
        self.addresses = ????

    def state(self):
        return "TODO"
```

`html` will be an HTML string, much like the one you were working with
in the practices.  Fill in the missing parts and add additional lines
as needed.  Much of the code from the practice exercises will be
useful here.

* `dates` should be a list of dates in the `YYYY-MM-DD` format that appear in the HTML (only count years starting as 19XX or 20XX)
* `sic` should be an `int` indicating the Standard Industrial Classification.  It should be `None` if this doesn't appear.
* `addresses` should be a list of addresses found in the HTML.  Each address will contain the address lines separated by newlines, but otherwise there shouldn't be unnecessary whitespace.
* `state()` should loop over the addresses.  If it finds one that contains two capital letters followed by 5 digits (for example, "WI 53706"), it should return what appears to be a state abbreviation (for example "WI").  You don't need to check that the abbreviation is a valid state.  If nothing that looks like a state abbreviation appears, return `None`.
