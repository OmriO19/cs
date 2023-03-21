import numpy as np
import pandas as pd
from surprise import NMF, Dataset, Reader
from drinks import DRINKS

ALCOHOL = ['Absinthe', 'Angostura Bitters', 'Apple Brandy', 'Apricot Brandy', 'Blackberry Liqueur', 'Cachaca',
           'Campari', 'Cherry Liqueur', 'Cognac', 'DOM Bénédictine', 'Dark Rum', 'DiSaronno', 'Drambuie', 'Galliano',
           'Gin', 'Green Créme de Menthe', 'Kirsch', 'Orange Bitters', 'Peach Schnapps', 'Peychaud’s Bitters', 'Pisco',
           'Tequila', 'Triple Sec', 'Vodka', 'Whiskey', 'White Rum']

LIQUEUR = ['Aperol', 'Baileys Irish Cream', 'Brown Créme de Cacao', 'Champagne', 'Coffee Liqueur', 'Créme de Cassis',
           'Dry White Wine', 'Ginger Beer', 'Lillet Blanc', 'Prosecco', 'Raspberry Liqueur', 'Red Port', 'Vermouth',
           'White Créme de Cacao', 'White Créme de Menthe']

NON = ['Agave Syrup', 'Coca-Cola', 'Coconut Milk', 'Cranberry Juice', 'Cream', 'Egg White', 'Egg Yolk', 'Espresso',
       'Ginger Ale', 'Grapefruit Juice', 'Grenadine', 'Lemon Juice', 'Lime', 'Lime Juice', 'Mint Leaves', 'Olive Juice',
       'Orange Flower Water', 'Orange Juice', 'Orgeat Syrup', 'Peach Bitters', 'Peach Puree', 'Pepper',
       'Pineapple Juice', 'Raspberry Syrup', 'Salt', 'Soda Water', 'Strawberry Syrup', 'Sugar', 'Sugar Syrup',
       'Tabasco', 'Tomato Juice', 'Vanilla Extract', 'Water', 'Worcestershire Sauce']

GLASSES = ["martini", "old-fashioned", "collins", "highball", "champagne-flute", "margarita", "champagne-tulip",
           "hurricane", "shot", "hot-drink", "white-wine"]

PREP = ["Shake", "Stir gently", "Build", "Muddle", "Layer", "Blend"]

ING_NUM = 75
DRI_NUM = 77
max_val = 10


def drinks_mat(drinks):
    """
    :return: the matrix that representing the given drinks data
    """
    ing_arr = []
    drinks_num = 0
    for drink in drinks:
        drinks_num += 1
        for j in (drink["ingredients"]):
            if "ingredient" in j:
                if j["ingredient"] not in ing_arr:
                    ing_arr.append(j["ingredient"])
    ing_arr.sort()
    ing_dict = {}
    k = 0
    for i in ing_arr:
        ing_dict[i] = k
        k += 1
    ing_num = len(ing_arr)
    m = np.ones((drinks_num, len(ing_arr) + len(PREP) + len(GLASSES) + 1), dtype=int)
    m = m * 0.000001
    d = 0
    for drink in drinks:
        for j in (drink["ingredients"]):
            ing = j["ingredient"]
            val = j["amount"]
            m[d][ing_dict[ing]] = val

        if "Ice" in drink["preparation"].title():
            m[d][ing_num] = 10
        if "Shake" in drink["preparation"].title():
            m[d][ing_num + 1] = 10
        elif "Stir" in drink["preparation"].title():
            m[d][ing_num + 2] = 10
        elif "Build" in drink["preparation"].title():
            m[d][ing_num + 3] = 10
        elif "Muddle" in drink["preparation"].title():
            m[d][ing_num + 4] = 10
        elif "Layer" in drink["preparation"].title():
            m[d][ing_num + 5] = 10
        elif "Blend" in drink["preparation"].title():
            m[d][ing_num + 6] = 10

        m[d][ing_num + len(PREP) + 1 + GLASSES.index(drink["glass"])] = 10

        d += 1
    return ing_arr, ing_dict, m


def ing_selection(ing_arr, ing_dict):
    """
    :param ing_arr: the ingredients array
    :param ing_dict: the ingredients' dictionary
    :return:
    """
    print("* Ingredient:", end=" ")
    ing = input()
    if ing == "-1":  # random choice
        ing = ing_arr[np.random.randint(ING_NUM)]
        print("* " + ing)
    elif ing not in ing_dict.keys():
        print("* Please choose an ingredient from the list")
        ing_selection(ing_arr, ing_dict)
    return ing


# def error_approximation():
# min_val = val
# l = 0
# rms = 0
# mse = 0
# am = 0
# for i in range(s_DRI_NUM):
#     for j in range(s_ING_NUM):
#         rms = rms + np.square((R[i, j] - R_hat[i, j]))
#         if R[i][j] == val:
#             mse = mse + np.square((val - R_hat[i, j]))
#             am += 1
#             if R_hat[i][j] < min_val:
#                 min_val = R_hat[i][j]
#                 l = j
# rms = np.sqrt(rms / (s_ING_NUM * s_DRI_NUM))
# print("RMS: " + str(rms))
# mse = np.sqrt(mse / am)
# print("MSE: " + str(mse))
# print(min_val)
# print(ing_arr[l])

def output_parsing(prediction, ing_arr):
    """
    this function prints the cocktail recipe  according to the algorithm prediction
    :param prediction: the array of the prediction
    :param ing_arr: the array of all the ingredients
    """
    # taking the ingredients with score bigger than zero
    out = {}
    j = 0
    for h in prediction[:ING_NUM]:
        if h > 0.5:
            out[h] = ing_arr[j]
        j += 1
    # print the top five ingredients and their quantities
    j = 0
    print("*", end="   ")
    for i in sorted(out.keys(), reverse=True):
        j += 1
        if j > 5:
            break
        print(str(round(i, 2)) + " cl " + out.get(i), end="   *   ")
    # print the best preparation method for the drink
    j = 0
    max_j = 0
    max_num = 0
    for num in prediction[ING_NUM + 1:ING_NUM + 7]:
        if num > max_num:
            max_num = num
            max_j = j
        j += 1
    print("\n* " + PREP[max_j] + " the ingredients", end=" ")
    if prediction[ING_NUM] > 5:
        print("with ice", end=" ")
    if max_j == 0:
        print("and strain into a", end=" ")
    elif max_j == 5:
        print("in a blender and strain into a", end=" ")
    else:
        print("in a", end=" ")
    # print the best glass for the drink
    j = 0
    max_j = 0
    max_num = 0
    for num in prediction[ING_NUM + len(PREP) + 1:]:
        if num > max_num:
            max_num = num
            max_j = j
        j += 1
    print(GLASSES[max_j] + " glass")


def opening_section():
    """prints the opening section"""
    print(
        "****************************************************************************COCKTAILS***************************************************************************************")
    print("* Please choose two ingredients -")
    print("* Alcohol -")
    print("* " + str(ALCOHOL[:10]))
    print("* " + str(ALCOHOL[10:21]))
    print("* " + str(ALCOHOL[21:]))
    print("* Liqueur -")
    print("* " + str(LIQUEUR[:10]))
    print("* " + str(LIQUEUR[10:]))
    print("* Non-alcoholic -")
    print("* " + str(NON[:12]))
    print("* " + str(NON[12:23]))
    print("* " + str(NON[23:]))


def menu():
    """
    the main function of the program
    """
    ing_arr, ing_dict, m = drinks_mat(DRINKS["drinks"])
    opening_section()
    a = ing_selection(ing_arr, ing_dict)
    print("* Amount:", end=" ")
    a_val = int(input())
    b = ing_selection(ing_arr, ing_dict)
    print("* Amount:", end=" ")
    b_val = int(input())
    print("Please wait a few seconds...", end="")

    new = np.empty(ING_NUM + len(PREP) + len(GLASSES) + 1)
    new[:] = np.nan
    new[ing_dict[a]] = a_val
    new[ing_dict[b]] = b_val
    R = np.vstack([m, new])
    # print(R)

    df = pd.DataFrame(data=R, index=range(R.shape[0]), columns=range(R.shape[1]))
    df = pd.melt(df.reset_index(), id_vars='index', var_name='items', value_name='ratings').dropna(axis=0)
    reader = Reader(rating_scale=(0, max_val + 1))
    data = Dataset.load_from_df(df[['index', 'items', 'ratings']], reader)
    k = ING_NUM - 2 + len(PREP) + len(GLASSES) + 1
    algo = NMF(n_factors=k)
    trainset = data.build_full_trainset()
    try:
        algo.fit(trainset)
    except ZeroDivisionError:
        print("* Please choose another ingredients")
        menu()
        return
    predictions = algo.test(trainset.build_testset())  # predict the known ratings
    R_hat = np.zeros_like(R)
    for uid, iid, true_r, est, _ in predictions:
        R_hat[uid, iid] = est

    predictions = algo.test(trainset.build_anti_testset())  # predict the unknown ratings
    for uid, iid, true_r, est, _ in predictions:
        R_hat[uid, iid] = est
    # print(R_hat)
    # print(R_hat[-1])
    print(
        "\r*****************************************************************************COCKTAILS**************************************************************************************")
    print("* I recommend you to use the next ingredients:")
    output_parsing(R_hat[-1], ing_arr)
    print(
        "**************************************************************************Enjoy Your Drink**********************************************************************************")


if __name__ == '__main__':
    menu()
