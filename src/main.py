import sys

from generate import generate_page, generate_pages_recursive
from static import copy_contents


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_contents("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
