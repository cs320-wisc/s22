# BSTs (Binary Search Trees)

In this lab, you'll create a BST that can be used to lookup values by
a key (it will behave a bit like a Python dict where the all the dict
values are lists of values).  You'll use the BST for P2.

## Basics Node and BST classes

Start by pasting+completing the following:

```python
class Node():
    def __init__(self, key):
        self.key = ????
        self.values = []
        self.left = None
        ????
```

Let's create a `BST` class with an `add` method that automatically
places a node in a place that preserves the search property (i.e., all
keys in left subtree are less than a parent's value, which is less
than those in the right tree).

Add+complete with the following.  Note that this is a non-recursive
version of `add`:

```python
class BST():
    def __init__(self):
        self.root = None

    def add(self, key, val):
        if self.root == None:
            self.root = ????

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left == None:
                    curr.left = Node(key)
                curr = curr.left
            elif key > curr.key:
                 # go right
                 ????
                 ????
                 ????
            else:
                # found it!
                assert curr.key == key
                break

        curr.values.append(val)
```

## Dump

Let's write some methods to BST to dump out all the keys and values (note
that "__" before a method name is a hint that it is for internal use
-- methods inside the class might call `__dump`, but code outside the
class probably shouldn't):

```python
    def __dump(self, node):
        if node == None:
            return
        self.__dump(node.right)            # 1
        print(node.key, ":", node.values)  # 2
        self.__dump(node.left)             # 3

    def dump(self):
        self.__dump(self.root)
```

Try it:

```python
tree = BST()
tree.add("A", 9)
tree.add("A", 5)
tree.add("B", 22)
tree.add("C", 33)
tree.dump()
```

You should see this:

```
C : [33]
B : [22]
A : [9, 5]
```

Play around with the order of lines 1, 2, and 3 in `__dump()` above.  Can you
arrange those three so that the output is in ascending alphabetical
order, by key?

## Length

Add a special method `__len__` to `Node` so that we can find the size
of a tree.  Count every entry in the `.values` list of each `Node`.

```python
    def __len__(self):
        size = len(self.values)
        if self.left != None:
            size += ????
        ????
            ????
        return size
```

```python
t = BST()
t.add("B", 3)
assert len(t.root) == 1
t.add("A", 2)
assert len(t.root) == 2
t.add("C", 1)
assert len(t.root) == 3
t.add("C", 4)
assert len(t.root) == 4
```

Discuss with your neighbour: why not have a `Node.__dump(self)` method
instead of the `BST.__dump(self, node)` method?

<details>
<summary>Answer</summary>

Right now, it is convenient to check at the beginning if `node` is
None.  A receiver (the `self` parameter) can't be None if the
`object.method(...)` syntax is used (you would get the
"AttributeError: 'NoneType' object has no attribute 'method'" error).
We could have a `Node.__dump(self)` method, but then we would need to do the None checks on both `.left` and `.right`, which is slightly longer.
</details>

## Lookups

Write a `lookup` method in `Node` that returns all the values that match a given key.  Some examples:

* `t.root.lookup("A")` should return `[2]`
* `t.root.lookup("C")` should return `[1, 4]`
* `t.root.lookup("Z")` should return `[]`

Some pseudocode for you to translate to Python:

```
lookup method (takes key)
    if key matches my key, return my values
    if key is less than my key and I have a left child
        call lookup on my left child and return what it returns
    if key is greater than my key and I have a right child
        call lookup on my right child and return what it returns
    otherwise return an empty list
```

## `search.py` module

If you've been developing your `BST` and `Node` classes in a notebook,
you should now move them to a module called `search.py` in your `p2`
directory.
