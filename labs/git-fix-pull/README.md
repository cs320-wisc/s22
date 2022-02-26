# Fixing Git Pull

For our 320 repo (and in general), you should run `git pull` often so
you'll have the latest code/test/etc.

A common situation where `git pull` doesn't work is when (a) there's a
new version of some file on GitHub and (b) you made changes to the old
version on your computer.  Git doesn't want to pull because it doesn't
want to erase your changes.

Let's practice resolving this issue.

1. on your VM, `cd` to `labs/git-fix-pull` in our semester repo
2. run `unzip pull.zip`
3. this creates a repo, `pull-practice` -- `cd` into it
4. edit `example.py` so that it prints "Hello World" instead of just "Hello"
5. run `git status` and `git diff` to see the change
6. try running `git pull`

You should see an error like this:

```
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 3 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), 267 bytes | 267.00 KiB/s, done.
From https://github.com/cs320-wisc/pull-practice
   729fc4a..30dccb4  main       -> origin/main
Updating 729fc4a..30dccb4
error: Your local changes to the following files would be overwritten by merge:
	example.py
Please commit your changes or stash them before you merge.
Aborting
```

There's a new version of `example.py` on GitHub, but git doesn't want
to overwrite your change.  One was to fix this is with "stashing", as
the error suggests.  We won't cover stashing in 320, but feel free to
read about it on your own.

The easiest way to solve this is to undo your changes (perhaps after
backing them up to another file), then pull again.  Let's try that:

7. `cp example.py backup-example.py`
8. `git checkout example.py` (this undoes your changes)
9. `git pull`

You'll now have the version with your changes in `backup-example.py`
and the latest version from GitHub in `example.py`.
