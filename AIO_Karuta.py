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
reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]

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
    except:
        print(1)
    try:
        bot2.click(
          data["author"]["id"],
          channelID=data["channel_id"],
          guildID=guildID,
          messageID=data["id"],
          messageFlags=data["flags"],
          data = buts.getButton(row=0, column=num-1),
        )
    except:
        print(2)
    try:
        bot3.click(
          data["author"]["id"],
          channelID=data["channel_id"],
          guildID=guildID,
          messageID=data["id"],
          messageFlags=data["flags"],
          data = buts.getButton(row=0, column=num-1),
        )
    except:
        print(3)
    print("clicked")

def add_reaction(channel, ID, reaction, e):
        response = json.loads(bot.getMessage(channel, ID).content)
        msgresp = response[0]['reactions'][e]['emoji']['name']
        bot.addReaction(str(channel), str(ID), reaction)
        try:
            bot1.addReaction(str(channel), str(ID), reaction)
        except:
            print(1)
        try:
            bot2.addReaction(str(channel), str(ID), reaction)
        except:
            print(2)
        try:
            bot3.addReaction(str(channel), str(ID), reaction)
        except:
            print(3)
        print("Reaction Added")

def chop(url, CardCount):
  test_string4 = ""
  response = requests.get(url)
  im = Image.open(BytesIO(response.content))
  if   CardCount == 3:
    im1 = im.crop((336-280,61,498-270,102))
    im2 = im.crop((336,61,498,102))
    im3 = im.crop((336+270,61,498+277,102))

  elif CardCount == 4:
    im1 = im.crop((59+(274*0),62,227+(274*0),103))
    im2 = im.crop((59+(274*1),62,227+(274*1),103))
    im3 = im.crop((59+(274*2),62,227+(274*2),103))
    im4 = im.crop((59+(274*3),62,227+(274*3),103))

  try:
    test_string1 = str((re.sub(r'[^A-Za-z0-9 ]+', '', image_to_string(im1))))
    test_string2 = str((re.sub(r'[^A-Za-z0-9 ]+', '', image_to_string(im2))))
    test_string3 = str((re.sub(r'[^A-Za-z0-9 ]+', '', image_to_string(im3))))
    if CardCount == 3:
        print(f"{test_string1}\n{test_string2}\n{test_string3}")
    if CardCount == 4:
        test_string4 = str((re.sub(r'[^A-Za-z0-9 ]+', '', image_to_string(im4))))
        print(f"{test_string1}\n{test_string2}\n{test_string3}\n{test_string4}")


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

  elif bool([ele for ele in test_list if (ele in test_string4)]) == True:
    print(4)
    return 4

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
        if "dropping 3 cards since" in msg_content or "dropping 4 cards since" in msg_content:
            if "3" in msg_content:
                CardCount = 3
            elif "4" in msg_content:
                CardCount = 4
            url = resp['d']['attachments'][0]['url']
            ocr_val = chop(url, CardCount)
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
