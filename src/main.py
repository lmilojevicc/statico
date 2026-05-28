from generate import generate_page, generate_pages_recursive
from static import copy_contents


def main():
    copy_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
