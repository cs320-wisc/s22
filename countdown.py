import sys

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        count = 3
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        count = sys.argv[2]
    else:
        print("Usage: python3 countdown.py <filename> [count]")
        return

    f = open(filename, "w")
    for i in range(count):
        f.write(str(count-i) + "\n")
    f.close()

main()
