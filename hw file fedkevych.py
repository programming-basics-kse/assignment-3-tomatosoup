with open('Olympic Athletes - raw.tsv', encoding="utf-8") as f:
    lines = f.readlines()
columnnames = lines[0].strip().split("\t")
data = [dict(zip(columnnames, line.strip().split("\t"))) for line in lines[1:]]
def filter():
    country = input("Enter ur country or code: ").strip()
    year = input("Enter year: ").strip()
    year = str(year)
    got_medals = [{"Name": olimpian["Name"], "Event": olimpian["Event"], "Medal": olimpian["Medal"]}
        for olimpian in data
        if (olimpian["Team"].lower() == country.lower() or olimpian["NOC"].lower() == country.lower()) and olimpian["Year"] == year and olimpian["Medal"] != "NA" ]
    print("Top Medalists:")
    for olimpian in got_medals[:10]:
        print(f"{olimpian['Name']} - {olimpian['Event']} - {olimpian['Medal']}")
    number_of_medals_per_country = {"Gold": 0, "Silver": 0, "Bronze": 0}
    for olimpian in got_medals:
        number_of_medals_per_country[olimpian["Medal"]] += 1
    print(f"\nTotal number of medals for {country} in {year} = ", number_of_medals_per_country,)


# ця штука шукає найкращий рік (3 завдання короч) оберни в парсер пж :)



def best_games_of_country():
    country = input("Enter your country or code: ").strip()
    country_medals = [
        olimpian for olimpian in data
        if (olimpian["Team"].lower() == country.lower() or olimpian["NOC"].lower() == country.lower()) and olimpian["Medal"] != "NA"]
    medals_year_specific = {}
    for olimpian in country_medals:
        year = olimpian["Year"]
        medals_year_specific[year] = medals_year_specific.get(year, 0) + 1

    best_year = max(medals_year_specific, key=medals_year_specific.get)
    worst_year = min(medals_year_specific, key=medals_year_specific.get)
    least_medals = medals_year_specific[worst_year]
    most_medals = medals_year_specific[best_year]
    print(f"{country} - {best_year} - {most_medals} medals {worst_year} - {least_medals} medals ")
best_games_of_country()