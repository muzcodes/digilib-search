# Scholarly Article Search Engine 📚

A prototype search engine built with Python and Streamlit to index and search a local collection of academic papers using TF-IDF and Cosine Similarity.

*This project was created for the "Digital Library and Content Management Techniques" course.*

***

## About The Project

This project is a practical application of information retrieval and content management principles. The goal was to build a simple but functional search engine that can ingest a corpus of PDF documents, process them into a searchable index, and provide a user-friendly web interface for querying.

**Key Features:**
* **PDF Text Extraction:** Automatically parses and extracts text content from PDF files.
* **TF-IDF Indexing:** Uses the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm to represent the textual data in a searchable vector space.
* **Relevance Ranking:** Ranks search results based on the Cosine Similarity between the user's query and the documents in the collection.
* **Interactive Web UI:** A clean and simple interface built with Streamlit for easy interaction.

***

## Tech Stack

This project was built using the following technologies:

* **Backend:** Python
* **NLP / Search:** Scikit-learn
* **PDF Parsing:** pdfplumber
* **Web Framework:** Streamlit

***

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

Make sure you have Python 3.8+ and pip installed on your system.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/muzcodes/digilib-search.git
    ```
2.  **Navigate to the project directory:**
    ```sh
    cd digilib-search
    ```
3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Add your data:**
    * Place all the PDF files you want to index into the `data/` folder.

5.  **Build the search index:**
    * Run the core logic script once to process your PDFs.
    ```sh
    python core.py
    ```
6.  **Run the Streamlit application:**
    ```sh
    streamlit run app.py
    ```
    Your browser should open with the application running!
