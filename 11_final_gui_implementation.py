# import the wx library to access GUI tools.
import wx
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
# Empty string to specify a content type filter.
chosen_content_filter = ""
# Empty list for content type filter dictionaries.
content_filters = []
# Set the boosting of keyword search to 'True' to begin.
boost = True
# Empty string which will become the query string (URL).
query_string = ""


# Define the function.
def remove_blank_elements_from_list(list_name):
    """
    The following function 'remove_blank_elements_from_list'
    provides functionality needed in a number of places.

    Its sole purpose is to strip any empty strings ("") from
    a given list.
    """
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


# Define the function.
def remove_duplicate_list_elements(list_name):
    """
    The following function 'remove_duplicate_list_elements'
    simply removes any duplicate items in a list.
    """
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


# Define the function.
def remove_unwanted_punctuation():
    """
    The following function 'remove_unwanted_punctuation'
    strips unwanted punctuation characters from the search
    query.

    These characters are "!#$£%&'()+,./:;?@[\]^_`{|}~

    The function then sets a list of keywords, removing any
    blank elements in the process.
    """
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


# Define the function.
def remove_stopwords():
    """
    The following function 'remove_stopwords' removes all
    defined stopwords from the keyword list.
    """
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


# Define the function.
def check_for_and_add_alternative_words():
    """
    The following function 'check_for_and_add_alternative_words'
    handles the looking up of synonyms, stemming words and
    acronyms of a given word.

    It then adds any relevant alternative words of all
    keywords to the keyword list.
    """
    # Specify any globals to work on.
    global keyword_list
    global content_providers

    # Open the structured data file.
    lexical_database_contents = open(
        "./assets/lexical_database.csv")

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
        # must be split into separate values.
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

    # Tidy up any blank elements left in the list and update
    # keyword list.
    # Remove duplicate items
    boosted_keyword_list = remove_duplicate_list_elements(boosted_keyword_list)
    # Remove blank elements
    boosted_keyword_list = remove_blank_elements_from_list(
        boosted_keyword_list)
    # Update the global 'keyword_list'
    keyword_list = boosted_keyword_list


def form_query_string():
    """
    This function ties together all of the pieces needed
    to form a fully qualified (working) URL.
        1. It adds the source domain to a new query string.
        2. It adds the source's specified search operator to
        the same query string.
        3. It adds every keyword to the string, separated
        by an OR separator (+).
    """
    # The pattern needed for this is
    # [domain][operator][keywords separated by + signs]
    # In practice, this looks like
    # https://isaaccomputerscience.org/search?query=base+2
    # The + sign is an OR operator.

    # Specify any globals to work on.
    global chosen_source
    global query_string
    global keyword_list
    global content_providers
    global chosen_content_filter

    # Firstly, clear out the 'query_string' to start afresh
    query_string = ""

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
    The next section checks to see whether the content 
    provider allows for filtering and applies a filter 
    if wanted.
    """
    # Check the 'sources.csv' data again
    # to work out what filter operator is
    # expected for the given domain.
    # For example, Isaac CS queries expect
    # the string '&types='.
    if chosen_content_filter != "Any":
        for source in content_providers:
            if source.get(
                    "source name") == chosen_source:
                # Find out what the filter
                # operator for the source is and
                # add it to the end of the query
                query_string = query_string + source.get(
                    "filter operator")
                # Use the chosen content type name.
                query_string = query_string + chosen_content_filter
                # Now it's added to the string, pass
                pass
    # However, if the filter is set to "Any" then skip this
    else:
        pass


def main():
    """
    This program runs functions when certain elements of
    the UI are interacted with.
    For example, if the user types in a query and presses a
    search button, then a series of query string building
    functions will be run and the user will be returned a
    result in a browser window.

    To keep things easy to read, all layout related items
    are defined in 'main()' and the actions (events) to
    occur when these items are interacted with are written
    outside of 'main()' and in separate functions.
    """
    # Specify any globals to work on
    global boost

    # Create an instance of an App() object called 'app'.
    app = wx.App()
    # Create an instance of a Frame() object with minimum
    # reasonable constructor arguments in place.
    # Arguments:
    #   parent: None (no parent), This argument's mandatory.
    #   title: Make it clear that the second argument is
    #   intended to be the title parameter.
    #   This argument is optional.
    #   style: Specified attributes are 'wx.CAPTION' to
    #   produce a top bar, 'wx.SYSTEM_MENU' to allow for a
    #   system menu
    #          to be placed, and 'wx.CLOSE_BOX' to place a
    #          close button in the frame. This argument is
    #          optional.
    #   size: Fix the window at a size which will fit on
    #   all devices (1000 x 800px).
    frame = wx.Frame(None,
                     title="GCSE Computer Science learning portal",
                     style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER,
                     size=(1000, 800))
    # Make an icon for the top left of the window out of the
    # png provided
    icon = wx.Icon()
    icon.CopyFromBitmap(wx.Bitmap("./assets/application_icon.png",
                                  wx.BITMAP_TYPE_ANY))
    frame.SetIcon(icon)
    # Create a status bar to the frame.
    status_bar = frame.CreateStatusBar()
    # Use the status bar.
    frame.SetStatusBar(status_bar)
    # Define the absolute smallest size the window can be.
    frame.SetMinSize((1000, 800))
    # Centre the frame
    frame.Center()
    # Create a standard menu bar object.
    menu_bar = wx.MenuBar()
    # Create a standard menu for the Help menu.
    main_menu = wx.Menu()
    # The 1st argument identifies the behaviour of this item
    # as an exit choice.
    # The 2nd argument dictates the menu entry title
    # displayed.
    # The 3rd is the tooltip which shows in the status line
    # if you have a status bar displayed.
    main_menu_item_about = main_menu.Append(wx.ID_ABOUT,
                                            "&About",
                                            "What's it all about?")
    main_menu_item_quit = main_menu.Append(wx.ID_EXIT,
                                           "&Exit",
                                           "Exit the learning portal.")

    def event_handler_about_app_clicked(event):
        # Creating a pop-up window with a message, message
        # caption and a specified button and icon
        # Use an "i" icon
        wx.MessageBox("Evie's GCSE Computer Science helper!"
                      "\n\nUse this application to help you"
                      " find the GCSE Computer Science "
                      "learning material "
                      "that you're REALLY after."
                      "\n\nI have curated a list of content"
                      " providers which have worked well for"
                      " me in the past."
                      "\n\nHave fun, Evie.", "About",
                      wx.OK | wx.ICON_INFORMATION)
        main_panel.Show()

    # Define an event handler function to dictate what
    # should happen when the user clicks on the 'quit'
    # button.
    def event_handler_quit_app_clicked(event):
        # Hide the app.
        main_panel.Hide()
        # Stop the program.
        exit()

    # Add that Help menu to the menu bar.
    menu_bar.Append(main_menu, "&Menu")
    # Attach listeners to the menu items.
    # When the main menu dispatches a wx.EVT_MENU event,
    # if it was the item 'Get outta here!', then call the
    # simple function called 'event_handler_quit_app_clicked'.
    main_menu.Bind(wx.EVT_MENU, event_handler_quit_app_clicked,
                   main_menu_item_quit)
    # When the main menu dispatches a wx.EVT_MENU event, if
    # it was the item 'What's it all about?', then call the
    # simple function called 'event_handler_about_app_clicked'.
    main_menu.Bind(wx.EVT_MENU, event_handler_about_app_clicked,
                   main_menu_item_about)
    # Use the menu bar
    frame.SetMenuBar(menu_bar)

    # ****LAYOUT****

    # LEVEL 1 panel layout...
    # Add a main panel to the frame.
    main_panel = wx.Panel(frame)
    # Create a box sizer in which to place the sub panel.
    main_panel_sizer = wx.BoxSizer()
    # Add this to the main panel.
    main_panel.SetSizer(main_panel_sizer)

    # LEVEL 2 panel layout...
    # Add a sub panel to the main panel.
    sub_panel = wx.Panel(main_panel)
    # Create a vertical box sizer in which to place the panels.
    sub_panel_sizer = wx.BoxSizer(wx.VERTICAL)
    # Apply the sizer to the frame.
    sub_panel.SetSizer(sub_panel_sizer)
    # Place the sub panel in the layout with a border and
    # expanded to fit.
    main_panel_sizer.Add(sub_panel, proportion=1,
                         flag=wx.EXPAND | wx.ALL, border=16)

    # LEVEL 3 panel layout...
    # The sub panel is going to contain three panels in
    # which to place widgets:

    # The first panel, 'query_panel', is going to contain
    # the search query box in which the user will enter
    # their query and a line of text will be placed in this
    # panel to explain to the user what to do.

    # The second panel, 'content_provider_panel', is going
    # to contain a line of text to ask the user to select a
    # source and the panel will contain radio buttons to
    # select a single content provider source.

    # The third panel 'boost_panel', is going to contain a
    # description about what 'boosting' a keyword search
    # means, and it is going to contain a checkbox button
    # for the user to select whether they do or don't wish
    # to boost their search.

    # The fourth panel, 'content_type_filter_panel', is going
    # to contain a line of text to ask the user whether they
    # wish to filter and the panel will contain each of the
    # filters that the content provider allows for.
    # For each filter, there will also be a description of
    # what the type of content is
    # (e.g. Interactive challenge = an online quiz).

    # Add a panel to the sub panel for the query box widget
    # and description.
    query_panel = wx.Panel(sub_panel)
    # Create a new vertical sizer to manage the component
    # layout in the query panel.
    query_panel_sizer = wx.BoxSizer(wx.VERTICAL)
    # Apply this to the query panel.
    query_panel.SetSizer(query_panel_sizer)
    # Place the query panel in the sub panel layout with a
    # border at the top and expanded to fit.
    sub_panel_sizer.Add(query_panel, proportion=0,
                        flag=wx.EXPAND | wx.TOP, border=16)

    # Add a panel to the sub panel for the content provider
    # selection and description.
    content_provider_panel = wx.Panel(sub_panel)
    # Create a new vertical sizer to manage the component
    # layout in the panel.
    content_provider_panel_sizer = wx.BoxSizer(wx.VERTICAL)
    # Apply this to the content provider panel.
    content_provider_panel.SetSizer(
        content_provider_panel_sizer)
    # Place the content provider panel in the sub panel
    # layout with a border at the top and expanded to fit.
    sub_panel_sizer.Add(content_provider_panel,
                        proportion=0, flag=wx.TOP,
                        border=16)

    # Add a panel to the sub panel for the boost my search
    # checkbox button and description.
    boost_panel = wx.Panel(sub_panel)
    # Create a new vertical sizer to manage the component
    # layout in the query panel.
    boost_panel_sizer = wx.BoxSizer(wx.VERTICAL)
    # Apply this to the boost panel.
    boost_panel.SetSizer(boost_panel_sizer)
    # Place the boost panel in the sub panel layout with a
    # border at the top and expanded to fit.
    sub_panel_sizer.Add(boost_panel, proportion=0,
                        flag=wx.EXPAND | wx.TOP, border=16)

    # Add a panel to the sub panel for the content
    # provider's filtering options and descriptions.
    content_type_filter_panel = wx.Panel(sub_panel)
    # Create a vertical sizer to manage the component layout
    # in the panel.
    content_type_filter_panel_sizer = wx.BoxSizer(
        wx.VERTICAL)
    # Apply this to the filter panel.
    content_type_filter_panel.SetSizer(
        content_type_filter_panel_sizer)
    # Place the filter panel in the sub panel layout with a
    # border at the top and expanded to fit.
    sub_panel_sizer.Add(content_type_filter_panel,
                        proportion=1, flag=wx.TOP,
                        border=16)

    # LEVEL 4 panel layout...

    # Inside of the LEVEL 3 'content_provider_panel', will
    # be two more panels: 'content_provider_header_panel'
    # and 'content_provider_sources_panel'.
    # The sources panel will house radio buttons which need
    # to be placed in a grid format in order to allow for
    # any number of sources to fit into the window
    # regardless of size.
    # Without proper grided layout, if 10 more content
    # providers were added to the system for example,
    # the radio button text would extend out of the frame
    # and would not be usable.

    # Add a panel to the content provider panel for
    # placement of a description.
    content_provider_header_panel = wx.Panel(
        content_provider_panel)
    # Create a vertical sizer to manage the component layout
    # in the header panel.
    content_provider_header_panel_sizer = wx.BoxSizer(
        wx.VERTICAL)
    # Apply this to the content provider header panel.
    content_provider_header_panel.SetSizer(
        content_provider_header_panel_sizer)
    # Place the content provider header panel in the content
    # provider panel layout, expanded to fit.
    content_provider_panel_sizer.Add(
        content_provider_header_panel, proportion=0,
        flag=wx.EXPAND)
    # Add a panel to the content provider panel for
    # placement of radio buttons for source choices.
    content_provider_sources_panel = wx.Panel(
        content_provider_panel)
    # Create a new grid sizer with 3 columns to manage the
    # component layout in the sources panel.
    content_provider_sources_panel_sizer = wx.GridSizer(3)
    # Apply this to the content provider sources panel.
    content_provider_sources_panel.SetSizer(
        content_provider_sources_panel_sizer)
    # Place the content provider sources panel in the
    # content provider panel layout, expanded to fit.
    content_provider_panel_sizer.Add(
        content_provider_sources_panel, proportion=0,
        flag=wx.EXPAND)

    # Level 4 of BOOST panel...
    # Add a panel to the boost panel for
    # placement of a description.
    boost_header_panel = wx.Panel(
        boost_panel)
    # Create a vertical sizer to manage the component layout
    # in the header panel.
    boost_header_panel_sizer = wx.BoxSizer(
        wx.VERTICAL)
    # Apply this to the boost header panel.
    boost_header_panel.SetSizer(
        boost_header_panel_sizer)
    # Place the boost header panel in the boost panel
    # layout, expanded to fit.
    boost_panel_sizer.Add(
        boost_header_panel, proportion=0,
        flag=wx.EXPAND)
    # Add a panel to the boost panel for
    # placement of a single checkbox button.
    boost_checkbox_button_panel = wx.Panel(
        boost_panel)
    # Create a vertical sizer to manage the component layout
    # in the boost checkbox button panel.
    boost_checkbox_button_panel_sizer = wx.BoxSizer(
        wx.VERTICAL)
    # Apply this to the boost checkbox button panel.
    boost_checkbox_button_panel.SetSizer(
        boost_checkbox_button_panel_sizer)
    # Place the checkbox button panel in the
    # boost panel layout, expanded to fit.
    boost_panel_sizer.Add(
        boost_checkbox_button_panel, proportion=0,
        flag=wx.EXPAND)

    # ****CONTENTS****

    # QUERY PANEL contents...
    # Create a label for the search box in the query panel.
    search_label = wx.StaticText(query_panel,
                                 label="What are you looking for?")
    # Add the search label component to the query panel
    # sizer but with just the default fixed width.
    query_panel_sizer.Add(search_label, proportion=0,
                          flag=wx.ALL, border=8)
    # Create a search box in the query panel.
    search_box = wx.SearchCtrl(query_panel)
    # Add some placeholder text to the search box.
    search_box.SetDescriptiveText(
        "This is an OR search, I will use ANY of the keywords you type.")
    # Add the search box component to the query panel sizer,
    # expanded horizontally to fill the available space.
    query_panel_sizer.Add(search_box, proportion=0,
                          flag=wx.EXPAND | wx.ALL, border=8)

    # Define the event handling function.
    def event_handler_search_enter(event):
        """
        The 'event_handler_search_enter' function is an event
        handler which takes in the user's search query and
        stores it as a global.
        In the process, it converts the string to lowercase to
        ensure that the search query is in a workable format and
        to avoid having to deal with case sensitivity at other
        points in the solution.
        """
        # Specify any globals to work on.
        global search_phrase
        global query_string
        global boost

        # Find out what the user is looking for.
        # Convert all characters to lower case for
        # consistency and so that eventually the URL does
        # not contain mixed case.
        search_phrase = event.GetString()
        # Change the case to lower.
        search_phrase = search_phrase.lower()
        # Run the function 'remove_unwanted_punctuation()'
        remove_unwanted_punctuation()
        # Run the function 'remove_stopwords()'
        remove_stopwords()
        # Check the state of 'boost' to see whether or not
        # to add alternative words to the query
        if boost == True:
            # Run the functions needed to add the extra
            # keywords and tidy up the list ready for the
            # formation of the query string.
            check_for_and_add_alternative_words()
            pass
        else:
            # There is nothing more to do for now to the
            # keyword search
            pass
        # Run the function to get a working URL.
        form_query_string()
        print(query_string)
        # Automatically open the URL in a browser
        webbrowser.open_new_tab(query_string)

    # When text is entered into the search box and the user
    # clicks on the search button or presses the ENTER key,
    # the text they enter needs to be stored as the global
    # 'search_phrase'.
    # Bind the event (clicking search or ENTER key) and the
    # function 'event_handler_search_enter()' to search box.
    search_box.Bind(wx.EVT_SEARCH,
                    event_handler_search_enter)

    # CONTENT PROVIDER PANEL contents...
    # For the content provider HEADER (level 4) panel...
    # Create a header to describe what is required of user.
    content_provider_header = wx.StaticText(
        content_provider_header_panel,
        label="Choose one of the recommended educators")
    # Add the text component to the content provider panel
    # sizer.
    content_provider_header_panel_sizer.Add(
        content_provider_header, proportion=0, flag=wx.ALL,
        border=8)

    # For the content provider SOURCES (level 4) panel...
    # Define the event handling function.
    def event_handler_sources_radio_button_click(event):
        """
        This function responds to any source radio button
        click and it ascertains which source was clicked and
        sets the 'chosen_source' variable.
        """
        # Specify any globals to work on.
        global chosen_source
        global chosen_content_filter
        global content_providers
        global boost

        # Clear out the 'chosen_content_filter' to allow for
        # reselection if the user changes their mind about
        # which content provider to use.
        chosen_content_filter = ""
        # Find out which source radio button was clicked and
        # get the label.
        # Set this label as the chosen source.
        chosen_source = event.GetEventObject().GetLabel()
        build_filter_options_panel()
        # Additionally, the state of 'boost' needs to change
        # now based on the recommendations for this content
        # provider.
        # Iterate through each record of all the sources of
        # learning material.
        for record in content_providers:
            # Locate the record of the chosen content provider.
            if record.get("source name") == chosen_source:
                # The source might be best used when queries
                # are not boosted because the source handles
                # synonyms server-side.
                # If this is the case...
                if record.get("auto boost") == "False":
                    boost = False
                    # There's nothing more to do, so break
                    # out of the loop.
                    break
                # But if boosted searches ARE recommended for
                # that content provider then don't do anything.
                else:
                    boost = True
                    # There's nothing more to do, so break
                    # out of the loop.
                    break
        # Now run the function to redraw the 'boost_panel'
        # with the desired state of True or False, as set
        # out in the code above.
        build_boost_panel()
        # Force redraw the sub panel to refresh the children
        sub_panel.Layout()

    # Create radio buttons for the content provider sources.
    # Access the global 'content_providers' list.
    global content_providers
    global chosen_source
    # Open the structured CSV sources data file.
    sources = open("./assets/sources.csv")

    # Use the csv library to:
    # 1) Read each line from the file
    # 2) Convert each row to its own dictionary
    # 3) Append the dictionary to the list
    for each_line_of_data in csv.DictReader(sources):
        # Add the dictionaries to the empty
        # content providers dictionaries list
        content_providers.append(each_line_of_data)

    for content_provider in content_providers:
        if content_provider.get(
                "default provider") == "True":
            # The style argument of radio button option
            # creates a radio button group and makes this
            # button the default.
            option = wx.RadioButton(
                content_provider_sources_panel,
                label=content_provider.get("source name"),
                style=wx.RB_GROUP)
            # Bind a radio button click event to the
            # function detailing the desired events
            option.Bind(wx.EVT_RADIOBUTTON,
                        event_handler_sources_radio_button_click)
            # Add the radio button components to the content
            # provider sources panel sizer.
            content_provider_sources_panel_sizer.Add(option,
                                                     proportion=0,
                                                     flag=wx.EXPAND | wx.ALL,
                                                     border=8)
            # Set the global 'chosen_source' to the default.
            chosen_source = content_provider.get(
                "source name")
            break

    for content_provider in content_providers:
        if content_provider.get(
                "default provider") != "True":
            # The style argument of radio button option
            # creates a radio button in the preexisting
            # group.
            option = wx.RadioButton(
                content_provider_sources_panel,
                label=content_provider.get("source name"))
            # Bind a radio button click to
            option.Bind(wx.EVT_RADIOBUTTON,
                        event_handler_sources_radio_button_click)
            # Add the radio button components to the content
            # provider sources panel sizer.
            content_provider_sources_panel_sizer.Add(option,
                                                     proportion=0,
                                                     flag=wx.EXPAND | wx.ALL,
                                                     border=8)

    # BOOST PANEL contents...
    # Create a label for the boost my search option in the
    # boost header panel.
    boost_label = wx.StaticText(boost_header_panel,
                                 label="'Boosting' your keyword search will intelligently extend your query.\nIt will automatically include commonly used synonyms, abbreviations and will even add stemmers such as 'algorithmic' for 'algorithm'.\nThis might improve your chances of a hit.\n\nThis is automatically set with a recommended value per educatior, but you can opt in or out as you wish.")
    # Add the boost label component to the boost header panel
    # sizer but with just the default fixed width.
    boost_header_panel_sizer.Add(boost_label, proportion=0,
                          flag=wx.ALL, border=8)

    def event_handler_boost_checklist_button_click(event):
        # Specify any globals to work on.
        global boost
        # Set the global 'boost' variable to the state of
        # the checkbox button.
        # By doing this, the 'event_handler_search_enter'
        # function can respond to the user's request to
        # boost or not to boost.
        if event.GetEventObject().GetValue() == True:
            boost = True
        else:
            boost = False
        pass

    def build_boost_panel():
        """
        This function is designed to be called once upon
        starting the program and then called everytime there
        is a change in the content provider selection.

        It redraws the 'boost_panel' and sets up the boost
        button inside the panel in the desired default state.
        For example, if Bit by bit is chosen as the content
        provider, the state of the 'boost' checkbox will be
        False because boosting is not recommended for this
        provider.
        """
        # Destroy the child elements of boost_panel
        # because we need to start afresh.
        boost_panel.DestroyChildren()
        # Re-add a panel to the boost panel for
        # placement of a description.
        boost_header_panel = wx.Panel(
            boost_panel)
        # Create a vertical sizer to manage the component layout
        # in the header panel.
        boost_header_panel_sizer = wx.BoxSizer(
            wx.VERTICAL)
        # Apply this to the boost header panel.
        boost_header_panel.SetSizer(
            boost_header_panel_sizer)
        # Place the boost header panel in the boost panel
        # layout, expanded to fit.
        boost_panel_sizer.Add(
            boost_header_panel, proportion=0,
            flag=wx.EXPAND)
        # Re-add a panel to the boost panel for
        # placement of a single checkbox button.
        boost_checkbox_button_panel = wx.Panel(
            boost_panel)
        # Create a vertical sizer to manage the component layout
        # in the boost checkbox button panel.
        boost_checkbox_button_panel_sizer = wx.BoxSizer(
            wx.VERTICAL)
        # Apply this to the boost checkbox button panel.
        boost_checkbox_button_panel.SetSizer(
            boost_checkbox_button_panel_sizer)
        # Place the checkbox button panel in the
        # boost panel layout, expanded to fit.
        boost_panel_sizer.Add(
            boost_checkbox_button_panel, proportion=0,
            flag=wx.EXPAND)

        # BOOST PANEL contents...
        # Create a label for the boost my search option in the
        # boost header panel.
        boost_label = wx.StaticText(boost_header_panel,
                                    label="'Boosting' your keyword search will intelligently extend your query.\nIt will automatically include commonly used synonyms, abbreviations and will even add stemmers such as 'algorithmic' for 'algorithm'.\nThis might improve your chances of a hit.\n\nThis is automatically set with a recommended value per educator, but you can opt in or out as you wish.")
        # Add the boost label component to the boost header panel
        # sizer but with just the default fixed width.
        boost_header_panel_sizer.Add(boost_label,
                                     proportion=0,
                                     flag=wx.ALL, border=8)
        # Create the 'boost my search' checkbox button.
        boost_my_search_button = wx.CheckBox(
            boost_checkbox_button_panel,
            label="Yes, boost my search!")
        # Set the state of the boost button to the state of the
        # global 'boost' (which is either True or False
        # depending on the recommendations for the chosen
        # content provider).
        boost_my_search_button.SetValue(boost)
        # Bind the checkbox button click to the relevant event
        boost_my_search_button.Bind(wx.EVT_CHECKBOX,
                    event_handler_boost_checklist_button_click)
        # Add the radio button components to the content
        # provider sources panel sizer.
        boost_checkbox_button_panel_sizer.Add(boost_my_search_button,
                                                 proportion=0,
                                                 flag=wx.EXPAND | wx.ALL,
                                                 border=8)
    # Run the function at start-up.
    build_boost_panel()

    # For the content provider SOURCES (level 4) panel...
    # Define the event handling function.
    def event_handler_content_filter_radio_button_click(event):
        """
        This function responds to any content filter radio
        button click and it ascertains which source was
        clicked and sets 'chosen_content_filter' variable.
        """
        # Specify any globals to work on.
        global chosen_content_filter
        global content_filters

        # Clear out the 'chosen_content_filter' to allow for
        # reselection if the user changes their mind.
        chosen_content_filter = "Any"

        # Find out which source radio button was clicked and
        # get the label. Set this label as the chosen
        # content type filter.
        chosen_content_filter_friendly_name = event.GetEventObject().GetLabel()
        # This label is just the "friendly name" of the
        # content type filter. It is not what the URL
        # expects to receive as part of the query.
        # The machine name is in stored in the
        # 'content_providers' dictionary.
        for filter_type_pair in content_filters:
            # If the current record belongs to the chosen
            # content provider
            if filter_type_pair.get(
                    "source name") == chosen_source:
                # and if the filter's friendly name is
                # stored in the record
                if filter_type_pair.get("content type name") == chosen_content_filter_friendly_name:
                    chosen_content_filter = filter_type_pair.get("content type ID")
                    break

    def build_filter_options_panel():
        # Specify the globals to work on.
        global chosen_source
        # Remove all the child elements of the filter panel
        # because we need to start afresh.
        content_type_filter_panel.DestroyChildren()
        # Add a panel to the content type filter panel for
        # placement of a description.
        content_type_filter_header_panel = wx.Panel(
            content_type_filter_panel)
        # Create a vertical sizer to manage the component
        # layout in the header panel.
        content_type_filter_header_panel_sizer = wx.BoxSizer(
            wx.VERTICAL)
        # Apply this to the content type filter header panel.
        content_type_filter_header_panel.SetSizer(
            content_type_filter_header_panel_sizer)
        # Place the content type filter header panel in the
        # content type filter panel layout, expanded to fit.
        content_type_filter_panel_sizer.Add(
            content_type_filter_header_panel, proportion=0)
        # Re-add a panel to the content type filter options
        # panel for placement of radio buttons for type
        # filtering options.
        content_type_filter_options_panel = wx.Panel(
            content_type_filter_panel)
        # Create a new grid sizer with 2 columns to manage
        # the component layout in the content type filter
        # options panel. One column will contain the option
        # name and the other a description of the option.
        # Set vertical gap to 0 and horizontal gap to 8px.
        content_type_filter_options_panel_sizer = wx.FlexGridSizer(
            20, 2, 0, 8)
        # Apply this to the content type filter options panel.
        content_type_filter_options_panel.SetSizer(
            content_type_filter_options_panel_sizer)
        # Attach the content type filter options panel to
        # the encompassing content type filter panel layout.
        content_type_filter_panel_sizer.Add(
            content_type_filter_options_panel, proportion=0)

        # CONTENT TYPE FILTER PANEL contents...
        # For the content type filter HEADER (level 4) panel...
        # Create a header to describe what the is required
        # of the user.
        content_type_filter_header = wx.StaticText(
            content_type_filter_header_panel,
            label="What type of material are you after?")
        # Add the text component to the content provider
        # panel sizer.
        content_type_filter_header_panel_sizer.Add(
            content_type_filter_header, proportion=0,
            flag=wx.ALL, border=8)

        # Create radio buttons for the content provider
        # sources.

        # Isaac Computer Science and Bit by bit both provide
        # content type filters.
        # For Isaac Computer Science, these are:
        # concept, question, topic
        # For Bit by bit, a few of these are:
        # explainer, step-by-step tutorial, examination
        # question

        # I have organised the data in a persistent database
        # in the form of a CSV file which looks like this...
        # source name,content type name,content type ID

        # Open the filters data file.
        filters = open("./assets/filters.csv")
        # We need a simple database which contains
        # dictionaries, one for each content provider
        # (e.g. Isaac CS)
        # Each details precisely how these providers
        # allows us to filter content into different 'types':
        # tutorial, question, etc so that we can use it to
        # look up values.
        global content_filters
        global chosen_content_filter

        # Clear out the list to avoid duplication of items
        content_filters = []

        # Use the csv library to:
        # 1) Read each line from the file
        # 2) Convert each row to its own dictionary
        # 3) Append the dictionary to the list
        for each_line_of_data in csv.DictReader(filters):
            content_filters.append(each_line_of_data)

        # Set up an empty list to be used as a database to
        # store all content type filters from the chosen
        # source.
        filter_options = []

        # Set the global 'chosen_content_filter' to the
        # default (NO filter).
        chosen_content_filter = "Any"

        # Run through the 'content_filters' database,
        # extracting those relevant to the chosen content
        # provider, building up the chosen content type
        # filter options as we go.
        for filter_type_pair in content_filters:
            # Is the current dictionary the source the user
            # has chosen to use? (e.g. Isaac CS)...
            if filter_type_pair.get(
                    "source name") == chosen_source:
                # Place the record in the 'filter_options'
                # list.
                filter_options.append(filter_type_pair)
        # Display an option to not filter to a particular
        # content type.
        no_filter = wx.RadioButton(
            content_type_filter_options_panel,
            label="Any",
            style=wx.RB_GROUP)
        # Bind a radio button click event to the function
        # detailing the desired events
        no_filter.Bind(wx.EVT_RADIOBUTTON,
                         event_handler_content_filter_radio_button_click)
        content_type_filter_options_panel_sizer.Add(
            no_filter, proportion=0, flag=wx.ALL, border=8)
        type_option_description = wx.StaticText(
            content_type_filter_options_panel,
            label="Find content of all content types.")
        content_type_filter_options_panel_sizer.Add(
            type_option_description, proportion=0, flag=wx.ALL, border=8)

        # Iterate through every dictionary which has now
        # been placed into the 'filter_options' list.
        for filter_option in filter_options:
            # The style argument of radio button option
            # creates a radio button and places it in the
            # radio group.
            type_option = wx.RadioButton(
                content_type_filter_options_panel,
                label=filter_option.get("content type name"))
            # Bind a radio button click event to the
            # function detailing the desired events.
            type_option.Bind(wx.EVT_RADIOBUTTON,
                        event_handler_content_filter_radio_button_click)
            # Option description text
            type_option_description = wx.StaticText(
                content_type_filter_options_panel,
                label=filter_option.get("description"))
            # Add the radio button components to the content
            # provider sources panel sizer.
            content_type_filter_options_panel_sizer.Add(
                type_option, proportion=0, flag=wx.ALL, border=8)
            content_type_filter_options_panel_sizer.Add(
                type_option_description, proportion=0,
                flag=wx.ALL, border=8)
    build_filter_options_panel()


    # Show the frame in the UI.
    frame.Show()
    # Start the app running so that it is creating native
    # GUI components and is 'listening' for any events that
    # may be emitted.
    app.MainLoop()


# Identify which methods should be run when the program is run.
if __name__ == '__main__':
    main()
