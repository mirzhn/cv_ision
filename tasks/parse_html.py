import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

def load_html_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

def extract_skills(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements_with_skills = soup.find_all(text=lambda text: "Skills:" in text)
    skills = set()
    for element in elements_with_skills:
        parent_li = element.find_parent('li')
        if parent_li:
            all_spans = parent_li.find_all('span', {'aria-hidden': 'true'})
            for span in all_spans:
                skills.update(span.get_text(strip=True).split(' · '))
    return list(skills) if skills else ["N/A"]

def parse_date_range(date_range):
    date_range = date_range.split('·')[0].strip()
    date_pattern = re.compile(r'(\w+ \d{4}) - (Present|\w+ \d{4})')
    match = date_pattern.search(date_range)
    if match:
        start_date_str, end_date_str = match.groups()
        start_date = datetime.strptime(start_date_str, "%b %Y")
        end_date = datetime.now() if end_date_str == "Present" else datetime.strptime(end_date_str, "%b %Y")
        duration_months = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
        return f"{start_date_str} - {end_date_str}", duration_months
    return date_range, "N/A"

def extract_job_data(job):
    job_title = job.select_one('div.mr1.t-bold span[aria-hidden="true"]').text if job.select_one('div.mr1.t-bold span[aria-hidden="true"]') else 'N/A'
    company = job.select_one('span.t-14.t-normal span').text.split(' · ')[0] if job.select_one('span.t-14.t-normal span') else 'N/A'
    date_range_element = job.select('span.t-14.t-normal.t-black--light')[0].span if job.select('span.t-14.t-normal.t-black--light') else None
    location = job.select('span.t-14.t-normal.t-black--light')[1].span.text if len(job.select('span.t-14.t-normal.t-black--light')) > 1 else 'N/A'
    description = job.select_one('li.pvs-list__item--with-top-padding span[aria-hidden="true"]').text if job.select_one('li.pvs-list__item--with-top-padding span[aria-hidden="true"]') else 'N/A'
    
    job_html = str(job)
    skills = extract_skills(job_html)
    
    date_range = date_range_element.text if date_range_element else 'N/A'
    date_range_clean, duration_months = parse_date_range(date_range)

    return {
        "job_title": job_title,
        "company": company,
        "date_range": date_range_clean,
        "duration_months": duration_months,
        "location": location,
        "description": description,
        "skills": skills
    }

def extract_experience(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    jobs = soup.select('main.scaffold-layout__main section.artdeco-card li.pvs-list__paged-list-item')
    experience_dict = {}
    for job in jobs:
        job_data = extract_job_data(job)
        company = job_data.pop("company")
        if company not in experience_dict:
            experience_dict[company] = []
        experience_dict[company].append(job_data)
    return experience_dict

def save_to_json(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving to {file_path}: {e}")

def main():
    html_file_path = "../files/linkedin_profile.html"
    output_file_path = "../files/linkedin_experience.json"
    
    html_content = load_html_file(html_file_path)
    if html_content:
        experience_data = extract_experience(html_content)
        save_to_json(experience_data, output_file_path)

if __name__ == "__main__":
    main()