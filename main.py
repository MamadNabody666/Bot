from telethon import TelegramClient, events
import asyncio
import random
import os


API_ID = 20756842  
API_HASH = "4b4ee2122b361f7e859d947c28484243"  
SESSION_NAME = "PowerSelf"

# راه‌اندازی کلاینت
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
enemies = {}  # لیست دشمن‌ها و تایمرها
attack_targets = {}  # لیست اتک و تایمرها
insults = ["لعنتی", "بی‌شعور", "احمق", "خاک بر سرت"]
SaveMode = "Off"


# 🔹 اضافه کردن دشمن
@client.on(events.NewMessage(pattern=r"^\.enemy(?: @?(\w+))?(?: (\d+))?$"))
async def add_enemy(event):
    match = event.pattern_match
    user = match.group(1)
    delay = int(match.group(2)) if match.group(2) else 0 
    if event.is_reply and not user:
        replied = await event.get_reply_message()
        user = replied.sender_id
    if user:
        enemies[user] = delay
        await event.reply(f"✅ {user} به لیست دشمن اضافه شد! (تأخیر: {delay} ثانیه)")
    else:
        await event.reply("❌ یوزرنیم یا ریپلای مشخص کن!")

# 🔹 حذف دشمن
@client.on(events.NewMessage(pattern=r"^\.remove_enemy(?: @?(\w+))?$"))
async def remove_enemy(event):
    match = event.pattern_match
    user = match.group(1)
    if event.is_reply and not user:
        replied = await event.get_reply_message()
        user = replied.sender_id
    if user in enemies:
        del enemies[user]
        await event.reply(f"✅ {user} از لیست دشمن حذف شد!")
    else:
        await event.reply("❌ این کاربر در لیست دشمن‌ها نیست!")

# 🔹 بررسی پیام‌های دشمن و ارسال فحش
@client.on(events.NewMessage)
async def enemy_responder(event):
    sender_id = event.sender_id
    if sender_id in enemies:
        delay = enemies[sender_id]
        if delay:
            await asyncio.sleep(delay)
        await event.reply(random.choice(insults))

# 🔹 اضافه کردن به لیست اتک
@client.on(events.NewMessage(pattern=r"^\.attack(?: @?(\w+))?(?: (\d+))?$"))
async def add_attack(event):
    match = event.pattern_match
    user = match.group(1)
    delay = int(match.group(2)) if match.group(2) else 0  # تایمر یا بدون توقف
    if event.is_reply and not user:
        replied = await event.get_reply_message()
        user = replied.sender_id
    if user:
        attack_targets[user] = delay
        await event.reply(f"🔥 {user} تحت اتک قرار گرفت! (تأخیر: {delay} ثانیه)")
        while user in attack_targets:
            await event.respond(random.choice(insults), reply_to=event.message.id)
            if delay:
                await asyncio.sleep(delay)
    else:
        await event.reply("❌ یوزرنیم یا ریپلای مشخص کن!")

# 🔹 حذف از لیست اتک
@client.on(events.NewMessage(pattern=r"^\.remove_attack(?: @?(\w+))?$"))
async def remove_attack(event):
    match = event.pattern_match
    user = match.group(1)
    if event.is_reply and not user:
        replied = await event.get_reply_message()
        user = replied.sender_id
    if user in attack_targets:
        del attack_targets[user]
        await event.reply(f"✅ {user} از لیست اتک حذف شد!")
    else:
        await event.reply("❌ این کاربر در لیست اتک نیست!")

# 🔹 اضافه کردن فحش
@client.on(events.NewMessage(pattern=r"^\.add_insult (.+)$"))
async def add_insult(event):
    insult = event.pattern_match.group(1)
    insults.append(insult)
    await event.reply(f"✅ فحش '{insult}' اضافه شد!")

# 🔹 حذف فحش
@client.on(events.NewMessage(pattern=r"^\.remove_insult (.+)$"))
async def remove_insult(event):
    insult = event.pattern_match.group(1)
    if insult in insults:
        insults.remove(insult)
        await event.reply(f"✅ فحش '{insult}' حذف شد!")
    else:
        await event.reply("❌ این فحش در لیست نیست!")


# فیکس باگ ذخیره فایل تایمردار
@client.on(events.NewMessage())
async def SaveMode_Setting(event):
    global SaveMode
    if(event.text=="سیو مود فعال" or event.text==".SaveMod_On"):
        await event.reply("حالت سیو مود فعال شد  \n شما اکنون میتوانید تصاویر و فیلم  و فایل های تایم دار را ذخیره کنید\nCoded By @MamadNabody6")
        SaveMode = "ok"
        
    if(event.text=="سیو مود غیر فعال" or event.text == ".SaveMod_Off"):
        await event.reply("حالت سیو مود غیرفعال شد\nCoded By @MamadNaody6")
        SaveMode = "off"
        

#ذخیره خودکار فایل ها
@client.on(events.NewMessage(func=lambda e: e.file))
async def save_file(event):
    global SaveMode
    
    if(SaveMode=="ok"):
     file_path = f"SecretFolder/{event.file.name}"
     await event.download_media(file=file_path)
     await event.reply(f"✅ فایل ذخیره شد: {file_path}")

# 🔹 ارسال سریع اعداد بعد از "خر"
@client.on(events.NewMessage(pattern=r"^خر(?: (\d+))?$"))
async def spam_numbers(event):
    await event.respond("1")
    await event.respond("2")
    await event.respond("3")
    await event.respond("4")
    await event.respond("5")
    await event.respond("6")
    await event.respond("7")
    await event.respond("8")
    await event.respond("9")
    await event.respond("10")

#شمارش زن حرفه ای
@client.on(events.NewMessage(pattern=r"^بمیر(?: (\d+))?$"))
async def spam_numbers(event):
    await event.respond("0")
    await event.respond("1")
    await event.respond("2")
    await event.respond("3")
    await event.respond("4")
    await event.respond("5")
    await event.respond("6")
    await event.respond("7")
    await event.respond("8")
    await event.respond("9")
    await event.respond("10")
    await event.respond("مدرک")
    
    
#مشاهده لیست فحش

@client.on(events.NewMessage(outgoing=True))
async def Fohshlist_View(event):
    global insults
    if(event.text=="لیست فحش" or event.text==".List_I"):
     await event.reply(f"{str(insults)}")
    
#مشاهده لیست دشمن
@client.on(events.NewMessage(outgoing=True))
async def EnemyList_View(event):
    global enemies
    if(event.text=="لیست دشمن" or event.text==".List_E"):
        await event.reply(f"{str(enemies)}")
    
         
#حدف لیست دشمن

@client.on(events.NewMessage(outgoing=True))
async def Remove_AllEnemy(event):
    global enemies
    if(event.text==".Remove_All_E" or event.text=="حذف لیست دشمن"):
        enemies.clear()
        await event.reply("♻️لیست دشمن خالی شد")
        
#حذف لیست فحش

@client.on(events.NewMessage(outgoing=True))
async def Remove_AllInsult(event):
    global insults
    if(event.text==".Remove_All_I" or event.text=="حذف لیست فحش"):
        insults.clear()
        await event.reply("♻️لیست فحش خالی شد")
        
#حذف لیست اتک

@client.on(events.NewMessage(outgoing=True))
async def Remove_AllAttack(event):
    global attack_targets
    if(event.text==".Remove_All_A" or event.text=="سحذف لیست اتک"):
        attack_targets.clear()
        await event.reply("♻️لیست اتک خالی شد")
    
    


# ذخیره فایل های تایم دار
@client.on(events.NewMessage(pattern=r'^\.$'))
async def save_self_destruct_file(event):
    if event.reply_to:
        msg = await event.get_reply_message()

        
        if msg.media and getattr(msg.media, "ttl_seconds", None):
            sender = await event.get_sender()
            file = await client.download_media(msg)

            if file:
                await client.send_file(sender.id, file, caption="✅ فایل ذخیره شد!\n\nCoded By @MamadNabody6")
                os.remove(file)
                await event.reply("✅ فایل تایم‌دار ذخیره شد در سیو مسیج!")
            else:
                await event.reply("❌این فایل تایم دار نیست")   
       
#ذخیره فایل

@client.on(events.NewMessage(pattern=r'^\!$'))
async def save_self_destruct_file2(event):
    if event.reply_to:
        msg = await event.get_reply_message()

        
        if msg.media:
            sender = await event.get_sender()
            file = await client.download_media(msg)

            if file:
                await client.send_file(sender.id, file, caption="✅ فایل ذخیره شد!\n\nCoded By @MamadNabody6")
                os.remove(file)
                await event.reply("✅ فایل ذخیره شد")
            
       
#مشاهده دستورات

@client.on(events.NewMessage(outgoing=True))
async def CommandList_View(event):
    text = "Command Of PowerSelf\n\n➖➖➖➖➖➖➖➖➖➖➖\n.enemy\n➖➖➖➖➖➖➖➖➖➖➖\n.remove_enemy\n➖➖➖➖➖➖➖➖➖➖➖\n.attack\n➖➖➖➖➖➖➖➖➖➖➖\n.remove_attack\n➖➖➖➖➖➖➖➖➖➖➖\n.add_insult Fohsh\n➖➖➖➖➖➖➖➖➖➖➖\n.remove_insult fohsh\n➖➖➖➖➖➖➖➖➖➖➖\n<=>"
    if(event.text=="پنل" or event.text==".Panel" or event.text==".panel"):
        await event.reply(str(text))
 
@client.on(events.NewMessage(outgoing=True))
async def Ping_Bot(event):
    if(event.text=="ping" or event.text=="پینگ" or event.text=="Ping"):
        await event.reply("ربات در حال حاضر آنلاین است🛜")

# راه‌اندازی سلف‌بات
async def main():
    print("🚀Self Has On")
    print("Coded By @MamadNaody6")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())