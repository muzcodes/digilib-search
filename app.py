#Streamlit UI

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

# --- Search Execution and Results Display ---
# Only run the search if the user has entered a query.
if query:
    # Use a spinner to show that the search is in progress.
    with st.spinner('Searching through the library...'):
        # Call the search function from your core_logic.
        results = search(query)

    # Display the number of results found.
    st.success(f"Found {len(results)} relevant documents.")
    
    # Check if any results were returned.
    if results:
        # Loop through the results and display each one.
        for result in results:
            st.subheader(f"📄 {result['filename']}")
            st.write(f"**Relevance Score:** {result['score']:.4f}")
            # Add a divider for better readability between results.
            st.divider()
    else:
        # If no results are found, display a warning message.
        st.warning("No documents found matching your query. Please try different keywords.")