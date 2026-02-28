import discord
import os
import mysql.connector
from discord.ext import commands
from discord.ui import View, Button
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# koneksi ke db
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot sudah online")


@bot.tree.command(name="nim", description="Cari profil Mahasiswa pake NIM")
async def search_by_nim(interaction: discord.Interaction, nim: str):
    cursor = db.cursor()
    cursor.execute(
        "SELECT Nama, Prodi, Fakultas, Angkatan, TTL, Sosmed, Foto_Url FROM mahasiswa WHERE NIM = %s",
        (nim,)
    )
    data = cursor.fetchone()
    cursor.close()


    if data:
        nama, prodi, fakultas, angkatan, ttl, sosmed, Foto_Url = data
        embed = discord.Embed(
            title="Profil Mahasiswa",
            color=0x2ecc71
        )

        embed.set_image(
            url=Foto_Url 
        )

        embed.add_field(name="Nama", value=nama, inline=False)
        embed.add_field(name="NIM", value=nim, inline=False)
        embed.add_field(name="Program Studi", value=prodi, inline=False)
        embed.add_field(name="Fakultas", value=fakultas, inline=False)
        embed.add_field(name="Angkatan", value=angkatan, inline=False)
        embed.add_field(name="TTL", value=ttl, inline=False)
        embed.add_field(name="Sosmed", value=sosmed, inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            "❌ Data tidak ditemukan"
        )


@bot.tree.command(name="nama", description="Cari profil Mahasiswa pake Nama Lengkap")
async def search_by_nama(interaction: discord.Interaction, nama: str):
    cursor = db.cursor()
    cursor.execute(
        "SELECT NIM, Prodi, Fakultas, Angkatan, TTL, Sosmed, Foto_Url FROM mahasiswa WHERE Nama = %s",
        (nama,)
    )
    data = cursor.fetchone()
    cursor.close()

    if data:
        nim, prodi, fakultas, angkatan, ttl, sosmed, Foto_Url = data
        embed = discord.Embed(
            title="Profil Mahasiswa",
            color=0x2ecc71
        )

        embed.set_image(
            url=Foto_Url
        )

        embed.add_field(name="Nama", value=nama, inline=False)
        embed.add_field(name="NIM", value=nim, inline=False)
        embed.add_field(name="Program Studi", value=prodi, inline=False)
        embed.add_field(name="Fakultas", value=fakultas, inline=False)
        embed.add_field(name="Angkatan", value=angkatan, inline=False)
        embed.add_field(name="TTL", value=ttl, inline=False)
        embed.add_field(name="Sosmed", value=sosmed, inline=False)

        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            "❌ Data tidak ditemukan"
        )


class PaginationView(View):
    def __init__(self, angkatan: str, page: int):
        super().__init__(timeout=300)
        self.angkatan = angkatan
        self.page = page

    @discord.ui.button(label="⏮️ Prev", style=discord.ButtonStyle.secondary)
    async def prev(self, interaction: discord.Interaction, button: Button):
        if self.page <= 1:
            await interaction.response.defer()
            return
        
        await update_page(interaction, self.angkatan, self.page - 1)

    @discord.ui.button(label="⏭️ Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: Button):
        await update_page(interaction, self.angkatan, self.page + 1)

async def update_page(interaction: discord.Interaction, angkatan: str, page: int):
        limit = 20
        offset = (page - 1) * limit

        cursor = db.cursor()
        cursor.execute(
            """
            SELECT Nama, NIM
            FROM mahasiswa
            WHERE Angkatan = %s
            ORDER BY Nama ASC
            LIMIT %s OFFSET %s
            """,
            (angkatan, limit, offset)
        )
        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            await interaction.response.defer()
            return
        hasil = []
        start_no = offset + 1

        for i, (nama, nim) in enumerate(rows, start=start_no):
            hasil.append(f"{i}. {nama} [{nim}]")

        output = "\n".join(hasil)

        await interaction.response.edit_message(
            content=(
                f"📚 **Daftar Mahasiswa Prodi Teknologi Informasi angkatan {angkatan}**\n"
                f"Halaman {page}\n\n"
                f"{output}"
            ),
            view=PaginationView(angkatan, page)
        )


@bot.tree.command(name="list", description="List mahasiswa berdasarkan angkatan")
async def list_mahasiswa(interaction: discord.Interaction, 
                         angkatan: str
                    ):
    page = 1
    limit = 20
    offset = (page -1) * limit

    cursor = db.cursor()
    cursor.execute(
        """
        SELECT Nama, NIM 
        FROM mahasiswa 
        WHERE Angkatan = %s 
        ORDER BY Nama ASC
        LIMIT %s OFFSET %s
        """,
        (angkatan, limit, offset)
    )
    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        await interaction.response.send_message(
            f"Tidak ada mahasiswa ini di halaman {page}"
        )
        return
    
    hasil = []
    start_no = offset + 1

    for i, (nama, nim) in enumerate(rows, start=start_no):
        hasil.append(f"{i}. {nama} [{nim}]")

    output = "\n".join(hasil)

    await interaction.response.send_message(
    f"📚 **Daftar Mahasiswa Teknologi Informasi angkatan {angkatan}**\n"
    f"Halaman {page}\n\n"
    f"{output}",
    view=PaginationView(angkatan, page)
    )


bot.run(TOKEN)
