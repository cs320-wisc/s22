import os, sys, json, re

def main():
    used = []
    available = []
    
    for path in os.listdir("."):
        if path.endswith(".md"):
            with open(path) as f:
                used.extend(re.findall(r"\(\./(.+?)\)", f.read()))
        elif os.path.isdir(path):
            available.append(path)

    print("\n".join(sorted(set(available) - set(used))))

if __name__ == '__main__':
     main()
