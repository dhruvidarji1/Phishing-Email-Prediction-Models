import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("hf://datasets/simlab-vs/meajor_cleaned_preprocessed/data/train-00000-of-00001.parquet")

# url_count, url_length_max, sender_domain, subject, body, attachment_count

features = ["url_count", "url_length_max", "sender_domain", "subject", "body", "attachment_count", "label"]
modfeatures = ["url_count", "url_length_max", "sender_domain_length", "subject_length", "body_length", "attachment_count", "label"]

fdf = df[features]
fdf["subject_length"] = fdf["subject"].str.len()
fdf["sender_domain_length"] = fdf["sender_domain"].str.len()
fdf["body_length"] = fdf["body"].str.len()

df_ham = fdf[fdf['label'] == 0]
df_spam = fdf[fdf['label'] == 1]

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3, figsize=(4, 7))

def vplot(ax, feature):
    ax.violinplot([df_ham[feature], df_spam[feature]], quantiles=[[0.25, 0.5, 0.75], [0.25, 0.5, 0.75]])
    ax.yaxis.grid(True)
    ax.set_xticks([1, 2], labels=["Not spam", "Spam"])
    ax.set_title(feature)
    if "length" in feature:
        ax.set_ylabel("# characters")

for (i, ax) in enumerate([ax1, ax2, ax3, ax4, ax5, ax6]):
    vplot(ax, modfeatures[i])

plt.show()