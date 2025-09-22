# core.py
import os
import pickle
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging


DATA_PATH = "data/"
INDEX_PATH = "saved_index/"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure the index directory exists.
os.makedirs(INDEX_PATH, exist_ok=True)

# Define the file paths for the saved index components.
VECTORIZER_PATH = os.path.join(INDEX_PATH, "vectorizer.pkl")
MATRIX_PATH = os.path.join(INDEX_PATH, "tfidf_matrix.pkl")
DOCUMENTS_PATH = os.path.join(INDEX_PATH, "documents.pkl")


def parse_pdfs(data_path):
    
    logging.info("🚀 Starting PDF parsing...")
    documents = []
    for filename in os.listdir(data_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_path, filename)
            try:
                with pdfplumber.open(file_path) as pdf:
                    full_text = ""
                    for page in pdf.pages:
                        # Extract text, handling None results from empty pages
                        page_text = page.extract_text()
                        if page_text:
                            full_text += page_text + "\n"

                    documents.append({"filename": filename, "text": full_text})
                    logging.info(f"  ✅ Parsed: {filename}")
            except Exception as e:
                logging.error(f"  ❌ Error parsing {filename}: {e}")

    logging.info(f"\n📚 Found and parsed {len(documents)} documents.")
    return documents


def build_and_save_index(documents):
    
    logging.info("\n🛠️ Building TF-IDF index...")

    # Extract the text content from the documents
    texts = [doc["text"] for doc in documents]

    # Initialize the TF-IDF Vectorizer.
    # stop_words='english' removes common English words.
    # ngram_range can capture multi-word phrases, improving search quality.
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=5000  # Limit vocabulary size to 5000 terms
    )

    # Create the TF-IDF matrix by fitting and transforming the text data.
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Save the necessary objects to disk using pickle.
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(MATRIX_PATH, "wb") as f:
        pickle.dump(tfidf_matrix, f)
    with open(DOCUMENTS_PATH, "wb") as f:
        pickle.dump(documents, f)

    logging.info("💾 Index built and saved successfully to the 'saved_index' folder.")


def search(query, top_n=10):
    
    # Check if the index files exist before trying to load them.
    if not all([os.path.exists(p) for p in [VECTORIZER_PATH, MATRIX_PATH, DOCUMENTS_PATH]]):
        logging.error("❌ Index not found. Please run the script to build the index.")
        return []

    # Load the saved vectorizer, matrix, and documents.
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    with open(MATRIX_PATH, "rb") as f:
        tfidf_matrix = pickle.load(f)
    with open(DOCUMENTS_PATH, "rb") as f:
        documents = pickle.load(f)

    # Transform the user's query into a TF-IDF vector.
    query_vector = vectorizer.transform([query])

    # Calculate the cosine similarity between the query and all documents.
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Get the indices of the top N most similar documents.
    # argsort() returns indices that would sort an array.
    # [::-1] reverses it to get descending order.
    top_doc_indices = similarity_scores.argsort()[::-1][:top_n]

    # Create a list of results.
    results = []
    for index in top_doc_indices:
        # Only add results with a similarity score greater than 0
        if similarity_scores[index] > 0:
            result = {
                "filename": documents[index]["filename"],
                "score": similarity_scores[index],
                "path": os.path.join(DATA_PATH, documents[index]["filename"]) # user needs the path to get the file
            }
            results.append(result)

    # Sort results by score (descending) and filename (ascending)
    results = sorted(results, key=lambda x: (-x['score'], x['filename']))

    return results


if __name__ == "__main__":
    logging.info("--- Starting Backend Engine Setup ---")

    # Step 1: Parse all PDFs in the data directory.
    docs = parse_pdfs(DATA_PATH)

    # Step 2: If documents were found, build and save the index.
    if docs:
        build_and_save_index(docs)
    else:
        logging.warning("\n⚠️ No documents found in the 'data' folder. The index was not built.")

    logging.info("\n--- Backend Engine Setup Complete ---")
    logging.info("You can now run the Streamlit app using: streamlit run app.py")