from fastai.tabular.all import *
from fastai.collab import *


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

single_channel = ratings["channel_id"].unique()[0]
total_brands = ratings["brand_domain"].unique()

channel_brands_not_seen = [
    (single_channel, brand)
    for brand in total_brands
    if ratings[
        (ratings["channel_id"] == single_channel) & (ratings["brand_domain"] == brand)
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
channel_brands_not_seen_df.head(10)
