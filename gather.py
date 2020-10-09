import requests, bs4, re, datetime
import pandas as pd
from os import path

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
#The following two lines in "editions" currently kill the script, since their site is not built yet.




##############################################################################################
##############################################################################################
####### The part that comes after here was added in Sept. 2020. to also scrape the ###########
####### Results of tournaments. It gathers data from the aether hub and writes all ###########
####### tournament top8 decks to files. It could be more refined, but for the purpose ########
############################ it serves this should be sufficient #############################
##############################################################################################
##############################################################################################
print("Finished the edition, come the deck gathering")
data=requests.get("https://aetherhub.com/Events/Standard/")
cleanpagedata = bs4.BeautifulSoup(data.text, 'html.parser')

def gather_deck(rank,loc,here):
    deck_page="https://aetherhub.com/"+loc[0].replace('"', '').split("=")[-1]
    current_deck=requests.get(deck_page)
    current_deck
    c_d_clean= bs4.BeautifulSoup(current_deck.text, 'html.parser')
    c_d_clean
    try:
        c_d_clean=str(c_d_clean)[:re.search(r'Side [0-9][0-9] cards', str(c_d_clean)).span()[0]]#cut the side out for now
    except AttributeError:
        return 0
    deck={}
    im_here=0
    while True:#I'll escape when no more cards are found.
        card=re.search(r'<a class="cardLink".*', str(c_d_clean)[im_here:])#I don't need to specify end thankfully. The newline character is the end of this. I love re.
        if not card:
            break
        im_here+=card.span()[1]
        card_name=re.search(r'ProductName=.*partner=', card[0])[0][12:-13]#Yes, this is an ugly workaround but I couldn't figure out how to escape the "&amp". the standard "escape with \" didn't work nor a few other approaches.
        if card_name in deck:
            deck[card_name]+=1
        else:
            deck[card_name]=1
    for i in deck:
        here.write(str(rank)+";"+str(i)+";"+str(deck[i])+"\n")

a=re.search(r'<a class="text-dark" href="/Events/Standard/.*</a>', str(cleanpagedata))
marker=a.span()[1]#I just move this across the text so I reach everything once

while True:
    title_search = re.search(r'<a class="text-dark" href="/Events/Standard/[0-9]*".*</a>', str(cleanpagedata)[marker:])
    if not title_search:
        break
    nr=title_search[0][44:49]
    name="Standard_ID_"+str(nr) #as far as I see these are unique identifiers for the events
    name
    got_it=path.isfile("Deck_lists/"+name.replace('"', '')+"_date_"+(re.search(r"[0-9][0-9]/[0-9][0-9]/[0-9][0-9]",title_search[0])[0]).replace("/", "_") +".csv")
    marker+=title_search.span()[1]
    if got_it:
        print("I already have "+name )
        break
    else:
        print("Writing deck lists of "+name)
        f=open("Deck_lists/"+name.replace('"', '')+"_date_"+(re.search(r"[0-9][0-9]/[0-9][0-9]/[0-9][0-9]",title_search[0])[0]).replace("/", "_") +".csv", "w")# the file for decklists
        f.write("Placing;Card;Qtty\n")#semicolon as a sep since some cards have commas in their names.
        for i in range(8):#this of course assumes that for every event I have at least 8 decks. I hope this is the case.
            print("writing deck #"+str(i+1))
            deck_link = re.search(r'<tr class="deckdata" .*', str(cleanpagedata)[marker:])#the link to the deck
            if not deck_link:
                break
            marker+=deck_link.span()[1]# I'm not sure if this is necessary
            data_rank=re.search(r'data-place="[0-9]', deck_link[0]) # data_rank[0][-1] - this is the ranking achieved by the deck
            data_loc=re.search(r'data-url="/Metagame/Traditional-Standard/Deck/.*"', deck_link[0])
            gather_deck(i+1, data_loc, f)#no data rank for now, since sometimes it seems to bug out... also I didn't account for "5-8th" positions, but that would be easy to resolve.
        f.close()
