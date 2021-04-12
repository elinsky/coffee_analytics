import os

interim_data_dir = os.path.dirname(__file__)
interim_data_dir = os.path.dirname(interim_data_dir)
interim_data_dir = os.path.dirname(interim_data_dir)
interim_data_dir = os.path.dirname(interim_data_dir)
interim_data_dir += '/data/interim/ratings.jl'


os.system('scrapy crawl coffee_ratings_spider -o ' + interim_data_dir)

print('\nJSON lines written to ratings.jl\n')