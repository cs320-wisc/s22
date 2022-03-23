import re, requests, os
from subprocess import check_output

r = requests.get("https://tyler.caraza-harter.com/cs320/s22/schedule.html")
r.raise_for_status()
d = dict(re.findall(r'<span id="lec-(.*?)-title">(.*?)</span>', r.text))
print(d)

for before, after in d.items():
    if os.path.exists(before):
        print(f"{before} => {before} {after}")
        print(check_output(["mv", before, before + " " + after]))
