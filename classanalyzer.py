class OlympicsAnalyzer:
    def __init__(self, data):
        self.data = data

    def filter(self, country, year, output=None):
        got_medals = [
            {"Name": olimpian["Name"], "Event": olimpian["Event"], "Medal": olimpian["Medal"]}
            for olimpian in self.data
            if (olimpian["Team"].lower() == country.lower() or olimpian["NOC"].lower() == country.lower())
            and olimpian["Year"] == year
            and olimpian["Medal"] != "NA"
        ]
        if not got_medals:
            print(f"No medalists found for {country} in {year}")
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(f"No medalists found for {country} in {year}.\n")
            return

        print("First 10 medalists:")
        results = []
        for olimpian in got_medals[:10]:
            result_line = f"{olimpian['Name']} - {olimpian['Event']} - {olimpian['Medal']}"
            results.append(result_line)
            print(result_line)

        number_of_medals_per_country = {"Gold": 0, "Silver": 0, "Bronze": 0}
        for olimpian in got_medals:
            number_of_medals_per_country[olimpian["Medal"]] += 1

        summary_line = f"\nTotal number of medals for {country} in {year} = {number_of_medals_per_country}"
        print(summary_line)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                for line in results:
                    f.write(line + "\n")
                f.write(summary_line + "\n")

    def total(self, year, output=None):
        medals_by_country = {}
        for olimpian in self.data:
            if olimpian["Year"] == year and olimpian["Medal"] != "NA":
                country = olimpian["Team"]
                if country not in medals_by_country:
                    medals_by_country[country] = {"Gold": 0, "Silver": 0, "Bronze": 0}
                medals_by_country[country][olimpian["Medal"]] += 1

        if not medals_by_country:
            print(f"No medals were awarded in {year}.")
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(f"No medals were awarded in {year}.\n")
            return

        print(f"Medals summary for {year}:")
        for country, medals in medals_by_country.items():
            print(f"{country} - Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}")

        if output:
            with open(output, "w", encoding="utf-8") as f:
                for country, medals in medals_by_country.items():
                    f.write(f"{country} - Gold: {medals['Gold']}, Silver: {medals['Silver']}, Bronze: {medals['Bronze']}\n")

    def best_games_of_country(self, country):
        medals_year_specific = {}
        country_medals = [
            olimpian for olimpian in self.data
            if ((olimpian["Team"] and olimpian["Team"].lower() == country.lower())
                or (olimpian["NOC"] and olimpian["NOC"].lower() == country.lower()))
            and olimpian["Medal"] != "NA"
        ]
        if not country_medals:
            print(f"No medals found for {country}.")
            return

        for olimpian in country_medals:
            year = olimpian["Year"]
            medals_year_specific[year] = medals_year_specific.get(year, 0) + 1

        best_year = max(medals_year_specific, key=medals_year_specific.get)
        worst_year = min(medals_year_specific, key=medals_year_specific.get)

        print(f"{country} - Best Year: {best_year} - {medals_year_specific[best_year]} medals")
        print(f"{country} - Worst Year: {worst_year} - {medals_year_specific[worst_year]} medals")

    def analyze_overall(self, countries):
        for country in countries:
            self.best_games_of_country(country)

    def interactive_mode(self):
        while True:
            country = input("Enter a country (or type 'exit' to quit): ").strip()
            if country.lower() == "exit":
                print("Exiting interactive mode.")
                break
            self.best_games_of_country(country)