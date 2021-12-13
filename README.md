# Python Exam Project
##### Created by Jens Gelbek, Peter Rambeck, Caroline Høg, Tobias Zimmermann

## Description
In this project, we focus on cereals; their prices and nutrional content. 
We start by giving the program a picture of some cereal we have at hand and using image recognition from `pytesseract` we obtain the brand and name of the cereal. 

Then we webscrape to get the nutrional content (calories (kcal), proteins (g), carbohydrates (g), fiber (g), fat (g), and salt (g)) of the original cereal. Futhermore, we scrape for alternatives to the original cereal. We scrape from the following websites:
1. https://hjem.foetex.dk/kategori/kolonial/morgenmad-smoerepaalaeg-og-marmelade/morgenmadsprodukter/ 
2. https://mad.coop.dk/irma/alle-varer
3. https://www.nemlig.com/
4. https://shop.rema1000.dk/

Finally, we plot the found data to make it easy to see what the different cereals cost, which are cheapest compared to price per 100 grams, and how many percent of the daily recommended nutrional intake a specific cereal makes up.

## Used Technologies
List of used technologies

## Install
pip3 install -r requirements.txt

## Status
Status (What has been done (and if anything: what was not done))

## Challenges
List of Challenges you have set up for your self (The things in your project you want to highlight)
