from csv_diff import load_csv, compare


diff = compare(
    load_csv(open("2020-02-28.csv")),
    load_csv(open("caca_ter.csv"))
)

print(len(diff))