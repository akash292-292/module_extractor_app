📘 Website Content Extractor

This Streamlit-based app extracts top-level **modules** and **submodules** from a help/documentation website by crawling the homepage and parsing internal links.

---

🚀 Features

- Input a single documentation homepage URL.
- Crawls only first-level internal links.
- Extracts module title (`h1/h2`) and submodules (`h3/h4/li`) with brief descriptions.
- Displays results in expandable sections.
- Option to download as JSON.

---

🛠️ Setup Instructions

1. Clone the repo
2. Install the requirements (pip install requirements.txt)
3. Run the Command to start the app(streamlit run streamlit_app.py)
4. Insert the URL
5. After the success notofication scroll down to see the download json button
