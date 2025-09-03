import requests
from bs4 import BeautifulSoup

CRAN_REPO_URL = (
    "https://cran.r-project.org/web/packages/available_packages_by_name.html"
)


def fetch_package_names():
    resp = requests.get(CRAN_REPO_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    spans = soup.find_all("span", class_="CRAN")
    # TODO: Check if Skip first 26 as in Makefile
    packages = [span.text for span in spans][26:]
    return packages


def save_packages(packages, filename="packages.txt"):
    with open(filename, "w") as f:
        for pkg in packages:
            f.write(pkg + "\n")
