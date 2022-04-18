# import the python csv library to access the csv tools
import csv
# import the webbrowser module to allow opening URLs in tabs
import webbrowser

# Set up all global variables to be used throughout.
# Empty string for the user inputted search request.
search_phrase = ""
# Empty list to house all keywords.
keyword_list = []
# Empty string to specify a content provider.
chosen_source = ""
# Empty list for source dictionaries.
content_providers = []
# Empty string which will become the query string (URL).
query_string = ""

"""
The 'event_handler_search_enter' function has one main goal...
Take in the user's search query and store as a global.

In the process, it converts the string to lowercase to 
ensure that the search query is in a workable format and 
to avoid having to deal with case sensitivity at other 
points in the solution.
"""


# Define the function.
def take_in_a_query():
    # Specify any globals to work on.
    global search_phrase

    # Find out what the user is looking for.
    # Convert all characters to lower case for
    # consistency and so that eventually the URL does not
    # contain mixed case.
    search_phrase = input(
        "What topic are you looking for? > ").lower()


"""
The following function 'remove_unwanted_punctuation' strips 
unwanted punctuation characters from the search query.

These characters are "!#$£%&'()+,./:;?@[\]^_`{|}~

The function then sets a list of keywords, removing any 
blank elements in the process.
"""


# Define the function.
def remove_unwanted_punctuation():
    # Specify any globals to work on.
    global search_phrase
    global keyword_list

    # I want the user to be able to enter Computer Science
    # relevant punctuation: -<=>+*
    # This punctuation I wish to keep will be excluded from
    # my 'unwanted_punctuation' string.
    unwanted_punctuation = "\"!#$£%&'()+,./:;?@[\]^_`{|}~"

    # Iterate through the 'unwanted_punctuation' string.
    for character in unwanted_punctuation:
        # Redefine the string to remove all punctuation
        # from the user query as the url cannot contain
        # punctuation.
        # Replace occurrences of any punctuation with "".
        search_phrase = search_phrase.replace(character, "")

    # Split the string into a list at every instance of a
    # single space (" ").
    # Fill the 'keyword_list' with whole words extracted
    # from 'search_phrase' string.
    keyword_list = search_phrase.split(" ")

    # Use my reusable function
    # 'remove_blank_elements_from_list' to remove any blank
    # elements left in the 'keyword_list'.
    keyword_list = remove_blank_elements_from_list(
        keyword_list)


"""
The following function 'remove_blank_elements_from_list' 
provides functionality needed in a number of places.

Its sole purpose is to strip any empty strings ("") from a 
given list.
"""


# Define the function.
def remove_blank_elements_from_list(list_name):
    # Remove any excess empty strings ("") left around in
    # the list sent in as an argument (list_name).
    # These may be due to the user typing multiple spaces or
    # due spaces left if punctuation was removed.
    try:
        # .remove() removes the first instance of a
        # specified parameter. Try to remove the first
        # instance of "" if there are any and keep on
        # while there are still instances.
        while True:
            list_name.remove("")
    # If this doesn't work because there are no "",
    # pass to the next part of the code.
    except ValueError:
        pass
    # Return the trimmed down list out of the function.
    return list_name


"""
The following function 'select_content_provider' allows 
users to select a content provider.

A default content provider is also established in this 
function.
"""


# Define the function.
def select_content_provider():
    # Specify any globals to work on.
    global chosen_source
    global content_providers
    global query_string

    # Open the structured CSV sources data file.
    sources = open("assets/sources.csv")

    # Use the csv library to:
    # 1) Read each line from the file
    # 2) Convert each row to its own dictionary
    # 3) Append the dictionary to the list
    for each_line_of_data in csv.DictReader(sources):
        # Add the dictionaries to the empty
        # content providers dictionaries list
        content_providers.append(each_line_of_data)

    # Set the source to Isaac CS by default.
    default_source = "Isaac CS"

    # Tell the user the default source.
    print("\nBy default,", default_source,
          "will be used as the default source for this "
          "session."
          "\nWould you prefer a different source?")

    # Check the 'sources.csv' data again to work out what
    # filter operator is expected for the given domain.
    # For example, Isaac Computer Science queries expect
    # the string '&types=' before filters are specified.
    for source in content_providers:
        if source.get("source name") == chosen_source:
            # Find out what the filter operator for the
            # source is and add it to the end of the query.
            query_string = query_string + source.get(
                "filter operator")

    # Provide a menu for the content provider options so
    # that the user can specify their choice.
    # Set up a counter to keep track of the menu options.
    counter = 1
    # Provide the option of no change.
    print("0) Keep default -", default_source)
    # Iterate through every dictionary which has now been
    # placed into the 'content_providers' list.
    for option in content_providers:
        # Present every source which isn't the default
        # source already mentioned.
        if option.get("source name") != default_source:
            # Provide a menu of content providers.
            # e.g. '1) Isaac Computer Science'
            print(counter, ') ', option.get("source name"),
                  sep='')
            # Add 1 to the counter for next time.
            counter += 1
        else:
            pass

    # Validation of the user's menu selection input is
    # needed.
    valid_menu_selection = False
    # Until the user provides a usable menu option...
    while not valid_menu_selection:
        # Which menu option does the user want?
        try:
            menu_number = int(input(
                "Enter the menu number of the content "
                "provider you wish to use: "))
            # Is the number within the range of the menu?
            if menu_number >= 1 and menu_number < counter + 1:
                # Update the global 'chosen_source' to be
                # the choice from the menu selection.
                chosen_source = content_providers[
                    menu_number - 1].get("source name")
                # The user's input is good.
                valid_menu_selection = True
            # If the user doesn't wish to change then go
            # with the default.
            elif menu_number == 0:
                chosen_source = default_source
                # The user's input is good
                valid_menu_selection = True
        except ValueError:
            pass


"""
The following function 'check_for_and_add_alternative_words' 
handles the looking up of synonyms, stemming words and 
acronyms of a given word.

It then adds any relevant alternative words of all 
keywords to the keyword list.
"""


# Define the function.
def check_for_and_add_alternative_words():
    # Specify any globals to work on.
    global keyword_list
    global content_providers  # ADDITION

    # Open the structured data file.
    lexical_database_contents = open(
        "assets/lexical_database.csv")

    # Create an empty list for lexical database.
    lexical_database = []

    # Set up a temporary list to store additional keywords.
    boosted_keyword_list = []

    # Consume each line as a discrete dictionary.

    # Use the csv library to:
    # 1) Read each line from the file
    # 2) Convert each row into its own dictionary
    # 3) Append the dictionary to the list

    for each_line_of_data in csv.DictReader(
            lexical_database_contents):
        # Add the dictionaries to the empty database list.
        lexical_database.append(each_line_of_data)

    # If any of the words in the line of data are found in
    # the search string, I want to include all the other
    # alternative words in the string.
    # e.g. ['decimal'] becomes
    # ['decimal', 'denary', 'base 10'], thus broadening the
    # search and making a search result more likely.

    # Iterate through every record in the lexical_database
    # in order to check against the individual keywords in
    # keywords_list.
    for record in lexical_database:
        # Extract all fields of the current record into
        # temporary variables (the value of which will
        # change with each iteration).
        # Put the 'word' field value in a string 'word'.
        word = record.get("word")

        # Put the 'stemming alternatives' field value in a
        # string 'stemming_alternatives'.
        stemming_alternatives = record.get(
            "stemming alternatives")

        # Records containing fields with multiple values
        # must be split into seperate values.
        # This is will only be from 'stemming alternatives'
        # or 'synonyms' fields because 'word' and
        # 'abbreviation' are single-value.

        # To split the 'stemming alternatives' field value
        # into multiple values where this is the case,
        # the '.split()' string method will achieve this
        # and place the multiple values in a list
        # 'stemming_word_split' as separate items.
        # Split the string where there's a pipe (|)
        stemming_words_split = stemming_alternatives.split(
            "|")

        # Put 'synonyms' field value in a string 'synonyms'.
        synonyms = record.get("synonyms")

        # To split the field value into multiple values
        # where this is the case, the '.split()' string
        # method will achieve this and place the multiple
        # values in list 'synonyms_split' as separate items.
        # Split the string where there's a pipe (|)
        synonyms_split = synonyms.split(
            "|")

        # Put the 'abbreviation' field value in a string
        # 'abbreviation'.
        abbreviation = record.get("abbreviation")

        # Define an empty list to populate with all the
        # individual alternative words as strings.
        alternatives_in_the_record = []

        # Split each word from the field value 'word' at
        # any spaces.
        word_list = word.split(" ")

        # Iterate through each word (now split into
        # individual strings) in word_list, appending to the
        # 'alternatives_in_the_record' list each time.
        for word in word_list:
            alternatives_in_the_record.append(word)

        # stemming_alternatives_split is a list so iterate
        # through each string item, splitting the same way.
        for stemming_string in stemming_words_split:
            # Split at spaces and put keywords into list.
            split_stemming_list = stemming_string.split(" ")

            # Iterate through every item in the split up
            # list and append to alternatives list.
            for stemming_item in split_stemming_list:
                alternatives_in_the_record.append(
                    stemming_item)

        # Do the same for 'synonyms_split'.
        for synonym_string in synonyms_split:
            split_synonym_list = synonym_string.split(
                " ")
            for synonym_item in split_synonym_list:
                alternatives_in_the_record.append(
                    synonym_item)

        # Lastly, populate the 'alternatives_in_the_record'
        # list with the abbreviation from the record.
        alternatives_in_the_record.append(abbreviation)

        # Now that all field values of the current record
        # are temporarily being stored in a list, check
        # each list item (word) against the words in the
        # user defined 'keyword_list'.

        # Iterate through the user defined 'keyword_list'
        for keyword in keyword_list:
            # Iterate through the list of alternative words
            # of the current record.
            for alternative in alternatives_in_the_record:
                # If the current keyword is the same as the
                # current alternative word...
                if keyword == alternative:
                    # Append the contents of the entire list
                    # of alternative words to the
                    # 'boosted_keyword_list'.
                    for item in alternatives_in_the_record:
                        boosted_keyword_list.append(item)
                    # The 'boosted_keyword_list' has now
                    # been boosted so break out of loop
                    # before any more instances of
                    # the alternatives to the current
                    # keyword are added.
                    break

    # However, all keywords should still be used in the
    # search string, so if a user defined keyword is not
    # included in the boosted list, then add it.
    # Append the keywords from the boosted_keyword_list
    # because they are significant.
    for word in keyword_list:
        # If the keyword doesn't appear at all in the
        # boosted list...
        if boosted_keyword_list.count(word) == 0:
            # Append the missing keyword to the boosted
            # list.
            boosted_keyword_list.append(word)

    # Tidy up any blank elements left in the list.
    boosted_keyword_list = remove_blank_elements_from_list(
        boosted_keyword_list)

    # Lastly, update the global 'keyword_list' with the
    # boosted list of keywords if it would improve the
    # result of the search of the chosen content provider.

    # Check to see if boosting is recommended for the chosen
    # content provider.

    # Does the user want to extend their search to increase
    # the chance of a result?
    # Assume that the search string of the content provider
    # should be boosted unless sources.csv says otherwise...
    boost = True
    # Iterate through each record of all the sources of
    # learning material.
    for record in content_providers:
        # Locate the record of the chosen content provider.
        if record.get("source name") == chosen_source:
            # Note that the source is best used when queries
            # are not boosted because the source handles
            # synonyms server-side.
            if record.get("auto boost") == "False":
                boost = False
            # But if boosted searches ARE recommended for
            # that content provider then don't do anything.
            else:
                pass

    # After ascertaining whether a boosted search SHOULD be
    # used for the content provider, give the user the
    # choice and recommendation.
    if boost:
        print("\nBoosting your search with synonyms is "
              "recommended for ", chosen_source, ".", sep="")
    else:
        print("\nBoosting your search with synonyms is not "
              "recommended for ", chosen_source, ", but "
              "you can boost your search if you wish.",
              sep="")

    # Display the options as a menu.
    print("0) Don't boost", "\n1) Boost my search!")

    # Validation of the user's menu selection input is
    # needed.
    valid_menu_selection = False
    # Until the user provides a usable menu option...
    while not valid_menu_selection:
        # Which menu option does the user want?
        try:
            menu_number = int(input(
                "Enter the menu number of your boosting "
                "preference: "))
            # Is the number within the range of the menu?
            if menu_number == 1:
                # Update the global 'keyword_list' to be
                # the boosted keywords.
                keyword_list = boosted_keyword_list
                # The user's input is good.
                valid_menu_selection = True
            # If the user doesn't wish to boost their
            # search then don't touch 'keyword_list'.
            elif menu_number == 0:
                pass
                # The user's input is good
                valid_menu_selection = True
        except ValueError:
            pass


"""
The following function 'remove_duplicate_list_elements' 
simply removes any duplicate items in a list.
"""


# Define the function.
def remove_duplicate_list_elements(list_name):
    # Check if any items in the list are duplicates.
    # For example, this will occur in the 'keyword_list'
    # if the user searches for 'cpu processor'.
    # The list will form as...
    # ['central', 'processing', 'unit', 'processor',
    # 'microprocessor', 'cpu', 'central', 'processing',
    # 'unit', 'processor', 'microprocessor', 'cpu']

    # Define an empty list to fill up with each word in the
    # original 'list_name' ONCE, the idea being that
    # duplicate words will be removed.
    unique_word_list = []

    # Iterate through each item in the list used as the
    # function's parameter (list_name).
    for item in list_name:
        # Use 'not in' to determine whether the item is not
        # in 'unique_word_list'.
        # If the outcome of this is 'True'...
        if item not in unique_word_list:
            # ...then add it to the 'unique_word_list'
            # because it is NOT a duplicated item.
            unique_word_list.append(item)

    # Redefine the list 'list_name' with the new cut down
    # list 'unique_word_list'.
    list_name = unique_word_list

    # Return the trimmed down list out of the function.
    return list_name


"""
The following function 'remove_stopwords' removes all 
defined stopwords from the keyword list.
"""


# Define the function.
def remove_stopwords():
    # Specify any globals to work on.
    global keyword_list

    # I am going to define my own stopwords instead of
    # taking them from any predefined libraries because I
    # know that there are certain standard stopwords
    # which I actually do not want to include in this.
    # e.g. 'and', 'or' and 'not'
    # (because these are Boolean operators), and
    # 'while', 'for', 'out', 'if', 'else', 'search'
    # (because these are associated with coding/algorithms).
    stopwords = ["a", "about", "am", "an", "as", "at",
                 "because", "before", "but", "by", "could",
                 "do", "from", "how", "i", "is", "in",
                 "interested", "into", "know", "like",
                 "me", "of", "off", "on", "onto", "per",
                 "please", "show", "since", "tell",
                 "than", "the", "their", "there", "they",
                 "this", "that", "to", "up", "via", "we",
                 "with", "would", "you"]

    # Iterate through all words in the defined 'stopwords'.
    for word in stopwords:
        # For each word in the stopwords list, try to remove
        # the word from the main 'keyword_list' whilst
        # it can find stopwords in it.
        try:
            while True:
                keyword_list.remove(word)
        # If this fails because there are no stopwords in
        # the keyword list, pass to the next bit of code.
        except ValueError:
            pass




"""
The following function 'form_query_string'
does a number of things to achieve a working URL.

It looks at the global 'chosen_source' and then:

    1. It adds the source domain to a new query string.
    2. It adds the source's specified search operator to the 
    same query string.
    3. It adds every keyword to the string, separated by an 
    OR separator (+).
"""


# Define the function.
def use_sources_to_form_query_string():
    # The query needs to be a fully qualified (working) URL.
    # The pattern needed for this is
    # [domain][operator][keywords separated by + signs]
    # In practice, this looks like
    # https://isaaccomputerscience.org/search?query=base+2
    # The + sign is an OR operator.

    # Specify any globals to work on.
    global chosen_source
    global query_string
    global keyword_list

    # For the last item in the keyword_list, a + isn't
    # needed, so set up a counter to keep track of position
    # in list.
    counter = 0
    # Iterate through each of the sources.
    for source in content_providers:
        # If the current dictionary is of the chosen source
        # (e.g. Isaac Computer Science)...
        if source.get("source name") == chosen_source:
            # Extract key information from the dictionary
            # and add to 'search_string'.

            # Add source domain to the search_string
            # (e.g. https://isaaccomputerscience.org).
            query_string = query_string + source.get(
                "source domain")
            # Add the source's operator to the search_string
            # (e.g. /search?query=)
            query_string = query_string + source.get(
                "operator")
            # Add the keywords to the search_string.
            for word in keyword_list:
                # Redefine the search_string with
                # current 'word'.
                query_string = query_string + word
                # For the last item in the keyword_list,
                # a + isn't needed, so by using a
                # counter, I can see if the current item
                # is the last of the keywords.

                # Add one to the counter.
                counter += 1

                # If it isn't the last item then add a +
                if counter != len(keyword_list):
                    # Redefine the search_string with a +
                    query_string = query_string + "+"


"""
The following function 'check_for_and_apply_content_filter'
checks to see whether the content provider allows for 
filtering and applies a filter if wanted.
"""


# Define the function.
def check_for_and_apply_content_filter():
    global chosen_source
    global content_providers
    global query_string

    # Isaac Computer Science and Bit by bit both provide
    # content type filters.
    # For Isaac Computer Science, these are:
    # concept, question, topic
    # For Bit by bit, a few of these are:
    # explainer, step-by-step tutorial, examination question

    # I have organised the data in a persistent database in
    # the form of a CSV file which looks like this...
    # source name,content type name,content type ID

    # Open the filters data file.
    filters = open("assets/filters.csv")

    # We need a simple database which contains dictionaries,
    # one for each content provider (e.g. Isaac CS) and
    # which details precisely how each of these providers
    # allows us to filter content into different 'types':
    # tutorial, question, etc so that we can use it to
    # look up values.
    content_filters = []

    # Use the csv library to:
    # 1) Read each line from the file
    # 2) Convert each row to its own dictionary
    # 3) Append the dictionary to the list
    for each_line_of_data in csv.DictReader(filters):
        content_filters.append(each_line_of_data)

    # Set up an empty list to be used as a database to
    # store all content type filters from the chosen source.
    filter_options = []

    # Run through the 'content_filters' database, extracting
    # those relevant to the chosen content provider,
    # building up the chosen content type filter options
    # as we go.
    for filter_type_pair in content_filters:
        # Is the current dictionary the source the user has
        # chosen to use? (e.g. Isaac CS)...
        if filter_type_pair.get(
                "source name") == chosen_source:
            # Place the record in the 'filter_options' list.
            filter_options.append(filter_type_pair)

    # Does the chosen content provider actually enable
    # content type filtering?
    if len(filter_options) > 0:
        # Does the user want to use filtering?
        # A menu is needed again to allow selection.
        print(
            "\nThe material provider allows for content type"
            " filtering."
            "\nWould you like to filter the search?")
        # Set up a counter to keep track of menu options.
        counter = 1
        # Provide the option of not using a filter.
        print("0) NO FILTERING")
        # Iterate through every dictionary which has now
        # been placed into the 'filter_options' list.
        for filter_option in filter_options:
            # Provide a menu of filters to select from.
            # e.g. '1) Examination'
            print(counter, ') ',
                  filter_option.get("content type name"),
                  sep='')
            # Add 1 to the counter for next time.
            counter += 1

        # Validate the user's input.
        valid_menu_selection = False
        # Until the user provides a usable menu option...
        while not valid_menu_selection:
            # Which menu option does the user want?
            try:
                menu_number = int(input(
                    "Enter the menu number of the filter "
                    "you wish to use: "))
                # Is the number within the range of the
                # menu's choices?
                if menu_number >= 1 and menu_number < counter:
                    # The user's input is good
                    valid_menu_selection = True
                    # Check the 'sources.csv' data again
                    # to work out what filter operator is
                    # expected for the given domain.
                    # For example, Isaac CS queries expect
                    # the string '&types='.
                    for source in content_providers:
                        if source.get(
                                "source name") == chosen_source:
                            # Find out what the filter
                            # operator for the source is and
                            # add it to the end of the query
                            query_string = query_string + source.get(
                                "filter operator")
                    # Use the chosen 'menu_number' to find
                    # the associated content type name.
                    query_string = query_string + \
                                   filter_options[
                                       menu_number - 1].get(
                                       "content type ID")
                # Or if the user doesn't wish to filter
                # after all, skip this part.
                elif menu_number == 0:
                    break
            except ValueError:
                pass


"""
The following function 'open_in_browser' opens the formed
query string in a new browser tab.
"""


# Define the function.
def open_in_browser():
    # Specify any globals to work on
    global query_string

    # Automatically open the URL in a browser
    webbrowser.open_new_tab(query_string)


# Define function 'main_menu' to hold the code for
# outputting menu options and receiving input for user menu
# option.
def main_menu():
    # Specify any globals to work on
    global search_phrase
    global keyword_list
    global chosen_source
    global content_providers
    global query_string

    # Set up a variable to store the user's choice of menu
    # item to run. e.g. "1" to run the main search code.
    choice = 0

    # Print the menu and ask for the user to select an
    # option until the user provides a valid menu choice.
    # If at any time the user wishes to quit, stop running
    # the code.
    while choice not in range(1, 3):
        retry = True
        while retry:

            # Reset all globals because each time the user
            # selects a different menu option, the global
            # variables such as query_string will be
            # added to each time.
            keyword_list = []
            search_phrase = ""
            chosen_source = ""
            content_providers = []
            query_string = ""

            # Print out the menu in a neat fashion, running
            # through the main options.
            print("\n========="
                  "\nMAIN MENU"
                  "\n========="
                  "\nSelect from the following options:"
                  "\n\n1. Search for GCSE Computer Science "
                  "material"
                  "\n2. Quit\n")

            try:
                # Which menu item does the user want?
                choice = int(input("Please enter the number"
                                   " of your option "
                                   "choice: "))

                # The user chose to search for GCSE Computer
                # Science material, so run all relevant
                # functions.
                if choice == 1:
                    take_in_a_query()
                    remove_unwanted_punctuation()
                    select_content_provider()
                    check_for_and_add_alternative_words()
                    keyword_list = remove_duplicate_list_elements(
                        keyword_list)
                    remove_stopwords()
                    use_sources_to_form_query_string()
                    check_for_and_apply_content_filter()
                    open_in_browser()

                # The user chose to quit so exit the program
                # after saying goodbye.
                elif choice == 2:
                    retry = False
                    quit("Thank you, goodbye.")

                else:
                    print("Your input isn't valid.")

            # The input cannot be cast to integer so the
            # user didn't enter a valid choice.
            except ValueError:
                print("Invalid menu option. "
                      "Your input is not a number.")


# Run the main code at start-up.
def main():
    # Find out what the user wants to do
    main_menu()


if __name__ == '__main__':
    main()
