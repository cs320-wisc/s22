# P5: EDGAR Web Logs

## Corrections/Clarifications

* Apr 3: released tester.py and module_tester.py
* Apr 4: clarified what size we're measuring for q1
* Apr 5: clarified requirements for SIC code regex (see [corresponding lab page](https://github.com/cs320-wisc/s22/tree/main/labs/edgar-util)) and updated `module_tester.py` expected output
* Apr 6: updated `tester.py` expected output, updated Q11 expected output below
* Apr 7: clarified wording, added Q7 example
* Apr 14: note that by default reading inside a zip gives you bytes.  For your regex work, convert to a string using UTF-8 (like we have done for `check_output`).

## Overview

In the US, public companies need to regularly file
various statements and reports to the SEC's (Securities and Exchange
Commission) EDGAR database.  EDGAR data is publicly available online;
furthermore, web requests to EDGAR from around the world are logged
and published.  EDGAR logs are huge.  Logs for *just one day* might be
about 250 MB compressed as a .zip (or 2 GB uncompressed!).

We'll develop tools to extract information from the filings stored in EDGAR (this will be done in a Python module, `edgar_utils.py`) and we'll use those tools to analyze user behavior in `p5.ipynb`.

## Packages

You'll need to install some packages:

```
pip3 install --upgrade pip
pip3 install geopandas shapely descartes geopy netaddr
sudo apt install -y python3-rtree
```

## Testing

Be sure to run `python3 tester.py` regularly to estimate your grade. As in Project 2, the tester will both check the results of the analysis in your notebook, and use `module_tester.py` to check your `edgar_utils.py` module.

## Submission

As before, your notebook should have a comment like this:

```python
# project: p5
# submitter: ????
# partner: none
# hours: ????
```

You'll hand in two files:

- `p5.ipynb`
- `edgar_utils.py`

Combine these into a zip by running the following in the `p5` directory:

```
zip ../p5.zip p5.ipynb edgar_utils.py
```

Hand in the resulting p5.zip file.  Don't zip a different way (our
tests won't run if you have an extra directory inside your zip, for
example).

## Data format

Take a look at the list of daily zips and CSV documentation on the EDGAR site:

- https://www.sec.gov/dera/data/edgar-log-file-data-set.html
- https://www.sec.gov/files/EDGAR_variables_FINAL.pdf

We have provided a `server_log.zip` file, which is a subset of the
records from `log20170101.zip`. Since you'll need to work with a lot of zipped files for this project, you'll want to know some command line techniques
to troubleshoot.

View names of files in a zip file:

```
unzip -l server_log.zip
```

View the start of a file inside of a zip file (change "head" to "tail"
to see the end):

```
unzip -p server_log.zip rows.csv | head -n 5
```

The expected result is:

```
ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser
104.197.32.ihd,2017-01-01,00:00:00,0.0,1111711.0,0001193125-12-324016,-index.htm,200.0,7627.0,1.0,0.0,0.0,10.0,0.0,
208.77.214.jeh,2017-01-01,00:00:00,0.0,789019.0,0001193125-06-031505,.txt,200.0,46327.0,0.0,0.0,0.0,10.0,0.0,
54.197.228.dbe,2017-01-01,00:00:00,0.0,800166.0,0001279569-16-003038,-index.htm,200.0,16414.0,1.0,0.0,0.0,10.0,0.0,
108.39.205.jga,2017-01-01,00:00:01,0.0,354950.0,0000950123-09-011236,-index.htm,200.0,8718.0,1.0,0.0,0.0,10.0,0.0,
```

Looking at the `cik`, `accession`, and `extention` fields tells you what web resoure a user was requesting (in particular, each company has it's own `cik`):

```
ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser,region
54.212.94.jcd,2017-01-01,03:31:36,0.0,1461219.0,0001209191-21-001287,-index.htm,301.0,243.0,1.0,0.0,1.0,10.0,0.0,,United States of America
...
```

For this row, we can construct the following URL from `1461219.0`, `0001209191-21-001287`, and `-index.htm`:

https://www.sec.gov/Archives/edgar/data/1461219/0001209191-21-001287-index.htm

Looking at this page and its source (as well as the source of the pages where your parser does not behave as expected) is highly recommended and will be very important later in the project.

We have already downloaded the docs for a subset of the requests in
`server_log.zip` for you and placed them in `docs.zip`. Note, however, that the file structure is slightly different than the URL above. The path in the zip to that file would be "1461219/0001209191-21-001287/-index.htm".


# Group Part (75%)

## Part 1: `server_log.zip` analysis

Answer these questions in `p5.ipynb`.

### Q1: what's the total size in bytes of the files requested?

Look at the `size` column of the CSV in `server_log.zip`.  We want to
count duplicates here; this gives us an estimate of the amount of
network traffic handled by EDGAR (since this data is only a sample,
the true value will be even larger). Answer with an integer.

### Q2: how many filings have been accessed by the top ten IPs?

Answer with a dictionary, with the (anonymized) IP as key and the number of requests seen in the logs as the values. Each row in the logs corresponds to one request. Note that the anonymized IP addresses are consistent between requests.

**Hint:** for this question and most of the others expecting dictionary output, it might be easiest to use Pandas operations to process the data into a `Series` and to use the `to_dict()` method. Consider using tools like `groupby`, `apply`, and aggregation methods like `size()`.

### Q3: what fraction of the requests had errors?

Count any request with a status code greater than or equal to 400 as having resulted in an error. Answer with a floating point number.

### Q4: what is the most frequently accessed file?

Answer with a string formatted like so: "cik/accession/extention" (these are the names of columns in "rows.csv").

### Q5: how many requests were made by automated crawlers?

Only count the requests made by users who were identified as crawlers (see the crawler column); considering the results of Q2, this is likely to be a vast underestimate. Answer with an integer.

## Part 2: creating `edgar_utils.py` module

This part is to be started during the [weekly lab](../labs/lab11.md).
Finish the `edgar_utils.py` module now if you didn't have enough time
during the scheduled lab.

## Part 3: using `edgar_utils.py` module

### Q6: which region uses EDGAR most heavily?

Use your `lookup_region` function and answer with a string.

### Q7: what fraction of IPs in each region are high-volume users?

Consider IPs which accessed more than 1000 EDGAR resoures to be
high-volume. This might indicate machines running automated scraping
and analysis tasks.

Note that given the sampling done in the data, the true EDGAR usage of
these machines is likely to be even heavier.

Answer with a dictionary, where the keys are the regions and the
values are the fraction (in floating point form) of IPs from that
region classified as high-volume.

**Example:**

Say "United States of America" has four IPs:
* 1.1.1.1 appears 1200 times in the logs
* 2.2.2.2 appears 900 times in the logs
* 3.3.3.3 appears 5 times in the logs
* 4.4.4.4 appears 234 times in the logs

This means that 1/4 of the IPs in the US are high volume, so there should be an entry like this:

```
{
    "United States of America": 0.25,
    ...
}
```

### Q8: what dates appear in the `850693/0000850693-07-000159/-index.htm` file of `docs.zip`?

Read the HTML from this file and use it to create a `Filing` object,
from which you can access the `.dates` attribute.

**Suggestion:** read every .htm or .html file in `docs.zip`, creating a
`Filing` object from each.  Save the Filing objects in a dict, keyed
by filename, so you don't need to re-read the data for each of the
following questions.

### Q9: what is the distribution of states for the filings in `docs.zip`?

Answer with a dict, like the following:

```
{'CA': 91,
 'NY': 83,
 'TX': 64,
 'MA': 30,
 'PA': 25,
 'IL': 25,
 ...
}
```

### Q10: what is the distribution of SIC codes for the filings in `docs.zip`?

Answer in the same format as in the previous question.  This time,
skip any `None` values (`None` shouldn't be a key in the final dict).

If you're curious, consider looking up the industry names for the top
couple categories:
https://www.sec.gov/corpfin/division-of-corporation-finance-standard-industrial-classification-sic-code-list

# Individual Part (25%)

## Part 4: combining logs with documents

### Q11: what is the distribution of requests across industries?

For each request in the logs that has a corresponding filing in
`docs.zip`, lookup the SIC (ignore rows in the logs which refer to
pages not in `docs.zip`).

Answer with a dictionary, where the keys are the SIC and the values
are the number of times the resources of that industry were accessed.

Expected output:

```
{2834: 984,
 1389: 656,
 1311: 550,
 2836: 429,
 6022: 379,
 1000: 273,
 ...
 }
 ```

### Q12: how many requests were made in each hour?

Use `pd.to_datetime` (the `hour` attributes of the converted
timestamps may be useful) or string manipulation to process the `time`
column. Answer with a dictionary, where the keys are integers from 0
to 23 representing the hour of the day, and the values are the number
of requests made in that hour.

### Q13: what is the geographic overlap in interest between Australia, France, and Viet Nam?

Answer with a Digraph like the following:

<img src="digraph.png" width=400>

In addition to a node for each of these three countries, there should
be a node for each state having a filing accessed by somebody in one
of these countries.

An edge from a country to a state means somebody in that country
looked at least one filing for a company in that state.

### Q14: what are the most commonly seen street addresses?

For each web request that has a corresponding filing, count each of
the addresses for that filing.

Show a dictionary of counts for all addresses appearing at least 225
times.

### Q15: geographic plotting of headquarters

The `locations.geojson` contains the positions of some of the
addresses in the dataset.  Plot this over the background map in
"shapes/cb_2018_us_state_20m.shp"

Additional requirements:

* crop to the following lat/lon bounds:

```python
west = -130
east = -55
north = 50
south = 20
```

* use a Mercator projection, "epsg:3395"
* the color of each point should indicate how many times a request has accessed a filing with that address (consider adding data you computed in the previous question to a column in the GeoDataFrame you get from `locations.geojson`)
* use the "plasma" colormap, with a colorbar

The result should look similar to this:

![](geo.svg)

Depending on how you you approach the problem, the zorder of the
scatter points may be different -- this is not a problem.

Note, we used `geopandas.geocode` to find the locations for each address in
`locations.geojson`.  This will generally be useful to you on other
projects, but we're providing you the pre-computed `locations.geojson`
here so your code runs faster.

# Conclusion

The EDGAR logs are supposedly anonymized (with the last three docs
left), but we can still tell where the users live and what they're
looking at.

 By connecting the filing information with the logs, we can learn a lot about the behavior of the investment firms which use the database - for example, we might learn which companies (or industries) a hedge fund might be considering investing in, and the extent to which it relies on automated vs manual research in its trading.

Others have used this same data to make good guesses
about what docs various hedge funds and others are looking at, then
correlate that with success.  For those interested in the nitty-gritty
details of what could be done with this data, take a look at this
early-stage work: [Hedge Funds and Public Information
Acquisition](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3127825).
