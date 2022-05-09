import numpy as np
import pandas as pd
from surprise import NMF, Dataset, Reader


drinks = [
    {"name": "Vesper",
     "glass": "martini",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 0.75,
          "ingredient": "Lillet Blanc"}
     ],
     "garnish": "Lemon twist",
     "preparation": "Shake over ice and strain into a chilled cocktail glass."},
    {"name": "Bacardi",
     "glass": "martini",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "White Rum",
          "label": "Bacardi White Rum"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Grenadine",
          "label": "Grenadine"}
     ],
     "preparation": "Shake with ice cubes. Strain into chilled cocktail glass."},
    {"name": "Negroni",
     "glass": "old-fashioned",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Campari"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Vermouth",
          "label": "Sweet red vermouth"}
     ],
     "garnish": "Half an orange slice",
     "preparation": "Build into old-fashioned glass filled with ice. Stir gently."},
    {"name": "Rose",
     "glass": "martini",
     "ingredients": [
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Kirsch"},
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Vermouth",
          "label": "Dry vermouth"},
         {"unit": "cl", "amount": 3 * 0.062, "ingredient": "Strawberry Syrup"}
     ],
     "preparation": "Stir all ingredients with ice and strain into a cocktail glass."},
    {"name": "Old Fashioned",
     "glass": "old-fashioned",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Whiskey",
          "label": "Bourbon or rye whiskey"},
         {"unit": "cl", "amount": 2 * 0.062, "ingredient": "Angostura Bitters"},
         {"unit": "cl", "amount": 0.5, "ingredient": "Sugar"},
         {"unit": "cl", "amount": 2 * 0.062, "ingredient": "Water"}
     ],
     "garnish": "Orange slice and cherry",
     "preparation": "Place sugar cube in old-fashioned glass and saturate with bitters, add a dash of plain water. Muddle until dissolve. Fill the glass with ice cubes and add whisky."},
    {"name": "Tuxedo",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Gin",
          "label": "Old Tom Gin"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Vermouth",
          "label": "Dry vermouth"},
         {"unit": "cl", "amount": 0.25, "ingredient": "Cherry Liqueur"},
         {"unit": "cl", "amount": 0.125, "ingredient": "Absinthe"},
         {"unit": "cl", "amount": 3 * 0.062, "ingredient": "Orange Bitters"}
     ],
     "garnish": "Cherry and lemon twist",
     "preparation": "Stir all ingredients with ice and strain into cocktail glass."},
    {"name": "Mojito",
     "glass": "collins",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "White Rum",
          "label": "White Cuban Rum"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 3, "ingredient": "Mint Leaves"},
         {"unit": "cl",
          "amount": 1, "ingredient": "Sugar"},
         {"unit": "cl",
          "amount": 10, "ingredient": "Soda Water"}
     ],
     "garnish": "Mint leaves and lemon slice",
     "preparation": "Muddle mint sprigs with sugar and lime Juice. Add splash of soda water and fill glass with cracked ice. Pour Rum and top with soda water. Serve with straw."},
    {"name": "Horse's Neck",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 12,
          "ingredient": "Ginger Ale"},
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Angostura Bitters"}
     ],
     "garnish": "Lemon twist",
     "preparation": "Build into highball glass with ice cubes. Stir gently. If required, add dashes of Angostura bitters."},
    {"name": "Planter's Punch",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Dark Rum"},
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "Orange Juice"},
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "Pineapple Juice"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Grenadine",
          "label": "Grenadine"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"},
         {"unit": "cl",
          "amount": 3 * 0.062, "ingredient": "Angostura Bitters"}
     ],
     "garnish": "Pineapple slice and a cherry",
     "preparation": "Pour all ingredients, except the bitters, into shaker filled with ice. Shake. Pour into large glass, filled with ice. Add Angostura bitters, “on top”."},
    {"name": "Sea Breeze",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 12,
          "ingredient": "Cranberry Juice"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Grapefruit Juice"}
     ],
     "garnish": "Lime wedge",
     "preparation": "Build all ingredients in a rock glass filled with ice."},
    {"name": "Pisco Sour",
     "glass": "old-fashioned",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Pisco"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"},
         {"unit": "cl",
          "amount": 3, "ingredient": "Egg White"}
     ],
     "preparation": "Shake and strain into a chilled champagne flute. Dash some Angostura bitters on top."},
    {"name": "Long Island Iced Tea",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Tequila"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 2.5,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 3.0,
          "ingredient": "Sugar Syrup",
          "label": "Gomme syrup"},
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Coca-Cola"}
     ],
     "garnish": "Lemon twist",
     "preparation": "Add all ingredients into highball glass filled with ice. Stir gently. Serve with straw."},
    {"name": "Clover Club",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Raspberry Syrup",
          "label": "Raspberry syrup"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 2, "ingredient": "Egg White"}
     ],
     "preparation": "Shake with ice cubes. Strain into cocktail glass."},
    {"name": "Angel Face",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Apricot Brandy"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Apple Brandy"}
     ],
     "preparation": "Shake with ice cubes. Strain into a cocktail glass."},
    {"name": "Mimosa",
     "glass": "champagne-flute",
     "category": "Sparkling Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 7.5,
          "ingredient": "Champagne"},
         {"unit": "cl",
          "amount": 7.5,
          "ingredient": "Orange Juice"}
     ],
     "garnish": "Optional orange twist",
     "preparation": "Pour orange Juice into flute and gently pour Champagne. Stir gently. Note: Buck's Fizz is a very similar cocktail but made of two parts champagne to one part orange Juice."},
    {"name": "Whiskey Sour",
     "glass": "old-fashioned",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Whiskey",
          "label": "Bourbon whiskey"},
         {"unit": "cl",
          "amount": 3.0,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"}
     ],
     "garnish": "Half an orange slice and cherry",
     "preparation": "Dash egg white (Optional: if used shake little harder to foam up the egg white). Pour all ingredients into cocktail shaker filled with ice. Shake. Strain into cocktail glass. If served ‘On the rocks’, strain ingredients into old-fashioned glass filled with ice."},
    {"name": "Screwdriver",
     "glass": "highball",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 10,
          "ingredient": "Orange Juice"}
     ],
     "garnish": "Orange slice",
     "preparation": "Build into a highball glass filled with ice. Stir gently."},
    {"name": "Cuba Libre",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 12,
          "ingredient": "Coca-Cola"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Lime Juice"}
     ],
     "garnish": "Lime wedge",
     "preparation": "Build all ingredients in a highball glass filled with ice."},
    {"name": "Manhattan",
     "glass": "martini",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Whiskey",
          "label": "Rye whiskey"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Vermouth",
          "label": "Red vermouth"},
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Angostura Bitters"}
     ],
     "garnish": "Cherry",
     "preparation": "Stir in mixing glass with ice cubes. Strain into chilled cocktail glass."},
    {"name": "Porto Flip",
     "glass": "martini",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Red Port"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Egg Yolk"}
     ],
     "preparation": "Shake with ice cubes. Strain into cocktail glass. Sprinkle with fresh ground nutmeg."},
    {"name": "Gin Fizz",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"},
         {"unit": "cl",
          "amount": 8,
          "ingredient": "Soda Water"}
     ],
     "garnish": "Lemon slice",
     "preparation": "Shake all ingredients with ice cubes, except soda water. Pour into tumbler. Top with soda water."},
    {"name": "Espresso Martini",
     "glass": "martini",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Coffee Liqueur",
          "label": "Kahlúa"},
         {"unit": "cl",
          "amount": 1, "ingredient": "Sugar Syrup"},
         {"unit": "cl",
          "amount": 3, "ingredient": "Espresso"}
     ],
     "preparation": "Shake and strain into a chilled cocktail glass."},
    {"name": "Margarita",
     "glass": "margarita",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "Tequila"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Triple Sec",
          "label": "Cointreau"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lime Juice"}
     ],
     "preparation": "Shake with ice cubes. Strain into cocktail glass rimmed with salt (note:Fruit Margarita - blend selected fruit with the above recipe)."},
    {"name": "French 75",
     "glass": "champagne-tulip",
     "category": "Sparkling Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 2 * 0.062, "ingredient": "Sugar Syrup"},
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Champagne"}
     ],
     "preparation": "Shake with ice cubes, except for champagne. Strain into a champagne flute. Top up with champagne. Stir gently."},
    {"name": "Yellow Bird",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Galliano"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lime Juice"}
     ],
     "preparation": "Shake and strain into a chilled cocktail glass."},
    {"name": "Pina Colada",
     "glass": "hurricane",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 9,
          "ingredient": "Pineapple Juice"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Coconut Milk"}
     ],
     "garnish": "Pineapple slice and a cherry",
     "preparation": "Blend all the ingredients with ice in a electric blender, pour into a large goblet or Hurricane glass and serve with straws."},
    {"name": "Aviation",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Cherry Liqueur",
          "label": "Maraschino"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lemon Juice"}
     ],
     "preparation": "Shake and strain into a chilled cocktail glass."},
    {"name": "Bellini",
     "glass": "champagne-flute",
     "category": "Sparkling Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 10,
          "ingredient": "Prosecco"},
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Peach Puree"}
     ],
     "preparation": "Pour peach puree into chilled glass and add sparkling wine. Stir gently. Variations: Puccini (fresh mandarin Juice), Rossini (fresh strawberry puree), Tintoretto (fresh pomegranate Juice)"},
    {"name": "Grasshopper",
     "glass": "martini",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "White Créme de Cacao",
          "label": "White Créme de Cacao"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Green Créme de Menthe",
          "label": "Green Créme de Menthe"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Cream"}
     ],
     "preparation": "Shake with ice cubes. Strain into chilled cocktail glass."},
    {"name": "Tequila Sunrise",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Tequila"},
         {"unit": "cl",
          "amount": 9,
          "ingredient": "Orange Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Grenadine",
          "label": "Grenadine"}
     ],
     "garnish": "Orange slice and a cherry",
     "preparation": "Build tequila and orange Juice into highball with ice cubes. Add a splash of grenadine to create sunrise effect. Do not stir."},
    {"name": "Daiquiri",
     "glass": "martini",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 2.5,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Sugar Syrup",
          "label": "Simple syrup"}
     ],
     "preparation": "Shake and strain into a cocktail glass."},
    {"name": "Rusty Nail",
     "glass": "old-fashioned",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Whiskey",
          "label": "Scotch whisky"},
         {"unit": "cl",
          "amount": 2.5,
          "ingredient": "Drambuie"}
     ],
     "garnish": "Lemon twist",
     "preparation": "Build into old-fashioned glass filled with ice. Stir gently."},
    {"name": "B52",
     "glass": "shot",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Coffee Liqueur",
          "label": "Kahlúa"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Baileys Irish Cream",
          "label": "Baileys Irish Cream"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Triple Sec",
          "label": "Grand Marnier"}
     ],
     "preparation": "Layer ingredients one at a time starting with Kahlúa, followed by Baileys Irish Cream and top with Grand Marnier. Flame the Grand Marnier, serve while the flame is still on, accompanied with a straw on side plate."},
    {"name": "Stinger",
     "glass": "martini",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "White Créme de Menthe",
          "label": "White Créme de Menthe"}
     ],
     "preparation": "Stir in mixing glass with ice cubes. Strain into a cocktail glass."},
    {"name": "Golden Dream",
     "glass": "martini",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Galliano"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Orange Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Cream"}
     ],
     "preparation": "Shake with ice cubes. Strain into chilled cocktail glass."},
    {"name": "God Mother",
     "glass": "old-fashioned",
     "ingredients": [
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "DiSaronno"}
     ],
     "preparation": "Build into old fashioned glass filled with ice cubes. Stir gently."},
    {"name": "Spritz Veneziano",
     "glass": "old-fashioned",
     "category": "Sparkling Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Prosecco"},
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Aperol"},
         {"unit": "cl",
          "amount": 0.6, "ingredient": "Soda Water"}
     ],
     "garnish": "Half an orange slice",
     "preparation": "Build into an old-fashioned glass filled with ice. Top with a splash of soda water."},
    {"name": "Bramble",
     "glass": "old-fashioned",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Blackberry Liqueur"}
     ],
     "garnish": "Lemon slice and two blackberries",
     "preparation": "Build over crushed ice, in a rock glass. Stir, then pour the blackberry Liqueur over the top of the drink in a circular fashion."},
    {"name": "Alexander",
     "glass": "martini",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Brown Créme de Cacao",
          "label": "Brown Créme de Cacao"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Cream"}
     ],
     "preparation": "Shake and strain into a chilled cocktail glass. Sprinkle with fresh ground nutmeg."},
    {"name": "Lemon Drop Martini",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 2.5,
          "ingredient": "Vodka",
          "label": "Citron Vodka"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lemon Juice"}
     ],
     "garnish": "Lemon slice",
     "preparation": "Shake and strain into a chilled cocktail glass rimmed with sugar."},
    {"name": "French Martini",
     "glass": "martini",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Raspberry Liqueur"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Pineapple Juice"}
     ],
     "preparation": "Stir in mixing glass with ice cubes. Strain into chilled cocktail glass. Squeeze oil from lemon peel onto the drink."},
    {"name": "Black Russian",
     "glass": "old-fashioned",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Coffee Liqueur"}
     ],
     "preparation": "Build into old fashioned glass filled with ice cubes. Stir gently. Note: for White Russian, float fresh cream on the top and stir gently."},
    {"name": "Bloody Mary",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 9,
          "ingredient": "Tomato Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 2 * 0.062, "ingredient": "Worcestershire Sauce"},
         {"unit": "cl",
          "amount": 2 * 0.062, "ingredient": "Tabasco"},
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Salt"},
         # SALT?????????????????????????????????????????????????????????????????????
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Pepper"}
     ],
     "garnish": "Celery and optionally lemon wedge",
     "preparation": "Stir gently, pour all ingredients into highball glass."},
    {"name": "Mai-tai",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Dark Rum"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Triple Sec",
          "label": "Orange Curaçao"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Orgeat Syrup",
          "label": "Orgeat syrup"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Lime Juice"}
     ],
     "garnish": "Pineapple spear, mint leaves and lime wedge",
     "preparation": "Shake and strain into highball glass. Serve with straw."},
    {"name": "Barracuda",
     "glass": "margarita",
     "category": "Sparkling Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Dark Rum",
          "label": "Gold Rum"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Galliano"},
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Pineapple Juice"},
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 3, "ingredient": "Prosecco"}
     ],
     "preparation": "Shake four ingredients with ice. Strain into glass, top with Sparkling wine."},
    {"name": "Sex on the Beach",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Peach Schnapps"},
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Cranberry Juice"},
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Orange Juice"}
     ],
     "garnish": "Orange slice",
     "preparation": "Build all ingredients in a highball glass filled with ice."},
    {"name": "Monkey Gland",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Orange Juice"},
         {"unit": "cl",
          "amount": 3 * 0.062, "ingredient": "Absinthe"},
         {"unit": "cl",
          "amount": 1.5, "ingredient": "Grenadine"}
     ],
     "preparation": "Shake and strain into a chilled cocktail glass."},
    {"name": "Derby",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl", "amount": 6, "ingredient": "Gin"},
         {"unit": "cl", "amount": 2 * 0.062, "ingredient": "Peach Bitters"},
         {"unit": "cl", "amount": 3, "ingredient": "Mint Leaves"}
     ],
     "garnish": "Mint leaves",
     "preparation": "Stir in mixing glass with ice cubes. Strain into a cocktail glass."},
    {"name": "Sidecar",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Lemon Juice"}
     ],
     "preparation": "Shake with ice cubes. Strain into cocktail glass."},
    {"name": "Irish Coffee",
     "glass": "hot-drink",
     "category": "Hot Drink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Whiskey",
          "label": "Irish whiskey"},
         {"unit": "cl",
          "amount": 9,
          "ingredient": "Espresso"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Cream"},
         {"unit": "cl",
          "amount": 0.5, "ingredient": "Sugar"}
     ],
     "preparation": "Warm the Irish whiskey over a burner. Pour into the glass (for hot drink) hot coffee, and add a teaspoon of brown sugar and stir. Float Cream on top."},
    {"name": "Sazerac",
     "glass": "old-fashioned",
     "category": "After Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Absinthe"},
         {"unit": "cl",
          "amount": 0.5, "ingredient": "Sugar"},
         {"unit": "cl",
          "amount": 2 * 0.062, "ingredient": "Peychaud’s Bitters"}
     ],
     "garnish": "Lemon twist",
     "preparation": "Rinse a chilled old-fashioned glass with the absinthe, add crushed ice and set it aside. Stir the remaining ingredients over ice and set it aside. Discard the ice and any excess absinthe from the prepared glass, and strain the drink into the glass."
                    " Note: The original recipe changed after the American Civil War, rye whiskey substituted cognac as it became hard to obtain."},
    {"name": "Americano",
     "glass": "old-fashioned",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Campari"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Vermouth",
          "label": "Red vermouth"},
         {"unit": "cl",
          "amount": 3, "ingredient": "Soda Water"}
     ],
     "garnish": "Half an orange slice",
     "preparation": "Build into old fashioned glass filled with ice cubes. Add a splash of soda water."},
    {"name": "Singapore Sling",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Cherry Liqueur"},
         {"unit": "cl",
          "amount": 0.75,
          "ingredient": "Triple Sec",
          "label": "Cointreau"},
         {"unit": "cl",
          "amount": 0.75,
          "ingredient": "DOM Bénédictine"},
         {"unit": "cl",
          "amount": 12.0,
          "ingredient": "Pineapple Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Grenadine",
          "label": "Grenadine"},
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Angostura Bitters"}
     ],
     "garnish": "Pineapple slice and a cherry",
     "preparation": "Shake with ice cubes. Strain into highball glass."},
    {"name": "French Connection",
     "glass": "old-fashioned",
     "ingredients": [
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "DiSaronno"}
     ],
     "preparation": "Build into old fashioned glass filled with ice cubes. Stir gently."},
    {"name": "Moscow Mule",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 12,
          "ingredient": "Ginger Beer"},
         {"unit": "cl",
          "amount": 0.5,
          "ingredient": "Lime Juice"}],
     "garnish": "Lime slice",
     "preparation": "Combine the vodka and ginger beer. Add lime Juice and stir gently."},
    {"name": "John Collins",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"},
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Soda Water"}
     ],
     "garnish": "Lemon slice and a cherry",
     "preparation": "Build into highball glass filled with ice. Stir gently. Add a dash of Angostura bitters. (Note: Use Old Tom Gin for Tom Collins)"},
    {"name": "Kir",
     "glass": "white-wine",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 9,
          "ingredient": "Dry White Wine"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Créme de Cassis",
          "label": "Créme de Cassis"}
     ],
     "preparation": "Pour Créme de Cassis into glass, top up with white wine. Stir gently. For Kir Royal: Use champagne instead of white wine."},
    {"name": "Mint Julep",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Whiskey",
          "label": "Bourbon whiskey"},
         {"unit": "cl",
          "amount": 3, "ingredient": "Mint Leaves"},
         {"unit": "cl",
          "amount": 1, "ingredient": "Sugar"},
         {"unit": "cl",
          "amount": 2, "ingredient": "Water"}
     ],
     "garnish": "Mint sprig",
     "preparation": "In a highball glass gently muddle the mint, Powdered sugar and water. Fill the glass with cracked ice, add Bourbon and stir well until the glass is frost."},
    {"name": "Tommy's Margarita",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Tequila"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 0.5, "ingredient": "Agave Syrup"}
     ],
     "preparation": "Shake and strain into a chilled cocktail glass."},
    {"name": "Paradise",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Apricot Brandy"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Orange Juice"}
     ],
     "preparation": "Shake with ice cubes. Strain into chilled cocktail glass."},
    {"name": "Dirty Martini",
     "glass": "martini",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Vermouth",
          "label": "Dry vermouth"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Olive Juice"}
     ],
     "garnish": "Green olive",
     "preparation": "Stir in mixing glass with ice cubes. Strain into chilled martini glass."},
    {"name": "Champagne Cocktail",
     "glass": "champagne-flute",
     "category": "Sparkling Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 9,
          "ingredient": "Champagne"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 2 * 0.062, "ingredient": "Angostura Bitters"},
         {"unit": "cl",
          "amount": 0.5, "ingredient": "Sugar"}  # sugar???????????????????????????????????
     ],
     "garnish": "Orange slice and a cherry",
     "preparation": "Add dash of Angostura bitter onto sugar cube and drop it into champagne flute. Add cognac followed by pouring gently chilled champagne. Stir gently."},
    {"name": "Mary Pickford",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Cherry Liqueur",
          "label": "Maraschino"},
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Pineapple Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Grenadine",
          "label": "Grenadine"}
     ],
     "preparation": "Shake and strain into a chilled large cocktail glass."},
    {"name": "Hemingway Special",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Grapefruit Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Cherry Liqueur",
          "label": "Maraschino"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lime Juice"}
     ],
     "preparation": "Shake with ice cubes. Strain into a double cocktail glass."},
    {"name": "Dark 'n' Stormy",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Dark Rum"},
         {"unit": "cl",
          "amount": 10,
          "ingredient": "Ginger Beer"}
     ],
     "garnish": "Lime wedge",
     "preparation": "Build into highball glass filled with ice. Add Rum first and top it with ginger beer."},
    {"name": "Ramos Fizz",
     "glass": "highball",
     "category": "Longdrink",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Cream"},
         {"unit": "cl",
          "amount": 2, "ingredient": "Egg White"},
         {"unit": "cl",
          "amount": 3 * 0.062, "ingredient": "Orange Flower Water"},
         {"unit": "cl",
          "amount": 1 * 0.062, "ingredient": "Vanilla Extract"},
         {"unit": "cl",
          "amount": 3, "ingredient": "Soda Water"}
     ],
     "preparation": "Pour all ingredients (except soda) in a mixing glass, dry shake (no ice) for two minutes, add ice and hard shake for another minute. Strain into a highball glass without ice, top with soda."},
    {"name": "Russian Spring Punch",
     "glass": "highball",
     "category": "Sparkling Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 2.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 2.5,
          "ingredient": "Lemon Juice"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Créme de Cassis",
          "label": "Créme de Cassis"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Sugar Syrup",
          "label": "Sugar syrup"}
     ],
     "garnish": "Lemon slice and a blackberry",
     "preparation": "Shake the ingredients and pour into highball glass. Top with Sparkling wine."},
    {"name": "God Father",
     "glass": "old-fashioned",
     "ingredients": [
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "Whiskey",
          "label": "Scotch whisky"},
         {"unit": "cl",
          "amount": 3.5,
          "ingredient": "DiSaronno"}
     ],
     "preparation": "Build into old fashioned glass filled with ice cubes. Stir gently."},
    {"name": "Cosmopolitan",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Vodka",
          "label": "Citron Vodka"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Triple Sec",
          "label": "Cointreau"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Cranberry Juice"}
     ],
     "garnish": "Lime slice",
     "preparation": "Shake with ice cubes. Strain into a large cocktail glass."},
    {"name": "Dry Martini",
     "glass": "martini",
     "category": "Before Dinner Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 6,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Vermouth",
          "label": "Dry vermouth"}
     ],
     "preparation": "Stir in mixing glass with ice cubes. Strain into chilled martini glass. Squeeze oil from lemon peel onto the drink, or garnish with olive."},
    {"name": "Between the Sheets",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "White Rum"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Cognac"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Lemon Juice"}
     ],
     "preparation": "Shake with ice cubes. Strain into chilled cocktail glass."},
    {"name": "Casino",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Gin",
          "label": "Old Tom Gin"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Cherry Liqueur",
          "label": "Maraschino"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Orange Bitters"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Lemon Juice"}
     ],
     "garnish": "Lemon twist and a cherry",
     "preparation": "Shake with ice cubes. Strain into chilled cocktail glass."},
    {"name": "Caipirinha",
     "glass": "old-fashioned",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Cachaca"},
         {"unit": "cl",
          "amount": 4, "ingredient": "Lime"},
         {"unit": "cl",
          "amount": 1, "ingredient": "Sugar"}
     ],
     "preparation": "Place lime and sugar in old fashion glass and muddle. Fill glass with ice and Cachaca. Stir gently (note:Caipiroska- use Vodka instead of Cachaca)."},
    {"name": "Vampiro",
     "glass": "highball",
     "ingredients": [
         {"unit": "cl",
          "amount": 5,
          "ingredient": "Tequila",
          "label": "Silver Tequila"},
         {"unit": "cl",
          "amount": 7,
          "ingredient": "Tomato Juice"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Orange Juice"},
         {"unit": "cl",
          "amount": 1,
          "ingredient": "Lime Juice"},
         {"unit": "cl",
          "amount": 1, "ingredient": "Grenadine"},
         {"unit": "cl",
          "amount": 0.0625, "ingredient": "Pepper"},
         {"unit": "cl",
          "amount": 0.0625, "ingredient": "Worcestershire Sauce"},
         {"unit": "cl",
          "amount": 0.0625, "ingredient": "Salt"}
     ],
     "garnish": "Lime wedge and a green or red chili",
     "preparation": "Shake with ice cubes. Strain into a highball glass, filled with ice."},
    {"name": "Kamikaze",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Lime Juice"}
     ],
     "preparation": "Shake with ice and strain into a chilled cocktail glass."},
    {"name": "White Lady",
     "glass": "martini",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4,
          "ingredient": "Gin"},
         {"unit": "cl",
          "amount": 3,
          "ingredient": "Triple Sec"},
         {"unit": "cl",
          "amount": 2,
          "ingredient": "Lemon Juice"}
     ],
     "preparation": "Shake with ice cubes. Strain into large cocktail glass."},

    {"name": "Harvey Wallbanger",
     "glass": "highball",
     "category": "All Day Cocktail",
     "ingredients": [
         {"unit": "cl",
          "amount": 4.5,
          "ingredient": "Vodka"},
         {"unit": "cl",
          "amount": 1.5,
          "ingredient": "Galliano"},
         {"unit": "cl",
          "amount": 9,
          "ingredient": "Orange Juice"}
     ],
     "garnish": "Orance slice and a cherry",
     "preparation": "Build vodka and orange Juice into a highball glass filled with ice. Stir gently and float Galliano on top."}
]

"""
{"name": "White Lady", "glass": "martini", "category": "All Day Cocktail",
 "ingredients": [{"unit": "cl", "amount": 4, "ingredient": "Gin"},
                 {"unit": "cl", "amount": 3, "ingredient": "Triple Sec"},
                 {"unit": "cl", "amount": 2, "ingredient": "Lemon Juice"}],
                 "preparation": "Shake with ice cubes. Strain into large cocktail glass."}
"""
alcohol = ['Absinthe', 'Angostura Bitters', 'Apple Brandy', 'Apricot Brandy', 'Blackberry Liqueur', 'Cachaca', 'Campari', 'Cherry Liqueur', 'Cognac', 'DOM Bénédictine', 'Dark Rum', 'DiSaronno', 'Drambuie', 'Galliano', 'Gin', 'Green Créme de Menthe', 'Kirsch', 'Orange Bitters', 'Peach Schnapps', 'Peychaud’s Bitters', 'Pisco', 'Tequila', 'Triple Sec', 'Vodka', 'Whiskey', 'White Rum']

liqueur = ['Aperol', 'Baileys Irish Cream', 'Brown Créme de Cacao', 'Champagne', 'Coffee Liqueur', 'Créme de Cassis', 'Dry White Wine', 'Ginger Beer', 'Lillet Blanc', 'Prosecco', 'Raspberry Liqueur', 'Red Port', 'Vermouth', 'White Créme de Cacao', 'White Créme de Menthe']

non = ['Agave Syrup', 'Coca-Cola', 'Coconut Milk', 'Cranberry Juice', 'Cream', 'Egg White', 'Egg Yolk', 'Espresso', 'Ginger Ale', 'Grapefruit Juice', 'Grenadine', 'Lemon Juice', 'Lime', 'Lime Juice', 'Mint Leaves', 'Olive Juice', 'Orange Flower Water', 'Orange Juice', 'Orgeat Syrup', 'Peach Bitters', 'Peach Puree', 'Pepper', 'Pineapple Juice', 'Raspberry Syrup', 'Salt', 'Soda Water', 'Strawberry Syrup', 'Sugar', 'Sugar Syrup', 'Tabasco', 'Tomato Juice', 'Vanilla Extract', 'Water', 'Worcestershire Sauce']

glasses = ["martini", "old-fashioned", "collins", "highball", "champagne-flute", "margarita", "champagne-tulip",
           "hurricane", "shot", "hot-drink", "white-wine"]

prep = ["Shake", "Stir gently", "Build", "Muddle", "Layer", "Blend"]


def drinks_mat():
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
    m = np.ones((drinks_num, len(ing_arr) + len(prep) + len(glasses) + 1), dtype=int)
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

        m[d][ing_num + len(prep) + 1 + glasses.index(drink["glass"])] = 10

        d += 1
    return ing_arr, ing_dict, m


def menu():
    ing_arr, ing_dict, m = drinks_mat()
    ING_NUM = 75
    DRI_NUM = 77
    max_val = 10
    print("****************************************************************************COCKTAILS****************************************************************************************")
    print("* Please choose two ingredients -")
    print("* Alcohol -")
    print("* " + str(alcohol[:10]))
    print("* " + str(alcohol[10:21]))
    print("* " + str(alcohol[21:]))
    print("* Liqueur -")
    print("* " + str(liqueur[:10]))
    print("* " + str(liqueur[10:]))
    print("* Non-alcoholic -")
    print("* " + str(non[:12]))
    print("* " + str(non[12:23]))
    print("* " + str(non[23:]))
    print("* First ingredient:", end=" ")
    a = input()
    if a == "-1":
        a = ing_arr[np.random.randint(ING_NUM)]
        print("* " + a)
    print("* Amount:", end=" ")
    a_val = int(input())
    print("* Second ingredient:", end=" ")
    b = input()
    if b == "-1":
        b = ing_arr[np.random.randint(ING_NUM)]
        print("* " + b)
    print("* Amount:", end=" ")
    b_val = int(input())
    print("Please wait a few seconds...", end="")
    new = np.empty(ING_NUM + len(prep) + len(glasses) + 1)
    new[:] = np.nan
    new[ing_dict[a]] = a_val
    new[ing_dict[b]] = b_val
    R = np.vstack([m, new])
    # print(R)
    df = pd.DataFrame(data=R, index=range(R.shape[0]), columns=range(R.shape[1]))
    df = pd.melt(df.reset_index(), id_vars='index', var_name='items', value_name='ratings').dropna(axis=0)
    reader = Reader(rating_scale=(0, max_val + 1))
    data = Dataset.load_from_df(df[['index', 'items', 'ratings']], reader)
    k = ING_NUM - 2 + len(prep) + len(glasses) + 1
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

    predictions = algo.test(trainset.build_anti_testset())  # predict the unknown ratings
    for uid, iid, true_r, est, _ in predictions:
        R_hat[uid, iid] = est
    # print(R_hat)
    # print(R_hat[-1])
    print("\r*****************************************************************************COCKTAILS***************************************************************************************")
    print("* I recommend you to use the next ingredients:")
    out = {}
    j = 0
    for h in R_hat[-1][:ING_NUM]:
        if h > 0.5:
            out[h] = ing_arr[j]
        j += 1
    j = 0
    print("*", end="   ")
    for i in sorted(out.keys(), reverse=True):
        j += 1
        if j > 5:
            break
        print(str(round(i, 2)) + " cl " + out.get(i), end="   *   ")
    j = 0
    max_j = 0
    max_num = 0
    for num in R_hat[-1][ING_NUM + 1:ING_NUM + 7]:
        if num > max_num:
            max_num = num
            max_j = j
        j += 1
    print("\n* " + prep[max_j] + " the ingredients", end=" ")
    if R_hat[-1][ING_NUM] > 5:
        print("with ice", end=" ")
    if max_j == 0:
        print("and strain into a", end=" ")
    elif max_j == 5:
        print("in a blender and strain into a", end=" ")
    else:
        print("in a", end=" ")
    j = 0
    max_j = 0
    max_num = 0
    for num in R_hat[-1][ING_NUM + len(prep) + 1:]:
        if num > max_num:
            max_num = num
            max_j = j
        j += 1
    print(glasses[max_j] + " glass")
    print("**************************************************************************Enjoy Your Drink***********************************************************************************")


if __name__ == '__main__':
    menu()
