# YouTuber with most brand deals with a brand
# Import Pandas library
import pandas as pd

# Load the TSV file into a Pandas DataFrame
file_path = "c_bd.tsv"
df = pd.read_csv(file_path, sep="\t")

# Group the data by 'brand_domain' and 'channel_title', summing the 'deals_count'
grouped_df = (
    df.groupby(["brand_domain", "channel_title"])
    .agg({"deals_count": "sum"})
    .reset_index()
)

# Find the channel_title with the maximum deals_count for each brand_domain
max_deals_df = grouped_df.loc[
    grouped_df.groupby("brand_domain")["deals_count"].idxmax()
]

# Sort the DataFrame by 'deals_count' in descending order
max_deals_df = max_deals_df.sort_values(by="deals_count", ascending=False)

# Create a tsv file with the results
print(max_deals_df.head())
max_deals_df.to_csv("charts/results/brand_ytr.tsv", sep="\t", index=False)
