import discord
import random
import asyncio
import datetime
import pytz

# 디스코드 클라이언트 생성
INTENTS = discord.Intents.all()
client = discord.Client(intents=INTENTS)
tree = discord.app_commands.CommandTree(client)

# 봇이 준비되면 실행되는 이벤트 핸들러
@client.event
async def on_ready(): # 봇이 실행되면 한 번 실행됨
    print("봇이 온라인 됩니다.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("테스트"))

# 임베드에 사용할 랜덤 색상을 선택하는 함수
def random_color():
    return discord.Color(random.randint(0, 0xFFFFFF))

# '!embed'라는 명령어를 받았을 때 실행되는 이벤트 핸들러
@client.event
async def on_message(message):
    if message.content.startswith('!embed'):
        if not message.author.guild_permissions.administrator:
            await message.channel.send(f"{message.author.mention}, 당신은 관리자가 아닙니다. 관리자만 사용할 수 있는 명령어입니다.")
            return
        
        await message.delete()
        # 입력된 메시지를 줄 단위로 분할하여 제목과 내용을 추출
        lines = message.content.split('\n')
        title = lines[0].replace('!embed', '').strip()  # 첫 번째 줄을 제목으로 사용
        description = '\n'.join(lines[1:]).strip()  # 두 번째 줄 이후를 내용으로 사용
        if title and description:
            # 랜덤한 색상으로 임베드 생성
            embed = discord.Embed(
                title=f"**{title}**",
                description=f"**{description}**",
                color=random_color()
            )
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("제목과 내용을 입력하세요.")

    elif message.content.startswith("!공지"):
        await message.delete()
        if message.author.guild_permissions.administrator:
            notice = message.content[4:]
            server_name = message.guild.name  # 서버 이름 가져오기

            # 공지를 입력한 채널에만 공지를 전송합니다.
            channel = message.channel   
            embed = discord.Embed(title=f"**{server_name} 공지사항**", description=f"**공지사항 내용은 항상 숙지 해주시기 바랍니다**\n**▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃**\n\n{notice}\n\n**▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃**", timestamp=datetime.datetime.now(pytz.timezone('UTC')), color=0x00ff00)
            embed.set_footer(text=f"Edit by. seori_99 | 담당 관리자 : {message.author.display_name}", icon_url="https://cdn.discordapp.com/attachments/1214278883369816128/1230043028115292160/1_-removebg-preview.png?ex=6631e1d6&is=661f6cd6&hm=177c1c7759c02315a6ebbdd50dc7cdc2849753217a3c26a6ea61830bd28d8dda&")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1214278883369816128/1230043381783072809/2_-removebg-preview.png?ex=6631e22b&is=661f6d2b&hm=1d15134b1087a06c0838112647f57eae0920ec011f977a33ee7943eac357a5da&")
            await channel.send("@everyone", embed=embed)

            await message.author.send(f"**[ BOT 자동 알림 ]** | 정상적으로 공지가 채널에 작성이 완료되었습니다 : )\n\n[ 기본 작성 설정 채널 ] : {channel}\n[ 공지 발신자 ] : {message.author}\n\n[ 내용 ]\n{notice}")
        else:
            await message.channel.send(f"{message.author.mention}, 당신은 관리자가 아닙니다")

    elif message.content.startswith ("!청소"):
        if message.author.guild_permissions.administrator:
            amount = message.content[4:]
            await message.delete()
            await message.channel.purge(limit=int(amount))

            embed = discord.Embed(title="메시지 삭제 알림", description="최근 디스코드 채팅 {}개가\n관리자 {}님의 요청으로 인해 정상 삭제 조치 되었습니다".format(amount, message.author), color=0xFF0000)
            embed.set_footer(text="Bot Edit by. 서리", icon_url="https://search.pstatic.net/sunny/?src=https%3A%2F%2Fpng.pngtree.com%2Fpng-clipart%2F20190920%2Foriginal%2Fpngtree-hygiene-cleaning-cartoon-illustration-png-image_4656357.jpg&type=sc960_832")
            await message.channel.send(embed=embed)
        
        else:
            await message.delete()
            await message.channel.send("{}, 당신은 명령어를 사용할 수 있는 권한이 없습니다".format(message.author.mention))

# 슬래쉬 커맨드 예제
@tree.command(name="제목",description="설명")
async def socis(interaction:discord.interactions.Interaction):
    await interaction.response.send_message("봇의 대답")

@client.event
async def on_member_join(member):
    embed = discord.Embed(colour=discord.Colour.random(), title=f"{member.display_name}님 어서오세요, {member.guild}에 오신 것을 환영합니다!", description="공지사항 필수로 숙지해 주세요")

    for channel in member.guild.channels:
        if channel.name == "입장로그":
            await channel.send(embed=embed)
            break
    else:  # if 구문에서 채널을 찾지 못한 경우
        channel = await member.guild.create_text_channel(name="입장로그")
        await channel.send(embed=embed)
        
# 디스코드 봇 토큰을 입력하세요
client.run('MTIzMDA0OTk4MjczNjc2NDkyOQ.G7zzfF.lKbWofs5EaGnT-noxAXfEaanmPaBtliKCgzwNs')
