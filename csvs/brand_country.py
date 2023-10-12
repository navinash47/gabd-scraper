import pandas as pd

# Load the TSV file into a DataFrame
file_path = "c_bd.tsv"
df = pd.read_csv(file_path, sep="\t")

# Display the first few rows to understand the structure
df.head()

# Group the data by brand and country, summing up the deals_count
grouped_df = (
    df.groupby(["brand_domain", "country"]).agg({"deals_count": "sum"}).reset_index()
)

# Identify the country with the maximum number of deals for each brand
max_deals_df = grouped_df.loc[
    grouped_df.groupby("brand_domain")["deals_count"].idxmax()
]

# Sort the DataFrame by country first, then by deals_count
max_deals_df = max_deals_df.sort_values(["country", "deals_count"], ascending=False)

# Show first few rows of the resulting DataFrame
print(max_deals_df.head())


# Save the result to a TSV file
output_path = "charts/results/brand_country.tsv"
max_deals_df.to_csv(output_path, sep="\t", index=False)
