#Imports for discord bot. Google Calendar Notifcation Bot
#https://discord.com/oauth2/authorize?client_id=1233444920912773192&permissions=2147944448&scope=bot

#Discord API manager
import discord
from discord import Embed
from discord.ext import commands, tasks
#Environemnt file reading for protection
import os
from dotenv import load_dotenv
#Misc Libraries
from datetime import time
#Custom Google Api Retrival Library
from GCaccess import getTodaysEvents

#Used .env to store discord bot token
load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
#if you want the chapter to add/vote for messages you can just use the txt

time = time(hour=6, minute=0)
#Insert Channel Id here
channel_id = ""
    
class Bot:
    def __init__(self, notification_message=False):

        self.intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix=";;", intents=self.intents)
        self.token = os.getenv("dsTOKEN")
        self.notification_message = notification_message
    
    
    class Notification:
        def __init__(self, title, description="Iota Xi Event", startTime="12:00PM", endTime="3:30PM", author="Iota Xi"):
            #Discord Embed Creation
            self.embed = Embed(title=title, description=description, color=discord.Color.from_rgb(24, 172, 255))
            self.embed.set_author(name=f"{author}", icon_url="INSERT YOUR OWN ICON HERE")
            if startTime == endTime:
                self.embed.add_field(name="Time", value=f"All day")
            else:
                self.embed.add_field(name="Time", value=f"{startTime} - {endTime}")
            self.embed.set_footer(text=f"Today's Event")

        
        def getEmbed(self):
            return self.embed

    #Sends out today's schedule
    @tasks.loop(time=time)
    async def notify(self):
        channel = self.bot.get_channel(channel_id)
        events = getTodaysEvents()
        #Prints multiple events, if you want to make it fancy use discord.Buttons to list through or merge them into one(hint:Use embed.add_field)
        for event in events:
            await channel.send(embed=self.Notification(event, description=events[event]["description"], startTime=events[event]["start"], endTime=events[event]["end"]).getEmbed())
        


    # Use to quickly run the notification
    # @tasks.loop(seconds=2)
    # async def notify_debug(self):
    #     channel = self.bot.get_channel(1021925897068085279) # <---- Change this to our @announcments
    #     events = getTodaysEvents()
    #     for event in events:
    #         #"This is the first ever description of a non existent event!\nFrom Google Calendar"
    #         await channel.send(embed=self.Notification(event, description=events[event]["description"], startTime=events[event]["start"], endTime=events[event]["end"]).getEmbed())

    #Bot Commands are here
    def run(self):
        #Some time loop that runs every time at 6am each day
        #Scan the current day of Google Calendar for events
        @self.bot.event
        async def on_ready():
            try:
                print("Google Calendar Bot is Operational🤓")
                #We start the notify loop, sends out the events every day at 6AM
                self.notify.start()
                #self.notify_debug.start()

            
            except Exception as e:
                print(f"The code produced the following error:\n{e}")

        self.bot.run(os.getenv("dsTOKEN"))


if __name__ == "__main__":
    Bot().run()