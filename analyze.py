# ------------------------------------------------------------------
# GemBet Project: Regulatory Strength Analysis
# ------------------------------------------------------------------
# What this script does:
# 1. Loads your operator dataset (the xlsx you filled in)
# 2. Converts a few text columns into simple numeric scores
# 3. Adds up those scores into one "regulatory_strength_score" per operator
# 4. Prints a summary table
# 5. Makes a bar chart comparing operators, colored by Regulated vs Offshore
# ------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load the data -----------------------------------------
# pandas reads the Excel file straight into a "DataFrame" (think: a table)
df = pd.read_excel("GemBet_Operator_Dataset_CLEANED.xlsx", sheet_name="Operator Dataset")

print("Columns in your dataset:")
print(df.columns.tolist())
print()

# --- Step 2: Turn text answers into 0/1 points ----------------------
# We can't do math on text like "TRUE" or "Partial" directly, so we
# write small helper functions that read the text and return a score.

def score_rtp_disclosed(value):
    text = str(value).strip().upper()
    if text == "TRUE":
        return 1
    return 0  # FALSE, "Not disclosed", "Not checked" all count as 0

def score_independent_audit(value):
    text = str(value).strip().upper()
    if text == "TRUE":
        return 1
    if text == "PARTIAL":
        return 0.5  # partial credit, e.g. Provably Fair crypto checks
    return 0

def score_dispute_mechanism(value):
    text = str(value).strip().lower()
    # if the cell mentions a named, real dispute body, give a point
    if "none" in text or text in ("nan", ""):
        return 0
    return 1

# Apply each function to its column. This creates 3 new columns of scores.
df["score_rtp"] = df["rtp_disclosed"].apply(score_rtp_disclosed)
df["score_audit"] = df["independent_audit"].apply(score_independent_audit)
df["score_dispute"] = df["dispute_mechanism"].apply(score_dispute_mechanism)

# --- Step 3: Combine into one overall score --------------------------
# Simple approach: add the three scores together (max possible = 3)
df["regulatory_strength_score"] = (
    df["score_rtp"] + df["score_audit"] + df["score_dispute"]
)

# --- Step 4: Print a clean summary table -----------------------------
summary = df[[
    "operator_name", "category", "score_rtp", "score_audit",
    "score_dispute", "regulatory_strength_score"
]].sort_values("regulatory_strength_score", ascending=False)

print("Regulatory Strength Summary:")
print(summary.to_string(index=False))
print()

# Average score by category (Regulated vs Offshore) -- this is the
# headline stat for your thesis
avg_by_category = df.groupby("category")["regulatory_strength_score"].mean()
print("Average regulatory strength score by category:")
print(avg_by_category)
print()

# --- Step 5: Make a bar chart -----------------------------------------
colors = df["category"].map({"Regulated": "#2E7D32", "Offshore": "#C62828"})

plt.figure(figsize=(9, 5.5))
bars = plt.bar(df["operator_name"], df["regulatory_strength_score"], color=colors)

plt.title("Regulatory Strength Score by Operator", fontsize=14, fontweight="bold")
plt.ylabel("Score (0-3): RTP disclosure + Independent audit + Dispute mechanism")
plt.xticks(rotation=30, ha="right")
plt.ylim(0, 3.5)

# Add the score number on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05,
              f"{height:.1f}", ha="center", fontsize=9)

# Manual legend since color = category
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2E7D32", label="Regulated"),
    Patch(facecolor="#C62828", label="Offshore"),
]
plt.legend(handles=legend_elements)

plt.tight_layout()
plt.savefig("regulatory_strength_chart.png", dpi=150)
print("Saved chart to regulatory_strength_chart.png")
