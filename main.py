import discord
import random
import asyncio

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

    # ---> random msgs -- every time the bot is tagged --
        if self.user.mentioned_in(message):
            responses = ["msg1", "msg2", "msg3", "msg4", "msg5",]
            response = random.choice(responses)
            await message.channel.send(response)

        # connects to the voice channel of the user who mentioned the bot,
        # plays a randomly selected MP3 sound, and disconnects after playback
            if message.author.voice and message.author.voice.channel:
                voice_channel = message.author.voice.channel
                try:
                    vc = await voice_channel.connect()
                    print("✅ Bot connected to the voice channel.")

                    # randomly choose between 'sound.mp3' and 'sound1.mp3'
                    audio_file = random.choice(["sound.mp3", "sound1.mp3"])
                    audio = discord.FFmpegPCMAudio(audio_file)

                    vc.play(audio)
                    print(f"🔊 Playing audio.. {audio_file}...")
                    while vc.is_playing():
                        await asyncio.sleep(1)

                    await vc.disconnect()
                    print("🔇 Audio finished, bot disconnected")
                except Exception as e:
                    print(f"❌ Error connecting or reproducing: {e}")
            else:
                print("⛔ The user is not on a voice channel.")

        # #chan -> channel id -> message
        if isinstance(message.channel, discord.DMChannel):
            if message.author.id != 1111111:        # <- here change your discord id
                await message.channel.send("❌ You can't use this.")
                return

            if message.content.startswith("#chan "):
                try:
                    parts = message.content.split(" ", 2)
                    channel_id = int(parts[1])
                    text = parts[2]
                    channel = self.get_channel(channel_id)
                    if channel:
                        await channel.send(text)
                        await message.channel.send("✅ Sent")
                    else:
                        await message.channel.send("❌ Channel not found.")
                except Exception as e:
                    await message.channel.send(f"❌ Error: {e}")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.dm_messages = True
intents.voice_states = True

client = Client(intents=intents)
client.run('') #Here your discord bot token