# In this model, we attempt to use the 'blind assessment' data to classify the 'roast level'
# of the coffee using a bag of words and random forest.

from src.features.build_features import get_clean_dataset



df = get_clean_dataset()
