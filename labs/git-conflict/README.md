# Git Merging (and conflicts)

1. In an SSH session, run `export EDITOR=nano` so that `nano` is your default editor for the following practice

2. navigate (with `cd`) to `labs/git-conflict` within the semester repo.  Run `unzip repo.zip` to create a `repo` directory, which contains an `adder.py` program.

3. `cd` to the `repo` directory and run the program: `python3 adder.py`.

4. use `ls` and `cat` (or `nano`) to browse the file(s) in the repo

5. run `git branch`, making a note of what branch the HEAD is currently on (the `*` indicates the `HEAD`).  Make a note of the other branches.

6. your job is to merge the other branches into the main branch, using `git merge ????` commands.  After each merge, check what files are in the directory you're working and what they contain.

7. when you're all done, delete the other branches (keeping only the `main` branch): `git branch -D ????`

**Notes:**

* the first merge you do will be easiest, because it is a roll forward merge.  Each of the three branches share a common history with `main`, so `main` can just catch up with the latest commits
* the changes on the `docs` branch are on a separate file (README.txt), so that will never conflict with the other changes
* there will be a conflict once you've tried to merge both `args` and `func-rename`.  Resolve it.

**Conflict resolution hints:**

* use `nano` to open the file with the conflict.  The file will contain conflicting code.  Edit everything so you have the version you want, and the extra characters added by git are removed.
* whenever you aren't sure of the next step, run `git status` to get the hint about how to "mark resolution" or "conclude the merge"

When you're all done, the `adder.py` program should look like this:

```python
import sys

print("Welcome to the adder program!")

def add(x, y):
    print(f"{x} plus {y} is {x+y}")

if len(sys.argv) == 3:
    add(int(sys.argv[1]), int(sys.argv[2]))
else:
    print("Usage: python3 adder.py <x> <y>")

print("Bye")
```

And it should be runnable like this (promt will vary):

```
PROMPT$ python3 adder.py 3 5
Welcome to the adder program!
3 plus 5 is 8
Bye

```
