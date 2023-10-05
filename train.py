import os
import json
from concurrent.futures import ThreadPoolExecutor

from fastai.tabular.all import *
from fastai.collab import *


def add_channel_to_channels_json(channel_id, brands):
    if not os.path.exists("channels.json"):
        with open("channels.json", "x") as f:
            json.dump({}, f)
    with open("channels.json", "r+") as f:
        data = json.load(f)
        data[channel_id] = brands
        f.seek(0)
        json.dump(data, f)


def add_brand_to_brands_json(brand_domain, channels):
    if not os.path.exists("brands.json"):
        with open("brands.json", "x") as f:
            json.dump({}, f)
    with open("brands.json", "r+") as f:
        data = json.load(f)
        data[brand_domain] = channels
        f.seek(0)
        json.dump(data, f)


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


def get_channel_preds(channel_id):
    channel_brands_not_seen = [
        (channel_id, brand)
        for brand in all_brand_domains
        if ratings[
            (ratings["channel_id"] == channel_id) & (ratings["brand_domain"] == brand)
        ].empty
    ]
    channel_brands_not_seen_df = pd.DataFrame(
        channel_brands_not_seen, columns=["channel_id", "brand_domain"]
    )

    channel_brands_not_seen_dl = dls.test_dl(channel_brands_not_seen_df)
    preds, _ = dt_learner.get_preds(dl=channel_brands_not_seen_dl)

    # Show the channel brands not seen and predicted ratings
    channel_brands_not_seen_df["pred_rating"] = preds
    channel_brands_not_seen_df.sort_values("pred_rating", ascending=False, inplace=True)
    print(channel_brands_not_seen_df.head(10))
    return channel_brands_not_seen_df["brand_domain"].head(10).tolist()


def get_brand_preds(brand_domain):
    brand_channels_not_seen = [
        (channel, brand_domain)
        for channel in all_channel_ids
        if ratings[
            (ratings["channel_id"] == channel)
            & (ratings["brand_domain"] == brand_domain)
        ].empty
    ]
    brand_channels_not_seen_df = pd.DataFrame(
        brand_channels_not_seen, columns=["channel_id", "brand_domain"]
    )

    brand_channels_not_seen_dl = dls.test_dl(brand_channels_not_seen_df)
    preds, _ = dt_learner.get_preds(dl=brand_channels_not_seen_dl)

    # Show the brand channels not seen and predicted ratings
    brand_channels_not_seen_df["pred_rating"] = preds
    brand_channels_not_seen_df.sort_values("pred_rating", ascending=False, inplace=True)
    print(brand_channels_not_seen_df.head(10))
    return brand_channels_not_seen_df["channel_id"].head(10).tolist()


all_channel_ids = ratings["channel_id"].unique()[0:10]
all_brand_domains = ratings["brand_domain"].unique()
NUM_WORKERS = 4

channels_brands_dict = {}
with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    for channel_id, index in zip(all_channel_ids, range(len(all_channel_ids))):
        print("Channel:", channel_id, index + 1, "/", len(all_channel_ids))
        channels_brands_dict[channel_id] = executor.submit(
            get_channel_preds, channel_id
        )

    for channel_id, future in channels_brands_dict.items():
        brands = future.result()
        add_channel_to_channels_json(channel_id, brands)


brands_channels_dict = {}
with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    for brand_domain, index in zip(all_brand_domains, range(len(all_brand_domains))):
        print("Brand:", brand_domain, index + 1, "/", len(all_brand_domains))
        brands_channels_dict[brand_domain] = executor.submit(
            get_brand_preds, brand_domain
        )

    for brand_domain, future in brands_channels_dict.items():
        channels = future.result()
        add_brand_to_brands_json(brand_domain, channels)
