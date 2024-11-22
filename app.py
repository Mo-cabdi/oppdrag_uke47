import sqlite3

# Connect to the SQLite database
mydb = sqlite3.connect('proverbData.db')
cur = mydb.cursor()

matchedWordsCount = {}

def menu():
    print('-------------- Welcome to the Proverbs Search Engine --------------')
    print('!---- Where you learn or teach a new proverb every time. ----!')
    print('----- So what are you waiting for? -----')
    print('** CHOOSE **')
    print('1. Add a proverb.')
    print('2. Search for a proverb.')
    print('3. Exit.')

    user_input = input('Enter choice (1, 2, or 3): ').strip()

    if user_input == '1':
        return addProverb()
    elif user_input == '2':
        return searchProverb()
    elif user_input == '3':
        print("Thank you for using the Proverbs Search Engine. Goodbye!")
        cur.close()
        mydb.close()
        exit()
    else:
        print(
            '''
                Error!
                Please choose 1, 2, or 3.
            '''
        )
        return menu()

def addProverb():
    proverb = input('Proverb: ').strip()
    meaning = input('Meaning: ').strip()

    if proverb and meaning:
        try:
            cur.execute("INSERT OR IGNORE INTO proverbs (proverb, meaning) VALUES (?, ?)", (proverb, meaning))
            mydb.commit()
            print('---------- The new proverb was added! ----------')
            print('---- Thanks for the contribution ----\n')
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
    else:
        print('Proverb and meaning cannot be empty.\n')
        return addProverb()

    return menu()

def searchProverb():
    searching_input = input('''---- Enter the proverb or keywords you remember ----
''').strip().lower()

    if not searching_input:
        print("You didn't enter any words. Please try again.\n")
        return menu()

    search_words = searching_input.split()

    
    query = ("SELECT proverb, meaning FROM proverbs WHERE "
    + " OR ".join(["LOWER(proverb) LIKE ?"] * len(search_words)))
    parameters = [f"%{word}%" for word in search_words]

    try:
        #Retrieve all proverbs that have the searched words
        cur.execute(query, parameters)
        results = cur.fetchall()
        if results:
            print("\nMatched Proverbs:")
            for idx, (proverb, _) in enumerate(results, 1):
                splitProverbs = proverb.split()
                print(f"{idx}. {proverb}")
                searchWordsCounter(splitProverbs, search_words)
                
            print(f'this is how much your words was found! {matchedWordsCount}')
            while True:
                choice = input("\nEnter the number of the proverb to see its meaning (or press Enter to return to menu): ").strip()
                if choice == '':
                    return menu()
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= len(results):
                        selected_proverb, selected_meaning = results[choice - 1]
                        showMeaning(selected_proverb, selected_meaning)
                        return menu()
                    else:
                        print("Invalid number. Please try again.")
                else:
                    print("Invalid input. Please enter a number corresponding to the proverb.")
        else:
            print("\nNo proverbs matched your search.\n")
            return menu()
    except sqlite3.Error as e:
        print(f"An error occurred during the search: {e}")
        return menu()

def showMeaning(proverb, meaning):
    print(f"\nProverb: {proverb}")
    print(f"Meaning: {meaning}\n")

def searchWordsCounter(proverbs, userWords):
    for word in userWords:
        if word not in matchedWordsCount:
            matchedWordsCount[word] = {"count": 0}

        for x in proverbs:
            if x.lower().startswith(word.lower()):
                matchedWordsCount[word]["count"] += 1
        
 
    


def initialize_database():
    """Creates the proverbs table if it doesn't exist."""
    try:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS proverbs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                proverb TEXT UNIQUE NOT NULL,
                meaning TEXT NOT NULL
            )
        ''')
        mydb.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
        exit()

if __name__ == "__main__":
    initialize_database()
    menu()
