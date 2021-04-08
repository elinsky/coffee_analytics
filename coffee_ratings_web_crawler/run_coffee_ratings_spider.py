import os

# make directory for storing raw HTML data
page_dirname = 'raw_coffee_data'
if not os.path.exists(page_dirname):
    os.makedirs(page_dirname)

os.system('scrapy crawl coffee_ratings_spider -o ratings.jl')
print('\nJSON lines written to ratings.jl\n')