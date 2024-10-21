# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import time
# import os

# # Scrape the latest data
# def scrape():
#     # Define the target URL
#     standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

#     # Check if 'matches.csv' exists
#     if os.path.exists("matches.csv"):
#         existing_data = pd.read_csv("matches.csv")
#         existing_dates = set(existing_data["date"])
#     else:
#         existing_data = pd.DataFrame()
#         existing_dates = set()

#     # Helper function to extract team URLs
#     def get_team_urls(soup):
#         standings_table = soup.select('table.stats_table')[0]
#         links = [l.get("href") for l in standings_table.find_all('a') if '/squads/' in l]
#         return [f"https://fbref.com{l}" for l in links]

#     # Scrape the latest matches
#     def scrape_latest_matches():
#         all_matches = []

#         # Fetch the current standings page
#         data = requests.get(standings_url)
#         soup = BeautifulSoup(data.text, 'html.parser')

#         # Get team URLs
#         team_urls = get_team_urls(soup)

#         # Loop through each team to get matches
#         for team_url in team_urls:
#             team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
#             print(f"Fetching data for {team_name}...")

#             # Fetch team page and parse matches
#             data = requests.get(team_url)
#             matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
#             soup = BeautifulSoup(data.text, 'html.parser')

#             # Get the shooting stats URL
#             links = [l.get("href") for l in soup.find_all('a') if 'all_comps/shooting/' in l]
#             if not links:
#                 continue  # Skip if no shooting data found

#             # Fetch shooting stats
#             shooting_data = requests.get(f"https://fbref.com{links[0]}")
#             shooting = pd.read_html(shooting_data.text, match="Shooting")[0]
#             shooting.columns = shooting.columns.droplevel()

#             # Merge matches and shooting data
#             try:
#                 team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
#             except ValueError:
#                 continue

#             # Filter Premier League matches and check for new data
#             team_data = team_data[team_data["Comp"] == "Premier League"]
#             team_data["Team"] = team_name
#             team_data["Season"] = 2024  # Update the current season if needed

#             # Filter only new matches based on the date
#             new_matches = team_data[~team_data["Date"].isin(existing_dates)]
#             all_matches.append(new_matches)

#             time.sleep(7)  # Be respectful to the website

#         if all_matches:
#             # Concatenate new matches and save to CSV
#             new_data = pd.concat(all_matches)
#             updated_data = pd.concat([existing_data, new_data])
#             updated_data.to_csv("matches.csv", index=False)
#             print("New matches added successfully!")
#         else:
#             print("No new matches found.")
#         pass
    
#     # Run the scraping function
#     scrape_latest_matches()

# # Update the CSV
# if __name__ == "__main__":
#     scrape()
