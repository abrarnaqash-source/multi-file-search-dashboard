import streamlit as st

st.set_page_config(page_title="Multi-File Search Dashboard", layout="wide")

st.title("📂 Multi-File Search Dashboard")
st.write("Upload multiple text files and search for a string across all of them.")

uploaded_files = st.file_uploader("Upload text files", type=["txt", "log", "csv"], accept_multiple_files=True)

search_term = st.text_input("Enter search term")
case_sensitive = st.checkbox("Case Sensitive Search", value=False)

if st.button("Search"):
    if not uploaded_files:
        st.warning("Please upload at least one file.")
    elif not search_term.strip():
        st.warning("Please enter a search term.")
    else:
        results = []
        for file in uploaded_files:
            content = file.read().decode("utf-8", errors="ignore")
            lines = content.split("\n")
            for i, line in enumerate(lines, start=1):
                if (case_sensitive and search_term in line) or \
                   (not case_sensitive and search_term.lower() in line.lower()):
                    results.append({
                        "file": file.name,
                        "line_number": i,
                        "line": line.strip()
                    })

        if results:
            st.success(f"Found {len(results)} matches across {len(uploaded_files)} files.")
            for match in results:
                st.markdown(f"**📄 File:** `{match['file']}` | **Line {match['line_number']}**\n> {match['line']}")
        else:
            st.error("No matches found.")
