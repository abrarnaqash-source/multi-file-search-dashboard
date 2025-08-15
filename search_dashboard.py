import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="📂 Multi-File Search Dashboard", layout="wide")

st.title("📂 Multi-File Search Dashboard")
st.write("Upload multiple text files, preview them, and search for keywords with highlighted results.")

# ✅ File uploader (this was missing in the broken version)
uploaded_files = st.file_uploader(
    "Upload text files", 
    type=["txt", "log", "csv"], 
    accept_multiple_files=True
)

# Display file previews in tabs
if uploaded_files:
    tabs = st.tabs([f"📄 {file.name}" for file in uploaded_files])
    for tab, file in zip(tabs, uploaded_files):
        with tab:
            content = file.read().decode("utf-8", errors="ignore")
            st.text_area("File Content", content, height=200)
            file.seek(0)  # Reset pointer for later reading

# Search input
search_term = st.text_input("Enter search term")
case_sensitive = st.checkbox("Case Sensitive Search", value=False)

# Search button
if st.button("Search"):
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    elif not search_term.strip():
        st.warning("Please enter a search term.")
    else:
        results = []
        total_matches = 0

        for file in uploaded_files:
            content = file.read().decode("utf-8", errors="ignore")
            lines = content.split("\n")
            matches = []
            for i, line in enumerate(lines, start=1):
                if (case_sensitive and search_term in line) or \
                   (not case_sensitive and search_term.lower() in line.lower()):
                    highlighted_line = re.sub(
                        f"({search_term})",
                        r"<mark style='background-color: yellow'>\1</mark>",
                        line,
                        flags=0 if case_sensitive else re.IGNORECASE
                    )
                    matches.append((i, highlighted_line))
            if matches:
                results.append({"file": file.name, "matches": matches})
                total_matches += len(matches)
            file.seek(0)

        if results:
            # ✅ Summary Counter
            col1, col2, col3 = st.columns(3)
            col1.metric("📂 Files Searched", len(uploaded_files))
            col2.metric("📄 Files with Matches", len(results))
            col3.metric("🔍 Total Matches Found", total_matches)

            st.success(f"Found {total_matches} matches across {len(results)} files.")

            # Display grouped results
            for res in results:
                with st.expander(f"📄 {res['file']} — {len(res['matches'])} matches"):
                    for line_num, line in res['matches']:
                        st.markdown(f"**Line {line_num}:** {line}", unsafe_allow_html=True)

            # Prepare CSV for download
            csv_data = []
            for res in results:
                for line_num, line in res['matches']:
                    csv_data.append([res['file'], line_num, re.sub('<.*?>', '', line)])
            df = pd.DataFrame(csv_data, columns=["File", "Line Number", "Matched Line"])
            st.download_button("📥 Download Results as CSV", df.to_csv(index=False), "search_results.csv", "text/csv")

        else:
            st.error("No matches found.")
