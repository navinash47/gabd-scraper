from fastai.tabular.all import *
from fastai.collab import *


path = untar_data(URLs.ML_100k)

ratings = pd.read_csv(
    path / "u.data",
    delimiter="\t",
    header=None,
    usecols=(0, 1, 2),
    names=["user", "movie", "rating"],
)
ratings.head()


movies = pd.read_csv(
    path / "u.item",
    delimiter="|",
    encoding="latin-1",
    usecols=(0, 1),
    names=("movie", "title"),
    header=None,
)
movies.head()


ratings = ratings.merge(movies)
ratings.head()


dls = CollabDataLoaders.from_df(ratings, item_name="title", bs=64)


dt_learner = collab_learner(dls, n_factors=50, y_range=(0.5, 5.5))
dt_learner.lr_find()

for num_epochs in [5, 10, 20, 30]:
    print("#epochs:", num_epochs)
    dt_learner.fit_one_cycle(num_epochs, 3e-2, wd=0.1)

single_user = ratings["user"].unique()[0]
total_movies = ratings["movie"].unique()

user_movies_not_seen = [
    (single_user, movie)
    for movie in total_movies
    if ratings[(ratings["user"] == single_user) & (ratings["movie"] == movie)].empty
]
user_movies_not_seen_df = pd.DataFrame(user_movies_not_seen, columns=["user", "movie"])
user_movies_not_seen_df = user_movies_not_seen_df.merge(movies, on="movie", how="left")

user_movies_not_seen_dl = dls.test_dl(user_movies_not_seen_df)
preds, _ = dt_learner.get_preds(dl=user_movies_not_seen_dl)

# Show the user movies not seen and predicted ratings
user_movies_not_seen_df["pred_rating"] = preds
user_movies_not_seen_df.sort_values("pred_rating", ascending=False, inplace=True)
user_movies_not_seen_df.head(10)
