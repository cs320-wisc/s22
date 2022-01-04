import os, sys, json, re, base64
from subprocess import check_output, DEVNULL
import tester

def build(ipynb):
    md_path = ipynb.replace(".ipynb", ".md")
    with open(ipynb) as f, open(md_path, "w") as md:
        nb = json.load(f)
        cells = nb["cells"]
        for cell in cells:
            if cell["cell_type"] == "markdown":
                md.write("".join(cell["source"]) + "\n\n")

default_notes = {
    "float": "tolerance=0.000001",
    "str": "case=strict",
    "list": "order=strict",
}

def main():
    if len(sys.argv) == 1:
        print("Specify the path to at least one .ipynb file")
    for path in sys.argv[1:]:
        assert path.endswith(".ipynb")

        # dump test results first so we can embed them in the HTML doc
        if not "lab" in path:
            tester.dump_results(path, path.replace(".ipynb", ".csv"), default_notes=default_notes)

        # ipynb => md => HTML
        build(path)

if __name__ == '__main__':
     main()
