### app.py

The basics of `app.py` were mentioned in README.md, so here we will go in depth to explain how the code does what it does!
In `app.py` there are two lists, `paths` and `queries`. The `paths` list encompasses various paths that are needed to access individual data entries within the .csv files, such that these paths are paired in the form of a dictionary to corresponding data values, which are found using the `get_path` function that takes up to three keywords as input.
But how did we find these keywords, and how do these “paths” work? In the U.S. Census's website (again, using the aforementioned link), the data represented in the table is accessed using a dropdown menu, from which you can find data by going further down this menu into various categories. For example, to find an estimate of the number of Americans who are employed, you can click on "EMPLOYMENT STATUS", then "Population 16 years and over," then "In labor force", then "Civilian labor force", then "Employed", and then look across this row to the "Estimate" column to find the value (according to this table, the number of unemployed civilian Americans in the labor force in 2021 was 156,380,433). In the .csv files, this "trail" leading to this desired value is "Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed".
However, to access this path, we really only need a few keywords, like 'EMPLOYMENT','Civilian', and 'Employed', which is exactly what `get_path` uses to get the path for the first item in the `paths` list. By this logic, we simply looked around this table, found a couple interesting data points that we decided on including, then picked a few keywords that would lead us to this data. In this way, the `paths` list is highly customizable -- simply go to the source data page yourself, find something interesting, and add a new line appending a path with keywords that would lead to this data. So, with over hundreds of possible data points, there's hundreds of possible queries you could answer!
Correspondingly, the `queries` list translates these paths into normal human language as questions that start with "What is the number of...?". In a future iteration of this project, maybe some form of natural language processing would be used to directly convert our paths into human questions, but for the sake of simplicity, we typed out possible queries and matched these with their paths. By standardizing the format of how the queries are phrased, our .html page will dynamically take in the selected query and turn it into a title for the outputted graph, removing the "What is the..." & "?", as well as adding "From 2010-2021" to specify the years for which data is being shown.
Finally, the bottom of `app.py` is populated by routes. The first route simply returns an index.html template, on which is a button that can redirect the user to query.html. The second route, representing reaching this query.html page, accepts both GET and POST request methods. If via GET, query.html will be returned with a form that allows users to submit a query. If via POST, an invalid submitted query will return an apology, whereas a valid submitted query will be compared to our queries list, then when the index of that query in the list is found, this index value is used to find the corresponding path, which we then plug into get_data and graph to graph the data that answers this query, given to the user by ways of reaching the graph.html page. This route is very similar to the previous one, because on reaching this page, users can continue to submit queries and see new graphs, updating these graphs depending on their choice of query.

### helpers.py
Various imported libraries constitute the top part of helpers.py. Following this are

Like app.py, helpers.py also imports various libraries at the top of the file. Then, it includes a short definition of an apology function. Afterwards, we need to find a way to read through our data. So, we create a path to read into the /data file within the user’s current directory (utilizing os.getcwd() so that this process is done automatically and does not require users to manually type in their current directory). Then, we find all the files within this folder and create a list of only the files which we need (excluding metadata files, .DS_Store files, and txt files) leaving only the .csv files. To read these files in chronological order by year, we must also sort the files (this is necessary particularly for MacOS users, as unlike Windows, files will not be automatically sorted and read chronologically). Then, we create a dictionary, called “all_paths”, to join files with their respective paths. Following this action, we create a single dataframe template using an individual data file (using the 2010 data file for this template). After this, we swap keys and values, extracting the individual "paths" corresponding to each data entry. An example of one of these "paths" is “Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed”, which then pairs with a string address that corresponds with the estimate for the number of employed Americans in the civilian labor force. We repeat this process such that we get two dictionaries, annotations and annotations_dict, where one dictionary pairs these paths (ex: “Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed”) with a string address (ex: “DP03_0005E”), and the other pairs this string address with a numeric value (ex: “156380433”, the number of unemployed American civilians in 2021). The use of dictionaries here makes this process fast and efficient.
Next, the function `graph` is defined to take in input, this being the string address for some specific data value (like “DP03_0005E”) and output a graph. This is done by reading through the data folder, creating dataframes to read the .csv files for every year (using a `multi_year_data` function defined within), using the aforementioned address to pull wanted data values, append these values to a results list (which will make up the y-axis for our graph), return to our data files and extract the years (making a list of years that becomes our x-axis), then creates a graph from all this data. However, to avoid memory leaks, the way this data is shown to the user is by creating a buffer to hold our graph and creating a temp_graph.html file, reading through our current graph.html file and copying over every line except for <img src=”...”>, which it replaces with our new image source given by our new graph. Lastly, the old graph.html file is removed and the temp_graph.html file is renamed to be our updated graph.html file which is outputted to the user. If all this goes without error, a 0 is returned.

The final helper function is `get_path` which takes in input as up to three keywords. Within this function is defined `query_search` which searches through all possible individual data paths (as enumerated in our annotations dictionary), and returns those which match our input keywords. It then narrows down keyword by keyword to return a single path for an individual data entry, like “Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed”. Note that this function is embedded with a degree of flexibility, as up to three keywords can be taken as input, which is because some data really only needs two or so words to be found, but other data needs the full three keywords. For instance, the path: “Estimate!!COMMUTING TO WORK!!Car, truck, or van -- drove alone” can be found using just the keywords “COMMUTING” and “alone”. So, we can execute get_path('COMMUTING','alone',''), leaving the last entry keyword blank, to get this path.

### layout.html and corresponding css files
Why layout? Layout offers multiple design advantages.
From a coding perspective, it avoids repeating code to format the html document, backdrop, and navigation bar.
From a user perspective, the logo has been intuitively designed, such that the user can always click on it to return to the home page. The title also changes with each page to indicate to a user easily on the tab what page they are on.
Each sub-link in the navigation bar also has a hover bar from left to right, generating an aesthetically pleasing result for the user to know that they are indeed hovering over the right link.
Layout also renders a background image which fades into black, creating a more immersive user experience.

### page design principles
Each page is designed to avoid overcrowding the user with information. Thus, information (and code) is not repeated where possible. The pages for querying are designed to follow linearly from each other, creating an easy user experience.

### query.html and corresponding css files
Query takes on the class `content`, the same as index, and so begins as something familiar to the user.
The code of query.html is also dynamically linked with `app.py`, allowing for the coder to simply add to the app.py queries without having to change the `query.html` page.
Aesthetically, the select bar is customised to have a rounded, oval, teal border, matching the buttons. When hovered over, a high-contrast, readable light-grey and black appears. The options are likewise high-contrast.

### graph.html and corresponding css files
Graph on this occasion overlays on the background New York skyline with black. This is done so that the user is not distracted from the graph. The top and bottom of this black canvas is also bordered with teal to mark the section clearly to the user.
Scientific notion is used to result in a more readable, cleaner graph.

### apology.html and corresponding css files
`apology.html` is designed to be dynamically linked with the coder’s input. Should future programmers decide to add more functions, and require a check mechanism which returns an apology message to their user, apology.html, along with the helper function, achieves this dynamically by taking in and formating the error code and message. The Bootstrap alert is also used here.

### the small things: font, colour and buttons
Font was designed as san-serif to generate a minimalistic, easy-on-the-eye experience for the user.
Colours are kept in a simple, elegant colour palette, utilising teal, black, and white. Teal is custom designated at the start of the css file to make custom colour design more intuitive for programmers. High contrast allows for text to be easily readable, particularly for colour-blind users.
Buttons generally have a teal border and a transparent background. When a user hovers over the button, a smooth teal hover from left to right is designed to be generated. This hover fades when the user moves their cursor away from the button.