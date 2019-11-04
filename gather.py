import requests, bs4, re, datetime
import pandas as pd

g=open("editions.dat", "r")# a list of current standard-legal sets - later I plan to include pioneer & modern?


for line in g:
    line=line.strip()
    line=line.split(";")
    data=requests.get(line[0])
    cleanpagedata = bs4.BeautifulSoup(data.text, 'html.parser')
    tag=cleanpagedata.findAll("script") # I know that the website is built in a way that it passes a JSON to the JS to build the table - I want to catch this JSON
    title_search = re.search(r"\[{.*?}\]", str(tag))
    string=line[1]+"_"+datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    # as of now, I don't know a better method of transforming a JSON string to pandas dataframe than saving it into a file...
    f=open("JSON/"+string+".json", "w")
    f.write(str(title_search.group(0))[1:-1])
    f.close()
    df=pd.read_json("JSON/"+string+".json", lines=True)
    df.drop(["quantity","setUrl", "url","fullImageUrl" ], axis=1)
    df.to_csv("CSV/"+string+".csv", index=False)
g.close()
