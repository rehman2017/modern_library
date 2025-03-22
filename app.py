import json
import os


# Name of library
library_file = os.path.join(os.path.dirname(__file__), "library.txt")


def load_library():
    # Open File is Exist
    if os.path.exists(library_file):
        with open(library_file, "r") as file:
            # Read File and Delete Extra
            data = file.read().strip()
            # if Blank
            if not data:
                return []
            # If Find Load Data
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                print(
                    f"❌ Error: {library_file} is corrupted. Resetting library...")
                # Save new Blank library if Finds Corrupted
                save_library([])
                return []
    return []


def save_library(library):
    try:
        # Open File and Add Data
        with open(library_file, "w") as file:
            json.dump(library, file, indent=4)
    except Exception as e:
        # If Error While Saving
        print(f"❌ Error saving library: {e}")


def add_book(library):
    # Add New Book Data Step by Step
    # Add Title
    while True:
        title: str = input("📋 Enter the book title: ").strip()
        # if Blank ask Again Input
        if not title:
            print("❌ Title cannot be blank. Please enter the book title again.")
            continue
        # Check if Title is already taken
        is_duplicate = False
        for book in library:
            if book["title"].lower() == title.lower():
                is_duplicate = True
                break
        # if Duplicate ask Again Input
        if is_duplicate:
            print("❌ Book Title is already taken. Please enter a different title.")
            continue
        break
    # Add Author Name
    while True:
        author: str = input("✍️ Enter the author: ").strip()
        if author:
            break
        print(f"❌ Author cannot be blank. Please enter the author name again.")
    # Add Year of Publish
    while True:
        try:
            year: int = int(input("📅 Enter the publication year: "))
            if year > 0:
                break
            else:
                print("⚠️ Please enter a valid year (e.g., 2025).")
        except ValueError:
            print("⚠️ Please enter a valid year (e.g., 2025).")
    # Add Genre
    while True:
        genre: str = input("📚 Enter the genre: ").strip()
        if genre:
            break
        print(f"❌ Genre cannot be blank. Please enter the genre again.")
    # Add Read or Unread
    read: str = input("🧐📖 Have you read this book? (yes/no): ").strip().lower()
    # Convert True or False
    read: bool = True if read in ["yes", "y"] else False
    # Add Received Data into Dict
    new_book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read,
    }
    # Append and Call Save Function
    library.append(new_book)
    save_library(library)
    # Added Successfully info for User
    print(f"Book \"{title}\" added successfully.")


def remove_book(library):
    # if Library is Empty
    if not library:
        print("📚 The library is currently empty. Add a book to get started.")
        return
    # Enter Title for Removing Book
    while True:
        remove_file = input(
            "📋 Enter the title of the book to remove: ").strip().lower()
        if remove_file:
            break
        print("❌ Title cannot be blank. Please enter the book title again.")
    # Check Initial Length
    initial_length = len(library)
    # Store in a new Variable
    updated_library = [book for book in library if book["title"].lower() !=
                       remove_file]
    # Show Success Message If Removed any Book
    if len(updated_library) < initial_length:
        # Save Updated Data in the Save Function
        save_library(updated_library)
        print(f"📗 Book \"{remove_file}\" removed successfully.")
        return updated_library
    # Show Success Message Book not Found
    else:
        print(f"📕 Book \"{remove_file}\" not found in the library.")


def search_book(library):
    # if Library is Empty
    if not library:
        print("📚 The library is currently empty. Add a book to get started.")
        return
    # Select Title or Author For Searching
    while True:
        print("Search by: \n1. Title  \n2. Author")
        search_type = input("Enter your choice: ").strip()
        if search_type in ["1", "title"]:
            search_type = "title"
            break
        elif search_type in ["2", "author"]:
            search_type = "author"
            break
        else:
            print("Invalid choice.")
    # Enter Data for Searching
    while True:
        search_query = input(
            f"Enter the \"{search_type}\" name: ").strip().lower()
        if search_query:
            break
        print(
            f"❌ {search_type.capitalize()} cannot be blank. Please enter the book {search_type} again.")
    # Show Result if Found
    result = [book for book in library if search_query in book[search_type].lower()]
    if result:
        print("Matching Books: ")
        for index, book in enumerate(result, start=1):
            if book['read']:
                read = "🟢 Read"
            else:
                read = "🔴 Unread"
            print(
                f"{index}. 📒 \"{book['title']}\" by ✍️  {book['author']}, 📅 ({book['year']}) - 🧐 {book['genre']} - {read}")
    # Show Not Found Message
    else:
        print(f"No books found for '{search_query}' in {search_type}.")


def display_book(library):
    # if Library is Empty
    if not library:
        print("📚 The library is currently empty. Add a book to get started.")
        return
    # Show Book if in the library
    print("\n📚 Library Books:")
    for index, book in enumerate(library, start=1):
        if book['read']:
            read = "🟢 Read"
        else:
            read = "🔴 Unread"
        print(
            f"{index}. 📒 \"{book['title']}\" by ✍️  {book['author']}, 📅 ({book['year']}) - 🧐 {book['genre']} - {read}")


def display_statistics(library):
    # if Library is Empty
    if not library:
        print("📚 The library is currently empty. Add a book to get started.")
        return
    # Total Length of Books in Library
    total_books = len(library)
    # Check if Read Books Available
    read_books = len([book for book in library if book['read']])
    # Calculated Percentage of Read Books
    percentage_read = (read_books / total_books) * \
        100 if total_books > 0 else 0
    # Show Data % and Read Books
    print(f"\n📚 Total books: {total_books}")
    print(f"📖 Books read: {read_books}")
    print(f"📊 Percentage read: {percentage_read:.2f}%")


def main():
    # Main Functions
    library = load_library()
    # Welcome Message and Choice Options
    print("👋 𝐖𝐄𝐋𝐂𝐎𝐌𝐄 to your Personal Library Manager!")
    menu = """
    1. ➕ Add a book  
    2. ❌ Remove a book  
    3. 🔍 Search for a book  
    4. 📺 Display all books  
    5. 📊 Display statistics  
    6. ⛔ Exit  
    """
    # Select Page to view or exit from program
    while True:
        print(menu)
        choice = input("🚀 Enter your choice: ")
        if choice == "1":
            add_book(library)
        elif choice == "2":
            # Update Data if Removed
            library = remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_book(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            print("👋😊 very glad to use my LIBRARY!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()