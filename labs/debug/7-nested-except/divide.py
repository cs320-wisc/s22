from datetime import datetime
import os, sys
import traceback

# try running this program on the terminal.  For example, you could run
# this to get 0.8:
# 
# python3 divide.py w x
#
# It has three issues (two of which require code changes!).  Try
# different inputs to discover them.
#
# Requirements for a correct program:
#
# 1. whenever there is user error causing an exception, the traceback
#    should be written to a file in the errors directory
# 2. all of the variables w, x, y, and z should be usable
# 3. if an invalid variable is used, that should also be caught

def main():
    variables = {"W": 80, "X": 100, "y": 2, "Z": 0}
    if len(sys.argv) != 3:
        print("Usage: python3 divide.py <VAR1> <VAR2>")
        print("Possible variables:", ",".join(sorted(variables.keys())))
        return

    try:
        var1, var2 = sys.argv[1:]
        val1, val2 = variables[var1.upper()], variables[var2.upper()]
        result = val1 / val2
        print(f"{val1}/{val2} = {result}")
    except ZeroDivisionError as e:
        print(repr(e))
        file_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt"
        with open(os.path.join("errors", file_name), "w") as f:
            f.write(traceback.format_exc())

if __name__ == '__main__':
     main()
