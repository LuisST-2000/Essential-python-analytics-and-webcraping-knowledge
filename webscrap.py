from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


# Configurar Selenium
##chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
s = Service("/usr/local/chromedriver")  #Route to ChromeDriver
driver = webdriver.Chrome(service=s)

#Gets the historical data of the player entered.
def get_player_data_history(url_player):
    url_player = url_player.replace('Show','History')
    driver.get(url_player)

    # Find elements in table 
    table = driver.find_element(By.ID, "player-tournament-stats")
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Assign variables to store extracted data
    seasons = []
    teams = []
    matchs = []
    matchs_played = []
    minutes = []
    goals = []
    assists = []
    ratings = []

    # Extract data from tables
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 16:
            season = cells[0].text
            team = cells[1].text
            match = cells[4].text
            match_played = cells[5].text
            minute = cells[6].text
            goal = cells[7].text
            assist = cells[8].text
            rating = cells[15].text


        seasons.append(season)
        teams.append(team)
        matchs.append(match)
        matchs_played.append(match_played)
        minutes.append(minute)
        goals.append(goal)
        assists.append(assist)
        ratings.append(rating)

    data = {
    'Season' : seasons,
    'Team' : teams,
    'Match': matchs,
    'Match_Played': matchs_played,
    'Minutes': minutes,
    'Goals': goals,
    'Assists': assists,
    'Rating': ratings}

    # Create a DataFrame with the collected data

    df = pd.DataFrame(data)
    print(df)

    df.to_csv('datos-estadicticos.csv',sep=';',index=False)

        
# Gets the players and their links, then stores them in lists.
def player_and_link(entry):

    # Navigate to the website
    url = 'https://es.whoscored.com/Search/?t='+entry
    driver.get(url)

    # Wait for the page to load 
    driver.implicitly_wait(10)

    #driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()

    try:
    # Find all link elements that contain players
        table = driver.find_element(By.CLASS_NAME, "search-result")
        rows = table.find_elements(By.TAG_NAME, "tr")

        players = []
        links = []

        for row in rows[1:]:
            # Searches for the first element it finds with the css_selector
            cell = row.find_element(By.TAG_NAME, 'a')
            name_player = cell.text

            # Calls the variable containing the first parameter and gets the href attribute
            url_player = cell.get_attribute('href')

            players.append(name_player.upper())
            links.append(url_player)

        data = {'Players':players,
                'Links':links}
        
    except NoSuchElementException:
        print('This player no exist \n')
        data = False

    return data


#Valid player selection if multiple players are found. 
def get_player_url(player_name):
    #calls function player_and_link(entry) and stores in a variable
    player_entered = player_and_link(player_name)

    #Returns false if player not found 
    if player_entered == False:
        url_got = False
    
    else:
        #We convert the data of the player_entered variable into a DataFrame.
        df = pd.DataFrame(player_entered)
        #Prints the players found as options for selection
        print(df.to_string())

        #Check if there are more than 2 players with the same name.        
        if len(player_entered['Players']) >= 2:
            print("There are several players with this name, write and be more specific or type one of the numbers: ")
            opcion = input('Type name / Digit number:')

            if opcion.isnumeric():
                opcion = int(opcion)
                player_got = player_entered['Players'][opcion]
                url_got = player_entered['Links'][opcion]

            else:
                opcion = opcion.upper()
                for name in player_entered['Players']:
                    if opcion in name:
                        index = player_entered['Players'].index(name)
                        player_got = player_entered['Players'][index]
                        url_got = player_entered['Links'][index]

    return url_got


name_player = input('Enter player name: ').upper()
url_player = get_player_url(name_player)
print(url_player)
history_player = get_player_data_history(url_player)
print(history_player)
