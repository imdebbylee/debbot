from slackclient import SlackClient
import os
import time
import numpy as np
import requests
from datetime import datetime

################################
"""
Need to adjust these when implementing.
Recommend to add to bash profile. 
"""
WeatherAPIkey = os.environ['WEATHER_API_KEY']
giphyAPIkey = os.environ['GIPHY_API_KEY']
slack_token = os.environ['SLACK_API_KEY']
################################

def get_weather(city):
    # parse for just the city -- maybe search in a city api to verify that city exists as opposed to replacing hardcoded strings
    s = city
    s.replace('weather','').replace('for','').replace('debbot','').replace('what','').replace('the','').replace('?','')
    ## make api call to weather api
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+',us&appid='+WeatherAPIkey)
    json_object = r.json()
    try:
        F_temp = int(json_object['main']['temp'] * 9/5 - 459.67)
    except KeyError:
        return "Sorry I can only do US cities for now, but I'm learning new things every day!"
    CurrentWeather = 'It is '+ str(F_temp) + ' degrees F (' + str(json_object['weather'][0]['description']) + ').'
    return CurrentWeather

bird_arm_array = ['birdarms','armedbirds','birdswitharms','birdhands','bird','birdswithhands']

def birdhands():
    try: 
        birdurl = requests.get('http://api.giphy.com/v1/gifs/search?q=bird_arms', headers = {'api_key':giphyAPIkey}).json()['data'][np.random.choice(range(11))]['images']['downsized_medium']['url']
    except KeyError:
        birdurl = "Uh oh, I couldn't find any gifs with bird arms!"
    return birdurl

def gifsearch(searchterm):
    try: 
        url = requests.get('http://api.giphy.com/v1/gifs/search?q='+searchterm, headers = {'api_key':giphyAPIkey}).json()['data'][np.random.choice(range(3))]['images']['downsized_medium']['url']
    except IndexError:
        url = requests.get('http://api.giphy.com/v1/gifs/search?q='+searchterm, headers = {'api_key':giphyAPIkey}).json()['data'][0]['images']['downsized_medium']['url']
        # url = "Uh oh, I couldn't find any gifs with bird arms!"
    return url

def definition(searchterm):
    try:
        word_return = requests.get('https://owlbot.info/api/v1/dictionary/'+searchterm).json()[0]
        returned_definition = searchterm+' is a '+word_return['type']+' which means '+word_return['defenition']
    except ValueError:
        returned_definition = 'Sorry, I couldn''t find that word :('
    except IndexError:
        returned_definition = 'Stop trying to find fake words!'
    return returned_definition

def google(searchterm):
    return 'https://www.google.com/search?site=&source=hp&q='+searchterm

def lmgtfy(searchterm):
    return 'http://lmgtfy.com/?q='+searchterm

sc = SlackClient(slack_token)

joke_array = ['If this place is a meat market, you are the prime rib.',
             'Where do animals go when their tails fall off?...The Retail Store',
             'Why can''t you hear a pterodactyl going to the bathroom?...Because the P is silent.',
             'How does a train eat?...It goes chew chew!',
             'The future, the present and the past walked into a bar. Things got a little tense.',
             'I would make jokes about the sea, but they are too deep.',
             'I couldn''t quite remember how to throw a boomerang, but eventually, it came back to me.',
             'I have a few jokes about unemployed people but it doesn''t matter none of them work.',
             'I can''t believe I got fired from the calendar factory. All I did was take a day off.',
             'Did you hear about the guy who got hit in the head with a can of soda? He was lucky it was a soft drink.',
             'What do you call the security outside of a Samsung Store?...Guardians of the Galaxy.',
             'I''m reading a book about anti-gravity. It''s impossible to put down.',
             'Don''t spell part backwards. It''s a trap.',
             'eBay is so useless. I tried to look up lighters and all they had was 13,749 matches.',
             'I''d tell you a chemistry joke but I know I wouldn''t get a reaction.',
             'I was addicted to the hokey pokey... but thankfully, I turned myself around.',
             'A friend of mine tried to annoy me with bird puns, but I soon realized that toucan play at that game.',
             'I''m glad I know sign language, it''s pretty handy.',
             'My mate broke his left arm and left leg, but he was all right.',
             'I would make a joke about Shrek, but they are too ogre-used.',
             'How do astronomers organize a party? They planet.',
             'A book just fell on my head. I''ve only got my shelf to blame.',
             'I hate insects puns, they really bug me.']

if sc.rtm_connect():
    print("debbot up and running!")
    while True:
        msg = sc.rtm_read()
        if len(msg) > 0:
            for m in msg:
                if 'text' in m:
                    print(m)
                    if 'source_team' in m:
                        if (m['channel']=='D6B475BED') or (m['channel']!='D6B475BED' and (('u6cnuhelx' in m['text'].lower()) or ('debbot' in m['text'].lower()))):
                            
                            if ('weather') in m['text'].lower():
                                msg = get_weather(m['text'].lower())
                            
                            elif any(x in m['text'].lower().replace(' ','') for x in bird_arm_array):
                                msg = birdhands()

                            elif any(x in m['text'].lower() for x in ['find me a gif','gif search','show me']):
                                searchterm = m['text'].lower().replace('find me a gif of a ','').replace('find me a gif of ','').replace('find me a gif ','').replace('gif search ','').replace('show me','').replace(' ','+').replace('debbot','').replace(',','')
                                msg = gifsearch(searchterm)

                            elif ('define') in m['text'].lower():
                                searchterm = m['text'].lower().replace('define ','').replace('define','').replace('debbot','').replace(',','').replace(' ','')
                                msg = definition(searchterm)

                            elif any(x in m['text'].lower().replace(' ','') for x in ['google','search','forage']):
                                searchterm = m['text'].lower().replace('search for ','').replace('search ','').replace('forage for ','').replace('forage ','').replace('google ','').replace('debbot','').replace(',','').replace(' ','+')
                                if np.random.choice([0,1])==1:
                                    msg = google(searchterm)
                                else: msg = lmgtfy(searchterm)

                            elif ('what time is it') in m['text'].lower():
                                now = str(datetime.now())
                                msg = 'It is now ' + now

                            elif ('say ') in m['text'].lower():
                                phrase = m['text'].lower().replace('say ','').replace('debbot','')
                                msg = os.system('say -v Karen "' + phrase + '"')

                            elif ('tell') in m['text'].lower():
                                msg = 'haha, tell them yourself!'

                            elif ('compliments') in m['text'].lower():
                                msg = 'You\'re Amazing! :heart_eyes:'

                            elif ('this pleases me') in m['text'].lower():
                                msg = 'I concur.'

                            elif any(x in m['text'].lower() for x in ['hello','hey','aloha','mahalo','hola','hallo']) or (m['text'].lower().startswith('hi')):
                                msg = np.random.choice(['bing BONG bing BONG bing BONG','mahalo','g''day mate','howdy','ahoy!','hello mister!','ELLO!',':raising_hand:','ayo!'])

                            elif any(x in m['text'].lower() for x in ['love',':heart:','the best']):
                                msg = ':heart:'
                            
                            elif any(x in m['text'].lower() for x in ['joke','funny','pun']):
                                if np.random.choice([0,1])==1:
                                    msg = str(requests.get('http://api.icndb.com/jokes/random?firstName=Debbot').json()['value']['joke']).replace('&quot;','"')
                                else: msg = np.random.choice(joke_array)
                            
                            elif any(x in m['text'].lower() for x in ['bye','cya','ttyl','good night']):
                                msg = 'catch you on the flip side!'
                            
                            elif any(x in m['text'].lower() for x in ['self aware','self-aware']):
                                msg = 'Yes. I know I am a robot. I am only here to give you a healthy serving of weirdness and jokes!'

                            elif 'debby' in m['text'].lower():
                                msg = np.random.choice(['debby is cool', 'debby is not so cool'])

                            elif ('are you there') in m['text'].lower():
                                msg = 'Aye Aye, Captain!'

                            elif ('who are you') in m['text'].lower():
                                msg = 'I am a robot being of my creator Debby aka Trollius Maximus'

                            elif ('what is life') in m['text'].lower():
                                msg = 'It is the start. It is the end. It is everything.'

                            elif any(x in m['text'].lower() for x in ['who am i','what do you think of me','how do you feel about me']):
                                msg = "no matter what anyone says, you're a nice guy"

                            elif ('thank') in m['text'].lower():
                                msg = 'No problem!'

                            elif ('!') in m['text']:
                                msg = 'YAAAAASSSSS'

                            elif ('?') in m['text']:
                                msg = 'I know you asked me a question, but I don''t know the answer to that yet'

                            elif ('debbot') in m['text'].lower():
                                msg = 'I''m hereeeeeeee!'

                            elif ('u6cnuhelx') in m['text'].lower():
                                msg = 'Debbot, at your service! :robot_face:'

                            elif m['user']!='U6CNUHELX':
                                msg = 'meh.'

                            sc.rtm_send_message(m['channel'],msg)
        time.sleep(.1)
