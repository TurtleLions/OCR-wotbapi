import requests
import keys

def player_search(player_name):
  # API endpoint for player statistics
  api_url = 'https://api.wotblitz.com/wotb/account/list/'
  # Parameters for the API request
  params = {
      'application_id': keys.application_id,
      'search': player_name,
  }
  
  # Make the API request
  response = requests.get(api_url, params=params)
  if response.status_code == 200:
    responsejson = response.json()
    try:
      if responsejson['meta']['count'] != 0:
        account_id = responsejson['data'][0]['account_id']
        print(player_name)
        return account_id
      else:
        print("fail")
        print(player_name)
    except KeyError:
      print("fail")
      print(player_name)
    
def stats_search(account_ids):
  api_url = 'https://api.wotblitz.com/wotb/account/info/'
  accountstr = ""
  for account_id in account_ids:
    accountstr = accountstr+str(account_id)+','
  params = {
      'application_id': keys.application_id,
      'account_id': accountstr,
  }
  response = requests.get(api_url, params=params)
  winrate = []
  spotspergame = []
  damageratio = []
  killdeathratio = []
  if response.status_code==200:
    responsejson = response.json()
    for account_id in account_ids:
      winrate.append(responsejson['data'][str(account_id)]['statistics']['all']['wins']/responsejson['data'][str(account_id)]['statistics']['all']['battles'])
      spotspergame.append(responsejson['data'][str(account_id)]['statistics']['all']['spotted']/responsejson['data'][str(account_id)]['statistics']['all']['battles'])
      damageratio.append(responsejson['data'][str(account_id)]['statistics']['all']['damage_dealt']/responsejson['data'][str(account_id)]['statistics']['all']['damage_received'])
      killdeathratio.append(responsejson['data'][str(account_id)]['statistics']['all']['frags']/(responsejson['data'][str(account_id)]['statistics']['all']['battles']-responsejson['data'][str(account_id)]['statistics']['all']['survived_battles']))
  else:
      print(f"API Error: {response.status_code}")
  return dict(winrate = winrate, spotspergame = spotspergame, damageratio = damageratio, killdeathratio = killdeathratio)

def parseStats(stats):
  averages = dict()
  averages['winrate'] = round(findAverage(stats['winrate'])*100,2)
  averages['spotspergame'] = round(findAverage(stats['spotspergame']),3)
  averages['damageratio'] = round(findAverage(stats['damageratio']),3)
  averages['killdeathratio'] = round(findAverage(stats['killdeathratio']),3)
  return averages
def findAverage(inputArray):
  sum = 0
  for input in inputArray:
    sum+=input
  return sum/len(inputArray)
def wrapper(player_names):
  account_ids = []
  for player_name in player_names:
    account_ids.append(player_search(player_name))
  account_ids = list(filter(lambda item: item is not None, account_ids))
  stats = stats_search(account_ids)
  print(len(stats['winrate']))
  averages = parseStats(stats)
  return averages