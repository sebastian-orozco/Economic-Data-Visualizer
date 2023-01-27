import os
import pandas as pd
import re
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import base64
from io import BytesIO


from flask import render_template

# displays an error message to the user
# from CS50 Finance distribution code
def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", code=code, message=message), code


#set path for folder containing data files
folder_path = r'%s' % (os.getcwd() + '/data')

#find all files within folder
filenames = os.listdir(folder_path)

#create list of only the files which we need (excluding metadata files, .DS_Store files, and txt files) leaving only the csv files
all_data = [file for file in filenames if 'Metadata' not in file and "txt" not in file and '.DS_Store' not in file]

#sorts the list by year (as year is in name of files) such that files will be read sequentially
all_data = sorted(all_data)

#create a dictionary joining files with their respective paths
all_paths = {}

for filename in all_data:
    tmp = (os.path.abspath(os.path.join(folder_path, filename)))
    all_paths[filename] = tmp

#create dataframe using individual data file by redefining folder_path to be the path to the first csv file in data
folder_path = folder_path + '/ACSDP1Y2010.DP03-Data.csv'

df = pd.read_csv(folder_path)

#swap keys and values, extracting the individual "paths" corresponding to each data entry
#an example of one of these "paths" is Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Employed,
#which pairs with an estimate for the number of employed americans in the civilian labor force
annotations = {v:k for k,v in df.loc[0].to_dict().items()}.keys()

#this code below is technically not needed, but it can be useful for future expansion in taking out key words from "paths" to data entries
#in this way, a potential future version of this project would use natural language processing to identify key words used by the user in making queries
#then assemble these key words into a "path" that corresponds with getting the data that the user wants
# wordspace = {}
# for annotation in annotations:
#     try:
#         annotation.replace("(","**")
#         for words in annotation.split(' '):
#             for word in words.split("!"):
#                 wordspace[word] = wordspace.get(word, 0)+1
#     except Exception as e:
#         continue

#again, swapping keys and values such that now we can access any specific value, like the number estimate for number of unemployed americans
#which is given as the key ('Estimate!!EMPLOYMENT STATUS!!In labor force!!Civilian labor force!!Unemployed'), using values (here being 'DP03_0005E')
annotations_dict = {v:k for k,v in df.loc[0].to_dict().items()}


#define function to pull location of data
def get_data(input):

    #using the annotations_dict from earlier, we can extract the alphanumeric value that corresponds
    data_location = annotations_dict[input]

    return data_location


#define function to graph our data
def graph(input):

    #create list of dataframes from all our list of files (using the paths for each file)
    dfs = []
    for path in list(all_paths.values()):
        dfs.append(pd.read_csv(path))

    #get names of columns from dataframes
    col_names =[]
    for df in dfs:
        col_names.append(df.columns)

    #rename input to query (for clarity)
    query = input

    #define function to pull data from every year available
    def multi_year_data(dfs, query, info_type = 1):
        data = []
        for df in dfs:
            try:
                data.append(df.loc[info_type,query])
            except Exception as e:
                continue
        return data

    #call multi_year_data function to pull data, returning results list of values corresponding to given query
    info_type = 1
    results = multi_year_data(dfs, query, info_type)

    #create years list
    years = []

    #extract available years from names of files
    for fname in all_data:
        res = re.split("[Y]", fname)
        if not res: continue
        years.append(res[1].split('.')[0])

    # x axis values
    x = [int(year) for year in years]
    # corresponding y axis values
    y = [int(result) for result in results]

    #creating figure
    fig = plt.figure()

    # plotting the points
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('Year')

    # naming the y axis
    plt.ylabel('Number')

    # giving a title to my graph
    plt.title('')

    #code below was the original implementation, however this produced memory leaks which led to flask crashing
    #so we must instead create buffers to output graphs
    # return plt.savefig("static/output.jpg")

    #create buffer
    buf = BytesIO()

    #save graph as png figure
    fig.savefig(buf, format="png")

    #encode then decode (may appear redundant but this is necessary to safeguard graph image data and protect against memory leaks)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    #html embedding new image (graph)
    image = f"<img src='data:image/png;base64,{data}'/>"

    #opens html file
    with open('templates/graph.html', 'rt') as file:
        #creates new temporary html file
        with open('templates/temp_graph.html', 'wt') as new:
            #for every line in file, replace the old img src with our new img src, otherwise maintain the other content by copying over those lines
            for line in file:
                if line.startswith('<img src='):
                    line = image
                    new.write(line + '\n')
                else:
                    new.write(line)

    #remove old html file
    os.remove('templates/graph.html')

    #rename our temporary to be our current html file (which is then displayed in our website)
    os.rename('templates/temp_graph.html', 'templates/graph.html')

    #success
    return 0


#define function to access data based off query
def get_path(q1, q2, q3):

    #define function to search through all possible individual data paths, returning those which match our input keywords
    def query_search(annotations, query):
        return [k for k in annotations if type(k) == str and query in k and "Annotation" not in k and "Error" not in k]

    #narrow down our paths
    new_ann = query_search(list(annotations), q1)
    if not q2 == "":
        new_ann = query_search(new_ann, q2)
    if not q3 == "":
        new_ann = query_search(new_ann, q3)

    #set variable to represent key for individual path to desired data
    ansEstimate = new_ann[0]

    #return this path
    return ansEstimate