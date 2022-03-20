import discum, json
import requests, time
from io import BytesIO
from discum.utils.button import Buttoner
from discord import Webhook, RequestsWebhookAdapter
from PIL import Image
from pytesseract import image_to_string
import re
from list import test_list

webhook_url = ""
token0      = "" 
token1      = "" 
token2      = ""
token3      = "" 

reactions = ["1️⃣", "2️⃣", "3️⃣"]

bot  = discum.Client(token=token0, log={"console":False, "file":False})
bot1 = discum.Client(token=token1, log={"console":False, "file":False})
bot2 = discum.Client(token=token2, log={"console":False, "file":False})
bot3 = discum.Client(token=token3, log={"console":False, "file":False})
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

def butt(guildID, channelID, messageID, num):
  message = bot.getMessage(channelID, messageID)
  data = message.json()[0]
  buts = Buttoner(data["components"])
  print("trying to click")
  bot.click(
      data["author"]["id"],
      channelID=data["channel_id"],
      guildID=guildID,
      messageID=data["id"],
      messageFlags=data["flags"],
      data = buts.getButton(row=0, column=num-1),
  )
  try:
      bot1.click(
          data["author"]["id"],
          channelID=data["channel_id"],
          guildID=guildID,
          messageID=data["id"],
          messageFlags=data["flags"],
          data = buts.getButton(row=0, column=num-1),
      )
      bot2.click(
          data["author"]["id"],
          channelID=data["channel_id"],
          guildID=guildID,
          messageID=data["id"],
          messageFlags=data["flags"],
          data = buts.getButton(row=0, column=num-1),
      )
      bot3.click(
          data["author"]["id"],
          channelID=data["channel_id"],
          guildID=guildID,
          messageID=data["id"],
          messageFlags=data["flags"],
          data = buts.getButton(row=0, column=num-1),
      )
  except:
    print("All Didnt Click")
  print("clicked")

def add_reaction(channel, ID, reaction, e):
        response = json.loads(bot.getMessage(channel, ID).content)
        msgresp = response[0]['reactions'][e]['emoji']['name']
        bot.addReaction(str(channel), str(ID), reaction)
        try:
            bot1.addReaction(str(channel), str(ID), reaction)
            bot2.addReaction(str(channel), str(ID), reaction)
            bot3.addReaction(str(channel), str(ID), reaction)
        except:
            print("All Didnt React")
        print("Reaction Added")


def chop(url):
  response = requests.get(url)
  im = Image.open(BytesIO(response.content))
  im1 = im.crop((336-280,61,498-270,102))
  im2 = im.crop((336,61,498,102))
  im3 = im.crop((336+270,61,498+277,102))
  try:
    test_string1 = str((re.sub(r'[^A-Za-z0-9 ]+', '', image_to_string(im1))))
    test_string2 = str((re.sub(r'[^A-Za-z0-9 ]+', '', image_to_string(im2))))
    test_string3 = str((re.sub(r'[^A-Za-z0-9 ]+', '', image_to_string(im3))))


  except:
    print("Error recognizing")

  if bool([ele for ele in test_list if (ele in test_string1)]) == True:
    print(1)
    return 1

  elif bool([ele for ele in test_list if (ele in test_string2)]) == True:
    print(2)
    return 2


  elif bool([ele for ele in test_list if (ele in test_string3)]) == True:
    print(3)
    return 3

  else:
    return 0

@bot.gateway.command
def helloworld(resp):
    if resp.event.ready_supplemental:
        bot.gateway.subscribeToGuildEvents(wait=1)
    if resp.event.message:
        resp = json.loads(json.dumps(resp.raw))
        msg_content = str(resp['d']['content'])
        channel_id = str(resp['d']['channel_id'])
        guild = str(resp['d']['guild_id'])
        ID =  str(resp['d']['id'])
        if "dropping 3" in msg_content:
            url = resp['d']['attachments'][0]['url']
            ocr_val = chop(url)
            if ocr_val == 0:
                print(f"No interesting card found in {channel_id}")
            else:            
                react = reactions[ocr_val-1]
                cont = True
                for i in range(100):
                    try:
                        if cont == True:
                            for w in range(30):
                                butt(guild, channel_id, ID, ocr_val)
                                cont = False
                                time.sleep(0.2)
                                print(w)
                    except:
                        try:
                            if cont == True:
                                add_reaction(channel_id, ID, react, ocr_val-1)
                                cont = False
                        except:
                            print(f"Card Not Found :: {i}")               
                with open('Good_Cards.txt', 'a') as the_file:
                    the_file.write(f'https://discord.com/channels/{guild}/{channel_id}/{ID}\n')
                webhook.send(f'https://discord.com/channels/{guild}/{channel_id}/{ID}')

bot.gateway.run(auto_reconnect=True)