with open('Olympic Athletes - raw.tsv', encoding="utf-8") as f:
    lines = f.readlines()

column_names = lines[0].strip().split('\t')

data = [dict(zip(column_names, line.strip().split("\t"))) for line in lines[1:]]

def filter():

    country = input("Enter ur country or code: ").strip()
    year = input("Enter ur year: ").strip()
    year = str(year)
    got_medals = [{"Name":olimpian["Name"], "Event": olimpian["Event"], "Medal": olimpian["Medal"]}

    for olimpian in data
        if (olimpian["Team"].lower() == country.lower() or olimpian["NOC"].lower() == country.lower()) and olimpian["Year"] == year and olimpian["Medal"]!= "NA" ]
    print(f"Medals from {country} in {year}")

    for olimpian in got_medals[:10]:
        print(f"{olimpian['Name']} - {olimpian['Event']} - {olimpian['Medal']}")


filter()
