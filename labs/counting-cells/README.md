# Counting Cells

Run the following:

```python
import numpy as np
a = np.array([
    [0,0,5,8],
    [1,2,4,8],
    [2,4,6,9],
])
```

How many even numbers are in this matrix?  What percentage of the
numbers are even?  We'll walk you through the solution.  Please run
each step (which builds on the previous) to see what's happening.

First step, mod by 2, to get a 0 in every odd cell:

```python
a % 2
```

Now, let's do an elementwise comparison to get a True in every place where there is an even number:

```python
a % 2 == 0
```

It will be easier to count matches if we represent True as 1 and False as 0:

```python
(a % 2 == 0).astype(int)
```

How many is that?

```python
(a % 2 == 0).astype(int).sum()
```

And what percent of the total is that?

```python
(a % 2 == 0).astype(int).mean() * 100
```

This may be useful for counting what percentage of an area matches a
given land type in P6.
