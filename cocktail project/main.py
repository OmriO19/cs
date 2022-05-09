import numpy
from ml import matrix_factorization


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    #
    c = []
    a = {"drinks":[{"idDrink":"12864","strDrink":"Apple Cider Punch","strDrinkAlternate":None,"strTags":None,"strVideo":None,"strCategory":"Punch \/ Party Drink","strIBA":None,"strAlcoholic":"Optional alcohol","strGlass":"Collins Glass","strInstructions":"If you use the whole all spice and cloves, tie them in cheesecloth. Heat the mixture. Stir occasionally. If you want an alcoholic drink, rum would be nice.","strInstructionsES":None,"strInstructionsDE":"Wenn du das ganze Gew\u00fcrz und die Nelken verwendest, bindest du sie in ein Seihtuch. Die Mischung erhitzen. Gelegentlich umr\u00fchren. Wenn du ein alkoholisches Getr\u00e4nk willst, w\u00e4re Rum sch\u00f6n.","strInstructionsFR":None,"strInstructionsIT":"Versa tutto in un pentolino tranne spezie e chiodi di garofano, legali in una garza e tienili in ammollo.\r\nRiscalda la miscela. Mescola di tanto in tanto. Se vuoi una bevanda alcolica puoi aggiungere un po\u2019 di Rum.","strInstructionsZH-HANS":None,"strInstructionsZH-HANT":None,"strDrinkThumb":"https:\/\/www.thecocktaildb.com\/images\/media\/drink\/xrqxuv1454513218.jpg","strIngredient1":"Apple cider","strIngredient2":"Brown sugar","strIngredient3":"Lemonade","strIngredient4":"Orange juice","strIngredient5":"Cloves","strIngredient6":"Allspice","strIngredient7":"Nutmeg","strIngredient8":"Cinnamon","strIngredient9":None,"strIngredient10":None,"strIngredient11":None,"strIngredient12":None,"strIngredient13":None,"strIngredient14":None,"strIngredient15":None,"strMeasure1":"4 qt ","strMeasure2":"1 cup ","strMeasure3":"6 oz frozen ","strMeasure4":"6 oz frozen ","strMeasure5":"6 whole ","strMeasure6":"6 whole ","strMeasure7":"1 tsp ground ","strMeasure8":"3 sticks ","strMeasure9":None,"strMeasure10":None,"strMeasure11":None,"strMeasure12":None,"strMeasure13":None,"strMeasure14":None,"strMeasure15":None,"strImageSource":None,"strImageAttribution":None,"strCreativeCommonsConfirmed":"No","dateModified":"2016-02-03 15:26:58"}]}
    for j in a["drinks"]:
        a = {}
        a["name"] = j["strDrink"]
        if j["strCategory"] == "" or "Unknown" in j["strCategory"]:
            a["category"] = None
        else:
            a["category"] = j["strCategory"]
        if j["strIBA"]:
            a["iba"] = 1
        else:
            a["iba"] = 0
        a["alcoholic"] = j["strAlcoholic"]
        a["glass"] = j["strGlass"]
        a["prep"] = j["strInstructions"]
        for i in range(1, 16):
            ing = "ingredient " + str(i)
            outg = "strIngredient" + str(i)
            a[ing] = j[outg]
        a["alternative"] = j["strDrinkAlternate"]
        a["tags"] = j["strTags"]
        c.append(a)
    print(c)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
