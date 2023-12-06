"""



conda activate Aws

python ./check_domain_keywords_ver_a04.py \


# Output: [
        +1,  # The domain contained the keyword.
        0,   # The domain DID NOT contain the keyword.
        -1,  # Other erroe cases.
        ]

# Google search "site" option.
- Do not insert a space between "site:" and an url.
- ~488 characters in the empty search result page (SRP).
- ~670 characters for a SRP containing one search hit.



"""

import requests, time
from bs4 import BeautifulSoup



def judge_by_google_site_option(
        keyword = "バナナ", 
        target_url = "https://pig-data.jp/", 
        verbose = True, 
        debug = False, 
        ):
    """ 
    - Target search engine is google.com .
    - Thresholding against the text length of a Google search result page.
    """
    url_of_proxy = 'http://brd-customer-hl_c4d84340-zone-testing:su1m4td6rxw0@brd.superproxy.io:22225'
    
    proxies = {
        'http': url_of_proxy,
        'https': url_of_proxy,
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    
    query = f"site:{target_url} \"{keyword}\""

    num_results = 1
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    response = requests.get(url, headers=headers, proxies=proxies)

    message = -1
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ''.join(soup.get_text("\n"))
        score = len(text)
        if score > 550:
            message = +1
        else:
            message = 0
    
    if verbose: print(message, query)
    if debug: print(message)

    return message


def scrape():
    
    def sanitize_lines(lines):
        atoms = list()
        for line in lines:
            atom = line.strip()
            atom = atom.replace("\t", "")
            if len(atom) > 0:
                atoms.append(atom)
            else:
                pass
        return atoms
    
    with open("./target_urls.txt", "r") as file:
        target_urls = sanitize_lines(file.readlines())

    with open("./keywords.txt", "r") as file:
        keywords = sanitize_lines(file.readlines())

    # Output to a file by line.
    print(keywords)
    
    def write_list(file, atoms):
        file.write("\t".join([str(atom) for atom in atoms]) + "\n")

    with open("./out.txt", "w") as file:
        write_list(file, ["url"] + keywords)
        
    for target_url in target_urls:
        judges = list()
        for keyword in keywords:
            # Retry routine.
            for i in range(3):
                judge = judge_by_google_site_option(keyword, target_url)
                time.sleep(1)
                if judge != -1: break
            judges.append(judge)
        
        with open("./out.txt", "a") as file:
            write_list(file, [target_url] + judges)
    


scrape()

