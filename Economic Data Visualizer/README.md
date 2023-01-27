—
files: [app.py]
url: varies; hosted locally using Flask
window: terminal
youtube: https://youtu.be/uDWilRxU1p4
—

# CS 50 Final Project - Economic Data Visualizer
By Sebastian Orozco & Brandon Chan

Goal: Implement a website where users can visualize answers to selected questions about economic characteristics using U.S. census data.

## Background

Inspired by FRED (Federal Reserve Economic Data), we sought to implement a similar website, albeit on a smaller scale, that allows users to graph economic data in response to specific queries. If you are unfamiliar with FRED, this is a site maintained by the Federal Reserve Bank of St. Louis, from which users can select some data, for example U.S. GDP growth, and see a graph output that represents this data over the years for which data is available.
In our web site, we source our data from the U.S. Census Bureau’s American Community Survey DP03 Selected Economic Characteristics table, which can be found at the link at the end of this section. Unfortunately, in its present form this data is not very user-friendly, and so to view data over multiple years one must manually select the data for each year and view it one year at a time.
With our web app, this data is automatically converted into a graph for users, such that it saves users' time and energy in looking up this data and graphically analyzing trends from it.

Source for data: https://data.census.gov/table?tid=ACSDP1Y2021.DP03

### Configuring

Before being able to properly run this web application, please be sure to download all program files while maintaining their relative locations to each other. For instance, .html files remain in a templates folder and .py files are in the root folder. While downloading the program files, data files will also be downloaded. The source for these data files is at the link provided at the end of the above section. In our application, we primarily use the 1-Year Estimate Profiles .csv files. If you want to download this data for yourself (say, to update your data once a year following the release of new information), you can click on the button labeled "Download Table Data" and download the desired .csv files.

### Running

Start Flask's built-in web server (within `final_project_copy/`):

```
$ flask run
```

Visit the URL outputted by `flask` to try out our code yourself. Now, you can access the site and answer queries to your heart’s content!

### Understanding

#### app.py
Upon opening `app.py`, you’ll notice various imports, which are mostly necessary libraries needed for our code to function properly. Also imported are a few helper functions, which we will discuss later.
Then, you’ll see two lists, `paths` and `queries`. The `paths` list encompasses various paths that are needed to access individual data entries within the .csv files, such that these paths are paired in the form of a dictionary to corresponding data values. This sort of parsing through data using a dictionary will be explained in further detail in the section on `helpers.py`. These paths are found using the `get_path` function, which takes up to three inputs, these being keywords leading us to the specific data we want.
How did we find these keywords? For an in-depth answer to this question, please refer to DESIGN.md to learn more about how this code works.
Then, the `queries` list translates these paths into normal human language as questions that start with "What is the number of...?", which are later given to the user as options to select from.
Afterwards, scrolling down `app.py` you'll see routes. These routes (except for the first one) accept both GET and POST request methods, such that it either renders a template, labeled `index.html` via GET, or `graph.html` or `queries.html` via METHOD if the user submits a query which they would like to see graphed.

#### helpers.py
Like app.py, helpers.py also imports various libraries at the top of the file. After a quick apology function, it then essentially creates dataframes to read the data from our .csv files, and creates dictionaries, labeled “annotations” and “annotations_dict”, which pairs the individual paths that correspond to data values, such as “Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed” with “DP03_0005E” and “DP03_0005E” with “156380433” as key-value pairs.

Below, the function `get_data` is defined to take in input, this being the path to where the desired data is (e.g. “Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed” for the number of unemployed American civilians)and plugs this into the annotation_dict to return the string address for this data as “DP03_0005E”.

Next, the function `graph` is defined to take in input, this being the string address for some specific data value (like “DP03_0005E”) and output a graph. If all this was successfully performed, a 0 is returned.

The final helper function is `get_path` which takes in input as up to three keywords. This function ultimately outputs some path (like “Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed”) that will lead to a specific data entry. We can use this output to find data for our other helper functions, like graph, to use to create a graph from.

#### `requirements.txt`
This file simply lists the packages which the app depends on.

#### `static/`
Within `static/` is contained:
`background.jpg`, which serves as the main backdrop of the website;
`favicon.ico`, which is used as the icon seen in the tabs window;
`logo.png`, which is used as the logo in the navigation bar (and redirects home!)
`styles.css`, containing all stylistic elements.

#### templates/
First is `layout.html`. This layout is used for all pages, and does a number of things. It links the website with the site icon, css style sheet, a navigation bar, a possible alert pop-up for Flask’s messages, and within `main`, a space to include all the other templates.

Second is `index.html`. This template serves as the welcome page for users, and prompts them with a user-friendly, sleek and simple design to start querying for economic data by clicking the “GO EXPLORE” button, redirecting them to ...

`query.html`. This template allows for a user to easily choose which dataset they would like to visualize. Should they fail to select a query then ...

`apology.html` shows up. This template is shown whenever an error, typically user-based, appears, with its corresponding error code and message. For example, if the user fails to select a query, it returns the error code (400), a relevant message, and a Bootstrap alert redirecting them to the homepage.

Once the user has selected a query, they are directed to `graph.html`. Here, the graph results are displayed, along with the option to submit another query!