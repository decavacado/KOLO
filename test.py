import discord
import pymongo
import random
import time
from threading import Timer
import asyncio

def async_call_later(seconds, callback):
    async def schedule():
        await asyncio.sleep(seconds)

        if asyncio.iscoroutinefunction(callback):
            await callback()
        else:
            callback()

    asyncio.ensure_future(schedule())

#making connection to local mongodb database
mongo = pymongo.MongoClient(DBHERE)
trivia =  mongo.Trivia
trivia_things = trivia.trivias
trivia_list = []

for trivia in trivia_things.find():
	print(trivia)
	trivia_list.append({'question': trivia["question"], 'answer': trivia["answer"]})

print(trivia_list)

#initialize bot
client = discord.Client()
game = discord.Game("$help for help")

print(client);

prefix = "$"

# Python Bot
@client.event
async def on_ready():
	print("client has logged in bois")
	await client.change_presence(activity=game)

@client.event
async def on_message(message):
	#trivia stuff
	player = None;

	cons = message.content.split()
	print(cons)
	if len(cons) == 0:
		a = message.content.lower()
	else:
		a  = cons[0].lower()
	print(a)
	pop = " "
	if a == "$add":
		cons.pop(0)
		try:
			num1 = float(cons[0])
			num2 = float(cons[1])
			await message.channel.send(num1 + num2)
		except ValueError:
			await message.channel.send("Buddy those are letters.")
		mes = pop.join(cons)
	elif a == "$sub":
		cons.pop(0)
		try:
			num1 = float(cons[0])
			num2 = float(cons[1])
			await message.channel.send(num1 - num2)
		except ValueError:
			await message.channel.send("Buddy those are letters bro")
		mes = pop.join(cons)
	elif a == "$hello":
		try:
			cons.pop(0)
			mes = pop.join(cons)
			if(len(cons) == 0):
				await message.channel.send("Missing Argument")
			else:
				print(cons)
				await message.channel.send(mes)
				await message.channel.send(message.author.mention)
		except:
			await message.channel.send("Missing Argument")
	elif a == "$games":
		try:
			embed = discord.Embed()
			embed.add_field(name="Games List", value="Here are the list of games you can play", inline=False)
			embed.add_field(name="Trivia", value="$trivia for a trivia game", inline=False)
			await message.channel.send(embed = embed, content = "Empty")
		except:
			print("Somthing bad happened")
	elif a == "$wake":
		await message.channel.send("Wake up " + "<@!" +str(message.mentions[0].id) + ">")
		print(message.mentions)
	elif a == "$help":
		try:
			embed = discord.Embed(title="Help", colour=0xcc1b1b)
			embed.add_field(name="Commands", value="Here are a few commands")
			embed.add_field(name="$add",value="Used to add  two args <num1> <num2>", inline=False)
			embed.add_field(name="$sub",value="Used to subtract two args <num1> <num2>")
			embed.add_field(name="$games",value="Used to see of games available", inline=False)
			embed.set_footer(text="Made with ❤️ By Declan", icon_url="https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/s150x150/94214424_740320093171238_2986654231106158592_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=zZnws6j1unoAX_ggKeY&oh=a19f9d4d91d4d387a204672953c085a1&oe=5EE20254")
			embed.set_thumbnail(url="https://images.discordapp.net/avatars/422087909634736160/ba3af9afe0ec8253149ac7f5f84a69f1.png?size=512")
			await message.channel.send(embed = embed)
		except:
			await message.channel.send("Something went wrong")
	elif a == "$trivia":
		global trivia_list
		trivia_list = []
		for trivia in trivia_things.find():
			trivia_list.append({'question': trivia["question"], 'answer': trivia["answer"]})
		print(trivia_list)
		random_num = random.randint(0, len(trivia_list)-1)
		embed = discord.Embed(title="Trivia", colour=0xcc1b1b)
		embed.set_footer(text="Made with ❤️ By Declan", icon_url="https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/s150x150/94214424_740320093171238_2986654231106158592_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=zZnws6j1unoAX_ggKeY&oh=a19f9d4d91d4d387a204672953c085a1&oe=5EE20254")
		embed.set_thumbnail(url="https://images.discordapp.net/avatars/422087909634736160/ba3af9afe0ec8253149ac7f5f84a69f1.png?size=512")
		embed.add_field(name="Question",value=trivia_list[random_num]['question'],inline=False)
		player = message.author
		await message.channel.send(embed = embed)
		print(player)
		await message.channel.send(content="Send the Answer")
		def check(m):
			mes = m.content.lower()
			return True
		try:
			async def res():
				msg = await client.wait_for('message', timeout=16.0, check=check)
				print(msg.content)
				print(msg.channel)
				print(message.channel)
				mes = msg.content.lower()
				if mes == trivia_list[random_num]['answer'] and msg.channel == message.channel:
					await message.channel.send("You got it right the answer was " + trivia_list[random_num]['answer'])
				elif msg.channel == message.channel:
					await message.channel.send("You got it wrong the answer is " + trivia_list[random_num]['answer'])
				else: 
					await res()
			await res()
		except asyncio.TimeoutError:
			await message.channel.send("You did not answer the question fast enough")
	elif a == "$t-add":
		cons.pop(0)
		await message.channel.send(content="Type the question you will like to add?")
		def check(m):
			mes = m.content.lower()
			return True
		try:
			msg = await client.wait_for('message', timeout=16.0, check=check)
			question = ""
			if message.author == msg.author:
				question = msg.content
				await message.channel.send(content="Your question is <" + question + ">")
				await message.channel.send(content="Now type the answer")
				msg2 = await client.wait_for('message', timeout=16.0, check=check)
				answer = ""
				if message.author == msg2.author:
					answer = msg2.content.lower()
					await message.channel.send(content="Your answer is <" + answer + ">")
					new_stuff = {'question': question, 'answer': answer}
					trivia_list.append(new_stuff)			
					trivia_things.insert_one(new_stuff)
			else:
				await message.channel.send(content = "Interruption Error")
		except asyncio.TimeoutError:
			await message.channel.send("You took to long to add a question")
	elif message.content.startswith(prefix):
		embed = discord.Embed(title="Command not found",colour=0xcc1b1b);
		embed.set_thumbnail(url="https://images.discordapp.net/avatars/422087909634736160/ba3af9afe0ec8253149ac7f5f84a69f1.png?size=512")
		embed.set_footer(text="Made with ❤️ By Declan", icon_url="https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/s150x150/94214424_740320093171238_2986654231106158592_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=zZnws6j1unoAX_ggKeY&oh=a19f9d4d91d4d387a204672953c085a1&oe=5EE20254")
		embed.add_field(name="Error",value="Command not found use $help to see available commands",inline=False)
		await message.channel.send(embed = embed)


client.run("KEY HERE")
