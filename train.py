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

for num_epochs in [5, 5]:
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

# all_pairs_df.to_csv("/content/drive/My Drive/predicted_ratings.csv", index=False)

# Top 10 ratings for each channel
top_10_brands_per_channel = (
    all_pairs_df.groupby("channel_id")
    .apply(lambda x: x.nlargest(10, "predicted_rating"))
    .reset_index(drop=True)
)
top_10_brands_per_channel.to_csv(
    "/content/drive/My Drive/top_10_brands_per_channel.csv", index=False
)

# Top 10 channels for each brand
top_10_channels_per_brand = (
    all_pairs_df.groupby("brand_domain")
    .apply(lambda x: x.nlargest(10, "predicted_rating"))
    .reset_index(drop=True)
)
top_10_channels_per_brand.to_csv(
    "/content/drive/My Drive/top_10_channels_per_brand.csv", index=False
)
