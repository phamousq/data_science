import seaborn as sns
import polars as pl

df = pl.read_csv(
    "741109643_dell-seton-medical-center-at-univ-of-texas_standardcharges.csv",
    # encoding="latin-1",
    skip_rows=2,
    ignore_errors=True,
)
# I don't understand why some values have null and others don't, we are including the following columns which I think are interesting.
# discounted cash is the price you will be charged if you don't have insurance
# gross is the number that presents as the charge to the hospital before any discounts
# negotiated dollar is the dollar amount that the hospital has negotiated with current insurance companies (the payer listed)


dd = (
    df.select(
        [
            "description",
            "standard_charge|discounted_cash",
            "standard_charge|gross",
            "standard_charge|negotiated_dollar",
            "payer_name",
            "standard_charge|min",
            "standard_charge|max",
        ]
    )
    .unique(subset=["description"])
    .drop_nulls()  # drops the first occurance of null
)

dd = dd.with_columns(
    (dd["standard_charge|max"] - dd["standard_charge|min"]).alias(
        "standard_charge|difference"
    )
)

dd.sort("standard_charge|discounted_cash")
# shows the discrepancy in "good" vs "bad" insurance plans
dd.sort("standard_charge|difference")

dd.head()
sns.scatterplot(data=dd, x="standard_charge|discounted_cash", y="standard_charge|gross")
# The 1:1 line here shows that the discount for cash payers is constant across all of the different items that can be billed for. We can also see from this that there are many charges that cost around 50k or less relative to the outliers above 50k.
print(
    round(
        1 - df[1, "standard_charge|discounted_cash"] / df[1, "standard_charge|gross"], 2
    )
)  # this is the discount rate; almost 62%

sns.scatterplot(
    data=dd, x="standard_charge|negotiated_dollar", y="standard_charge|gross"
)
# this graph in comparison shows that
