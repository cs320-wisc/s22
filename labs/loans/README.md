# Loan Module

In these exercises, you'll start writing a `loans.py` module with
three Python classes you'll use for P2.  It's OK if you don't finish
these classe during lab time (you can finish them with your group or
alone later when working on P2).

## loans.py

In Jupyter, do the following:
1. go to s22/p2
2. click "New"
3. choose "Text File"
4. "File" > "Rename"
5. type "loans.py"

Using a .py module is easy -- just run `import some_mod` to run
`some_mod.py`, loading any function or classes it has.

In your `loans.py`, add a print like this:

```python
print("Hello from loans.py!")

def hey():
    print("Hey!")
```

Now lets import it to your project notebook.  Create a `p2.ipynb` in
the same directory as `loans.py`.

Run `import loans` in a cell.  You should see the first print!

You can also call the `hey` function now.  Try it:

```python
loans.hey()
```

If you change `hey` in `loans.py`, the new version won't automatically
reload into the notebook.  Add this so it will auto-reload:

```
%load_ext autoreload
%autoreload 2
```

Note this doesn't work all the time (if there's a bug in your
loans.py, you may need to do a Restart & Run All in the notebook after
fixing your module).

## `Applicant` class

We'll want to create a class to represent people who apply for loans.  Start with this in `loans.py`:

```python
class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            ????
```

We'll be using HDMA loan data
(https://www.ffiec.gov/hmda/pdf/2020guide.pdf), which uses numeric
codes to represent race.  Here are the codes from the documentation,
recorded in a dictionary:

```python
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
```

Paste the `dict` in your `loans.py` module, and use it to complete
your `__init__` constructor.  The loop should add entries in the
`race` parameter to the `self.race` attribute of the classes,
converting from the numeric codes to text in the process.  The `race`
attribute is a set because applicants often identify with multiple
options.

Simply skip over any entries in the `race` parameter that don't appear
in the `race_lookup` dict (e.g., we'll see and skip "6" later because
that code indicates a missing value).

Test the code you wrote in `loans.py` from your `p2.ipynb` notebook to
make sure the `Applicant.__init__` constructor properly fills the
`race` set.

```python
loan = loans.Applicant("20-30", ["1", "2", "3"])
loan.race
```

You should see this set:

```python
{'American Indian or Alaska Native', 'Asian', 'Black or African American'}
```

### `__repr__`

Add a `__repr__` method to your `Applicant` class:

```python
    def __repr__(self):
        ????
        return ????
```

Putting `loan` at the end of a cell or printing `repr(loan)` should show this:

```
Applicant('20-30', ['American Indian or Alaska Native', 'Asian', 'Black or African American'])
```

### `lower_age`

You might notice that ages are given as strings rather than ints
because we need to support ranges (like "20-30").

Add a `lower_age` method that returns an the lower int of an applicant's age range:

```python
    def lower_age(self):
        return ????
```

It should also support ages like "<75" (should just return the int
`75`) and ">25" (should just return the int `25`).

Try your method (you should get the int `20` since the age is "20-30"):

```python
loan.lower_age()
```

Hints: you could use `.replace` get get rid of unhelpful characters
(like "<" and ">").  After, splitting on "-" could help you find the
first number.

### `__lt__`

Recall that `__lt__` ("less than") lets you control what happens when two objects get compared.

`obj1 < obj2` automatically becomes `obj1.__lt__(obj2)`, and you can
write `__lt__` to return a True/False, indicating whether `obj1` is
less.

Complete the following for your `Applicant` class:

```python
    def __lt__(self, other):
        return ????
```

Comparisons should be based on age.  Python sorting will also use your
`__lt__` method.  Try it:

```python
sorted([
    loans.Applicant(">75", ["43", "44"]),
    loans.Applicant("20-30", ["1", "3"]),
    loans.Applicant("35-44", ["22"]),
    loans.Applicant("<25", ["5"]),
])
```

You should get this order:

```python
[Applicant('20-30', ['American Indian or Alaska Native', 'Black or African American']),
 Applicant('<25', ['White']),
 Applicant('35-44', ['Chinese']),
 Applicant('>75', ['Other Pacific Islander', 'Samoan'])]
```
