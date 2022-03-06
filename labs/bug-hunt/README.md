# Bug Hunt

It's helpful to intentionally make various "mistakes", then make a
mental note of what exceptions occurs.  Then when you make
unintentional mistakes later and see that exception, it will help you
identify the problem more quickly.

Copy/paste the following code.  Replace each `pass # TODO` with some
code (could be multiple lines) that trigger an exception.  You're goal
is to trigger seven unique types of exception.

Suggestions:
* brainstorm with your group first about different kinds of mistakes, and make a list before writing the code
* we've used various modules this semester, which often have unique exceptions.  Think about what "mistakes" you can make with `math`, `json`, `subprocess`, `graphviz`, `pandas`, and `selenium`.


```python
exception_types = []

# error 1
try:
    x = 1 / 0
except Exception as ex:
    exception_types.append(type(ex))
    
# error 2
try:
    pass # TODO
except Exception as ex:
    exception_types.append(type(ex))
    
# error 3
try:
    pass # TODO
except Exception as ex:
    exception_types.append(type(ex))
    
# error 4
try:
    pass # TODO
except Exception as ex:
    exception_types.append(type(ex))
    
# error 5
try:
    pass # TODO
except Exception as ex:
    exception_types.append(type(ex))
    
# error 6
try:
    pass # TODO
except Exception as ex:
    exception_types.append(type(ex))
    
# error 7
try:
    pass # TODO
except Exception as ex:
    exception_types.append(type(ex))

# OPTIONAL: copy/paste if you want to find more than 7

print(f"You have found {len(set(exception_types))} out of 7 required")
exception_types
```
