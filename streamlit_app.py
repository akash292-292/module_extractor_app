import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
import json

# Helper: Validate a URL
dict={}
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

# Helper: Normalize domain (no external links)
def get_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

# Step 1: Extract first-level links
def extract_first_level_links(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        for tag in soup.find_all('a', href=True):
            href = tag['href']
            full_url = urljoin(base_url, href)
            if get_domain(full_url) == get_domain(base_url):
                links.add(full_url.split('#')[0])
        
        return list(links)
    except Exception as e:
        return []

# Step 2: Extract structured content from a single page
def extract_module_structure(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract main heading as module name
        heading = soup.find(['h1', 'h2'])
        module_title = heading.get_text(strip=True) if heading else "Untitled Module"

        submodules = {}
        for tag in soup.find_all(['h3', 'h4', 'li']):
            title = tag.get_text(strip=True)
            if not title or len(title) < 5 or title in submodules:
                continue

            # Try to find a paragraph or sibling content for context
            description = ""
            next_elem = tag.find_next_sibling()
            while next_elem and next_elem.name not in ['h3', 'h4', 'li']:
                if next_elem.name in ['p', 'div', 'ul']:
                    text = next_elem.get_text(strip=True)
                    if text and len(text) > 20:
                        description = text
                        break
                next_elem = next_elem.find_next_sibling()

            if not description:
                description = f"Details about '{title}' as described on the page."

            submodules[title] = description

        return {
            "module": module_title,
            "Description": f"Includes information and tools related to {module_title.lower()}.",
            "Submodules": submodules
        }

    except Exception as e:
        return None


# Step 3: Build output structure from all first-level pages
def process_documentation(url):
    links = extract_first_level_links(url)
    modules = []

    for link in links:
        module = extract_module_structure(link)
        if module:
            modules.append(module)

    return modules

# Streamlit UI
st.set_page_config(page_title="Doc Websited Info Extractor", layout="wide")
st.title("📘Documentation Extractor")
st.markdown("Paste a help site homepage URL (like https://help.instagram.com/) to extract top-level module info.")

user_url = st.text_input("Enter Help Documentation URL")

if st.button("🚀 Extract Modules"):
    if not is_valid_url(user_url):
        st.error("Please enter a valid URL.")
    else:
        with st.spinner("Processing..."):
            #Check if the URL is already """PROCESSED OR NOT"""
            if user_url in dict:
                result= dict[user_url]
            else:   
                result = process_documentation(user_url)

        if not result:
            st.warning("No valid modules found or site could not be parsed.")
        else:
            st.success(f"Extracted {len(result)} modules.")
            json_output = json.dumps(result, indent=2)

            # Show structured results
            
            for module in result:
                with st.expander(f"📂 {module['module']}"):
                    st.markdown(f"**Description:** {module['Description']}")
                    for sub, desc in module['Submodules'].items():
                        st.markdown(f"- 🔹 **{sub}**: {desc}")

            st.download_button("📥 Download JSON", json_output, file_name="modules_output.json", mime="application/json")
