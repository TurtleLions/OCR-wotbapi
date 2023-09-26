def removeClanTag(player_names):
  player_list = []
  for player_name in player_names:
    leftBracketIndex = -1000
    rightBracketIndex = -1000
    leftFlag = False
    rightFlag = False
    try: 
      leftBracketIndex = player_name.index('[')
      leftFlag = True
    except ValueError: 
      print('no left bracket') 
      leftFlag = False
    try: 
      rightBracketIndex = player_name.index(']') 
      rightFlag = True
    except ValueError: 
      try: 
        rightBracketIndex = player_name.index('J') 
        rightFlag = True
      except ValueError:
        print('no right bracket') 
        rightFlag = False
    if leftFlag==rightFlag:
      if(leftBracketIndex==-1000 or rightBracketIndex==-1000):
        player_list.append(player_name)
      elif leftBracketIndex==0:
        player_list.append(player_name[rightBracketIndex+1:])
      else:
        player_list.append(player_name[:leftBracketIndex])
  return player_list
def intoList(text):
  text = text.replace(' ', '')
  text = text.replace('(','[')
  text = text.replace(')',']')
  text = text.replace('{','[')
  text = text.replace('}',']')
  player_names = text.split()
  return player_names