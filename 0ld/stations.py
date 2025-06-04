import pandas as pd

df = pd.read_csv("isd-history.csv")
df["USAF"] = df["USAF"].astype(str).str.zfill(6)
df["WBAN"] = df["WBAN"].astype(str).str.zfill(5)

stations_fr = df[
    (df["CTRY"] == "FR") &
    (df["WBAN"] != "99999") &
    (df["USAF"] != "999999")
]

print(f"{len(stations_fr)} stations NOAA valides trouvées en France.")
print(stations_fr[["STATION NAME", "USAF", "WBAN", "LAT", "LON"]].sort_values("LAT"))
