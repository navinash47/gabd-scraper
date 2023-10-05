import os
import json
import pandas as pd
import itertools

from fastai.tabular.all import *
from fastai.collab import *


from google.colab import drive

drive.mount("/content/drive")


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


ratings = pd.read_csv(
    "c_bd.tsv",
    delimiter="\t",
    header=0,
    usecols=(0, 2, 3),
    names=["channel_id", "brand_domain", "deals_count"],
)
ratings["rating"] = ratings["deals_count"].apply(sigmoid)
ratings.head()


dls = CollabDataLoaders.from_df(
    ratings,
    user_name="channel_id",
    item_name="brand_domain",
    rating_name="rating",
    bs=64,
)


dt_learner = collab_learner(dls, n_factors=50, y_range=(0, 1))
dt_learner.lr_find()

for num_epochs in [5, 10, 20, 30]:
    print("#epochs:", num_epochs)
    dt_learner.fit_one_cycle(num_epochs, 3e-2, wd=0.1)


# Step 1: Generate all channel-brand pairs
unique_channels = ratings["channel_id"].unique()
unique_brands = ratings["brand_domain"].unique()
all_pairs = list(itertools.product(unique_channels, unique_brands))

# Step 2: Format as DataFrame
all_pairs_df = pd.DataFrame(all_pairs, columns=["channel_id", "brand_domain"])

# Step 3: Use DataLoader
all_dl = dls.test_dl(all_pairs_df)

# Step 4: Get predictions
predictions, _ = dt_learner.get_preds(dl=all_dl)

# Step 5: Attach predictions to DataFrame
all_pairs_df["predicted_rating"] = predictions.numpy().flatten()

print(all_pairs_df.head())

all_pairs_df.to_csv("/content/drive/My Drive/predicted_ratings.csv", index=False)
