import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.co.uk/jobs?q=python&limit={LIMIT}"

def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page

def extract_job (html):
    # extract title
    title = html.find("div", {"class": "title"}).find("a")["title"]

    # extract company
    company = html.find("span", {"class": "company"})
    if company is not None:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = company_anchor.string
        else:
            company = company.string
    else:
        company = "Null"
    company = company.strip()

    # extract location
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    # extract Job Apply link
    job_id = html["data-jk"]

    return {"title": title, "company": company, "location": location, "apply_link": f"https://www.indeed.co.uk/viewjob?jk={job_id}"}

def get_jobcards(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page: {page+1}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_pages = get_last_pages()
    jobs = get_jobcards(last_pages)
    return jobs
