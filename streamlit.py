import streamlit as st
import json
import os

# File path for storing the library
data_file = "library.json"

def load_library():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.error("Library file is corrupted. Resetting library...")
            save_library([])
    return []

def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file, indent=4)

def add_book(title, author, year, genre, read):
    library = load_library()
    if any(book["title"].lower() == title.lower() for book in library):
        st.warning("❌ This book title already exists.")
        return
    new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
    library.append(new_book)
    save_library(library)
    st.success(f"✅ Book '{title}' added successfully!")

def remove_book(title):
    library = load_library()
    updated_library = [book for book in library if book["title"].lower() != title.lower()]
    if len(updated_library) == len(library):
        st.warning("📕 Book not found.")
        return
    save_library(updated_library)
    st.success(f"📗 Book '{title}' removed successfully!")

def search_book(query, search_by):
    library = load_library()
    results = [book for book in library if query.lower() in book[search_by].lower()]
    return results

def display_books():
    library = load_library()
    if not library:
        st.info("📚 The library is currently empty. Add a book to get started.")
        return
    
    for book in library:
        read_status = "🟢 Read" if book["read"] else "🔴 Unread"
        st.markdown(f"**📖 {book['title']}** by {book['author']} ({book['year']})  ")
        st.caption(f"📚 Genre: {book['genre']} | {read_status}")
        st.divider()

def display_statistics():
    library = load_library()
    total_books = len(library)
    read_books = len([book for book in library if book["read"]])
    unread_books = total_books - read_books
    if total_books == 0:
        st.info("📚 No books available in the library.")
        return
    st.metric(label="Total Books", value=total_books)
    st.metric(label="Books Read", value=read_books)
    st.metric(label="Books Unread", value=unread_books)

# Streamlit UI
st.set_page_config(page_title="📚 Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

menu = st.sidebar.radio("📌 Menu", ["Add Book", "Remove Book", "Search Book", "View Books", "Statistics"])

if menu == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("📋 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Year of Publication", min_value=0, step=1)
    genre = st.text_input("📚 Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        if title and author and year and genre:
            add_book(title, author, year, genre, read)
        else:
            st.warning("❌ Please fill all fields.")

elif menu == "Remove Book":
    st.subheader("❌ Remove a Book")
    title = st.text_input("📋 Enter the book title to remove")
    if st.button("Remove Book"):
        remove_book(title)

elif menu == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_query = st.text_input("Enter title or author")
    search_type = st.radio("Search by", ("title", "author"))
    if st.button("Search"):
        results = search_book(search_query, search_type)
        if results:
            for book in results:
                read_status = "🟢 Read" if book["read"] else "🔴 Unread"
                st.markdown(f"**📖 {book['title']}** by {book['author']} ({book['year']})  ")
                st.caption(f"📚 Genre: {book['genre']} | {read_status}")
                st.divider()
        else:
            st.warning("No matching books found.")

elif menu == "View Books":
    st.subheader("📚 Library Collection")
    display_books()

elif menu == "Statistics":
    st.subheader("📊 Library Statistics")
    display_statistics()
