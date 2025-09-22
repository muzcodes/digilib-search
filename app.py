#Streamlit UI
import os
import streamlit as st
# Import the search function from your backend logic.
from core import search

# --- Page Configuration ---
# Set the page title and a favicon for your app.
st.set_page_config(page_title="Scholarly Lib Search", page_icon="📚", layout="centered")

# --- Main User Interface ---

# Display a title and a short introduction.
st.title("📚 Scholarly Article Search Engine")
st.markdown("""
Welcome to your personal digital library search engine! 
This prototype uses a TF-IDF vectorizer to find relevant academic papers from your collection. 
Enter a query below to get started.
""")

# --- Search Bar ---
# Create a text input box for the user to enter their search query.
query = st.text_input(
    "Search for articles",
    placeholder="e.g., Brain Inspired Computing",
    help="Enter keywords related to the articles you want to find."
)

# Initialize results to an empty list
results = []

# --- Search Execution and Results Display ---
# Only run the search if the user has entered a query.
if query.strip():  # Ensure the query is not empty or just whitespace
    with st.spinner('Searching through the library...'):
        results = search(query)
    st.success(f"Found {len(results)} relevant documents.")
else:
    # Only show the warning if the user has interacted with the search bar
    if query != "":
        st.warning("Please enter a valid search query.")

# Check if any results were returned.
if results:
    for result in results:
        file_url = f"file://{os.path.abspath(result['path'])}"
        st.subheader(f"📄 {result['filename']}")
        st.write(f"**Relevance Score:** {result['score']:.4f}")
        
        try:
            with open(result['path'], "rb") as f:
                file_data = f.read()
            st.download_button(
                label="⬇️ Download",
                data=file_data,
                file_name=result['filename'],
                mime='application/pdf'
            )
        except FileNotFoundError:
            st.error(f"⚠️ File not found: {result['filename']}")
        except Exception as e:
            st.error(f"⚠️ An error occurred while accessing {result['filename']}: {e}")
        
        st.divider()
else:
    # Only show the warning if the user has interacted with the search bar
    if query.strip():
        st.warning("No documents found matching your query. Please try different keywords.")