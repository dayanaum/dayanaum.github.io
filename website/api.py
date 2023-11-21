import wikipediaapi
import json


class infoQuery():

    def info(booktitle):
        wiki = wikipediaapi.Wikipedia('en')
        pageSearch = wiki.page(booktitle)

        if pageSearch.exists() == True:
                descJSON = json.dumps({'description':pageSearch.summary})
                descJSON = descJSON.replace('\\n',' ')
                return(descJSON)
        else:
                pageSearch = "No information available on this book."
                return json.dumps({'description':pageSearch})


