import requests
# pip install requests
from bs4 import BeautifulSoup
# pip install beautifulsoup4
# pip install lxml
import csv



# import le page de site web pour scrap 
date=input("donne le date de matches en forme si mm/dd/yyyy: ")
page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}")

def main(page):
  # edit  content en xml content for beautifulsoup 
  src=page.content
  soup= BeautifulSoup(src,'lxml')
  
  # create variable for stock data of matches
  matches_details=[]
  
  # data of championship div
  championships=soup.find_all("div",{'class':'matchCard'})
  
  # get all matches de championships
  def get_match_info(championships):
    # get first championships title 
    championship_title=championships.contents[1].find('h2').text.strip()
    # get all matches 
    all_matches=championships.contents[3].find_all('div',{"class":"item"})
    # number de matches 
    numbers_matches=len(all_matches)
    
    for i in range(numbers_matches):
      # get first equips  team_A
      team_A=all_matches[i].find("div",{"class":"teamA"}).find("p").text.strip()
      # get second equips  team_B
      
      team_B=all_matches[i].find("div",{"class":"teamB"}).find("p").text.strip()
      #get score of the matches 
      match_result=all_matches[i].find("div",{"class":"MResult"}).find_all('span',{'class':'score'})
      score=f"{match_result[0].text.strip()}-{match_result[1].text.strip()}"
      
      # get time of match 
      match_time=all_matches[i].find("div",{"class":"MResult"}).find('span',{'class':'time'}).text.strip()
      
      # add match info to matches_details
      matches_details.append({  "championship": championship_title, "team_A": team_A,    "team_B": team_B, "time_of_match": match_time,"result_of_match": score})

      
      

  for  i in range(len(championships)):
    get_match_info(championships[i])
    
    
  # stock le donner de matches en csv file 
    keys = matches_details[0].keys()
    with open('matches_details.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print('File created successfully.')
    
    
    
  
  
  
  
  
  
main(page) 