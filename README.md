# Python Exam Project
##### Created by Jens Gelbek, Peter Rambeck, Caroline Høg, Tobias Zimmermann

## Description
In this project, we focus on cereals; their prices and nutrional content. 
We start by giving the program a picture of some cereal we have at hand and using image recognition from `pytesseract` we obtain the brand and name of the cereal. 

Then we webscrape to get the nutrional content (calories (kcal), proteins (g), carbohydrates (g), fiber (g), fat (g), and salt (g)) of the original cereal. Futhermore, we scrape for alternatives to the original cereal. We scrape from the following websites:
1. https://hjem.foetex.dk/kategori/kolonial/morgenmad-smoerepaalaeg-og-marmelade/morgenmadsprodukter/ 
2. https://mad.coop.dk/irma/alle-varer
3. https://www.nemlig.com/

Finally, we plot the found data to make it easy to see what the different cereals cost, which are cheapest compared to price per 100 grams, and how many percent of the daily recommended nutrional intake a specific cereal makes up.

## Used Technologies
- `numpy`
- `pandas`
- `matplotlib.pyplot`
- `pytesseract`
- `nltk`
- `opencv`
- `Selenium`
- `Beautiful Soup`
- `lxml`
- `concurrent.futures`

## Install
- pip3 install -r requirements.txt
- docker exec -it -u root notebookserver bash
- cp exam_project/dan.traineddata /usr/share/tesseract-ocr/4.00/tessdata/dan.traineddata

## Status

### Plotting
Status: Completed 

We want to visualize the following:
- The prices of cereals at the different stores
- Prices per 100 grams for easier comparison between cereal products
- The nutrional content in all found cereals 
- The nutrional content in a specific cereal compared to how many percent it covers of a person's daily recommended nutrional intake

And all of this has been plotted, or visualized in a different way.

## Challenges
List of Challenges you have set up for your self (The things in your project you want to highlight)

### Webscraping
Initially we wanted to have 4 supermaked chains to lookup for image "Product & Brand" recognigtion:
1. Irma, 
2. Nemlig, 
3. Føtex, 
4. Rema, 
though as Rema's data-site-structure is very challenging for data we want to extract, the decision was to focus on 1, 2 & 3.

We experienced challenges with memory on our machines due to how much data had to be processed in many threads, which often led to stalling laptops, and eventually a crashed program.     

Føtex scraping gave us a challenge with 'Accepting Cookies' from time-to-time.
error message:
" .. bg-background"> is not clickable at point (999,658) because another element <div id="coiOverlay"> obscures it"
The problem was infrequent.


### Plotting
During the process, what needed to be plotted and how it should be plotted has changed. This meant that I (Caroline) have spent time plotting as pie charts and with multiple bar charts in one, but as the data I received from web scraping doesn't match well with how I imagined, those charts have been removed. 

I was particually proud of the multiple bar chart, which was instead of multiple bar charts for `show_price` and `show_price_per_100g`, but the products in our different stores aren't as similar as we had first expected, and therefore, I couldn't get the cereal data to fit in a single bar chart. 
  
I chose to remove the pie chart, which I had created to show the nutrional content in one specific cereal in percentage of daily nutrition, because it didn't have the decided effect. It created slices with percent values compared to the whole pie, which wasn't what I wanted. Instead a opted for a single bar chart. At the time it was created, the other bar charts were still with multiple colours, so it didn't look as similar as it does now.
  
I do think that the `pandas DataFrame` is the most visually appealing way of showing the nutritional content data.
