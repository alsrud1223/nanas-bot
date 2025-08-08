from flask import Flask
from threading import Thread
import os
import discord
from discord.ext import commands

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    port = int(os.environ.get("PORT", 8080))  # Render가 감지할 포트
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 환경변수에서 토큰, 비밀번호, 역할 이름 불러오기
TOKEN = os.environ['TOKEN']
PASSWORD = os.environ.get('PASSWORD', '1223')  # 기본값 설정 가능
ROLE_NAME = os.environ.get('ROLE_NAME', '₍ᐢ..ᐢ₎')      # 기본 역할 이름

# 인텐트 설정 (멤버 입장 이벤트와 메시지 콘텐츠 읽기 허용)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 비밀번호 입력 모달 클래스
class PasswordModal(discord.ui.Modal, title="🔐 비밀번호 입력"):
    password = discord.ui.TextInput(label="비밀번호를 입력해주세요", style=discord.TextStyle.short, required=True)

    async def on_submit(self, interaction: discord.Interaction):
        if self.password.value.strip() == PASSWORD:
            role = discord.utils.get(interaction.guild.roles, name=ROLE_NAME)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message("✅ 인증 성공! 𝘯𝘰𝘵𝘪𝘧𝘪𝘢𝘵𝘪𝘰𝘯 채널을 확인해 주세요.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ 역할이 존재하지 않아요.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ 비밀번호가 틀렸어요!", ephemeral=True)

# 버튼 뷰 클래스
class PasswordButton(discord.ui.View):
    @discord.ui.button(label="비밀번호 입력", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(PasswordModal())

# 멤버 입장 이벤트 - 환영 메시지 및 비밀번호 버튼 전송
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="password")
    if channel:
        try:
            await channel.purge()
        except Exception as e:
            print(f"채널 메시지 삭제 실패: {e}")
        await channel.send(
            f"{member.mention} 👋\n버튼을 눌러 비밀번호를 입력해주세요!",
            view=PasswordButton()
        )

@bot.event
async def on_ready():
    print(f'✅ 봇 로그인됨: {bot.user}')

keep_alive()

bot.run(TOKEN)
