import requests
import pandas as pd
import re
from urllib.parse import urlparse
import dask
from dask import delayed


def clean_domain(url):
    """Remove prefixes like http, https, www and trailing slashes."""
    url = url.lower().strip()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    return url.rstrip('/')

@delayed
def check_domain_for_dask(domain, prefixes, session):
    """Check the status of a single domain (wrapped for Dask)."""
    status_code = None
    status = "Invalid"
    redirected_domain = ""
    
    # Check domain with and without prefixes
    for prefix in prefixes:
        url = prefix + domain
        try:
            response = session.get(url, timeout=5, allow_redirects=True)
            status_code = response.status_code
            final_url = response.url
            cleaned_final_url = clean_domain(final_url)
            cleaned_input_domain = clean_domain(domain)
            
            if response.ok:
                if cleaned_input_domain == cleaned_final_url:
                    status = "Valid"
                else:
                    status = "Redirected"
                    redirected_domain = cleaned_final_url
                break
                
        except requests.RequestException:
            continue
    
    return {
        "input domain": domain, 
        "status code": status_code, 
        "status": status, 
        "redirected domain": redirected_domain
    }

def check_domain_status(input_file, output_file):
    df = pd.read_csv(input_file, low_memory=False)
    column_name = df.columns[0]
    domains = df.iloc[:, 0].dropna().astype(str).tolist()

    # Request headers and URL prefixes
    headers = {"User-Agent": "Mozilla/5.0"}
    prefixes = ["", "https://", "https://www.", "http://", "http://www."]
    
    # Initialize a session for better performance
    session = requests.Session()
    session.headers.update(headers)
    
    results = []

    for domain in domains:
        results.append(check_domain_for_dask(domain, prefixes, session))
    
    results = dask.compute(*results)
    
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, index=False)


check_domain_status("your_input_file.csv", "your_output_file.csv")    