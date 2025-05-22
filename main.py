 #!/usr/bin/python

import random
import urllib.parse
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from pakundo import Pakundo

def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text


def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')    
    brand_name = "    ░██████╗░███╗░░░███╗░█████╗░\n"
    brand_name += "    ██╔════╝░████╗░████║██╔══██╗\n"
    brand_name += "    ██║░░██╗░██╔████╔██║██║░░╚═╝\n"
    brand_name += "    ██║░░╚██╗██║╚██╔╝██║██║░░██╗\n"
    brand_name += "    ╚██████╔╝██║░╚═╝░██║╚█████╔╝ █░█ █ █▀█\n"
    brand_name += "    ░╚═════╝░╚═╝░░░░░╚═╝░╚════╝░ ▀▄▀ █ █▀▀\n"
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
        "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,191,255)", "rgb(0,0,255)", "rgb(139,0,255)",
        "rgb(255,0,255)"
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    console.print("[bold green] ================================================[/bold green]")
    console.print("[bold white]  𝗣𝗟𝗘𝗔𝗦𝗘 𝗟𝗢𝗚 𝗢𝗨𝗧 𝗙𝗥𝗢𝗠 𝗖𝗣𝗠 𝗕𝗘𝗙𝗢𝗥𝗘 𝗨𝗦𝗜𝗡𝗚 𝗧𝗛𝗜𝗦 𝗧𝗢𝗢𝗟[/bold white]")
    console.print("[bold yellow]      𝗦𝗛𝗔𝗥𝗜𝗡𝗚 𝗧𝗛𝗘 𝗔𝗖𝗖𝗘𝗦 𝗞𝗘𝗬 𝗜𝗦 𝗡𝗢𝗧 𝗔𝗟𝗟𝗢𝗪𝗘𝗗[/bold yellow]")
    console.print("[bold green] ================================================[/bold green]")  
    
def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
            
            console.print("[bold][yellow]========[/yellow][ ᴘʟᴀʏᴇʀ ᴅᴇᴛᴀɪʟꜱ ][yellow]========[/yellow][/bold]")
            
            console.print(f"[bold green]  >> Name        : {data.get('Name', 'UNDEFINED')}[/bold green]")
            console.print(f"[bold green]  >> LocalID     : {data.get('localID', 'UNDEFINED')}[/bold green]")
            console.print(f"[bold green]  >> Money       : {data.get('money', 'UNDEFINED')}[/bold green]")
            console.print(f"[bold green]  >> Coins       : {data.get('coin', 'UNDEFINED')}[/bold green]")
            friends_count = len(data.get("FriendsID", []))
            console.print(f"[bold green]  >> Friends     : {friends_count}[/bold green]")
            car_data = data.get("carIDnStatus", {}).get("carGeneratedIDs", [])
            unique_car_data = set(car_data)
            car_count = len(unique_car_data)
            console.print(f"[bold green]  >> Cars        : {car_count}[/bold green]")
        
        else:
            console.print("[bold yellow] '! ERROR: new accounts must be signed-in to the game at least once (✘)[/bold yellow]")
            sleep(1)
    else:
        console.print("[bold yellow] '! ERROR: seems like your login is not properly set (✘)[/bold yellow]")
        exit(1)

     

def load_key_data(cpm):

    data = cpm.get_key_data()
    
    console.print("[bold][yellow]========[white][ 𝘼𝘾𝘾𝙀𝙎𝙎 𝙆𝙀𝙔 𝘿𝙀𝙏𝘼𝙄𝙇𝙎 ][/white]========[/yellow][/bold]")
    
    console.print(f"[bold white]  >> Access Key  [/bold white]: [yellow][bold]{data.get('access_key')}[/bold][/yellow]")
    
    console.print(f"[bold white]  >> Telegram ID : {data.get('telegram_id')}[/bold white]")
    
    console.print(f"[bold white]  >> Balance     : {data.get('coins') if not data.get('is_unlimited') else 'Unlimited'}[/bold white]")
    

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            console.print(f"[bold yellow]{tag} cannot be empty or just spaces. Please try again (✘)[/bold yellow]")
        else:
            return value
            
def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    console.print("[bold yellow] =============[bold white][ 𝙇𝙊𝘾𝘼𝙏𝙄𝙊𝙉 ][/bold white]=============[/bold yellow]")
    console.print(f"[bold green]  >> Country     : {data.get('country')} {data.get('zip')}[/bold green]")
    console.print("[bold yellow] ===============[bold green][ ＭＥＮＵ ][/bold green]===========[/bold yellow]")

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][?] Account Email[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] Account Password[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] Access Key[/bold]", "Access Key", password=False)
        console.print("[bold white][%] Trying to Login[/bold white]: ", end=None)
        cpm = Pakundo(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[bold yellow]ACCOUNT NOT FOUND (✘)[/bold yellow]")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[bold yellow]WRONG PASSWORD (✘)[/bold yellow]")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[bold yellow]INVALID ACCESS KEY (✘)[/bold yellow]")
                sleep(2)
                continue
            else:
                console.print("[bold yellow]TRY AGAIN[/bold yellow]")
                console.print("[bold white] '! Note: make sure you filled out the fields ![/bold white]")
                sleep(2)
                continue
        else:
            console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
            sleep(1)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52"]
            console.print("[bold white][bold green](01)[/bold green]: Increase Money                 [bold yellow]1.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](02)[/bold green]: Increase Coins                 [bold yellow]1.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](03)[/bold green]: King Rank                      [bold yellow]8K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](04)[/bold green]: Change ID                      [bold yellow]4.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](05)[/bold green]: Change Name                    [bold yellow]100[/bold yellow][/bold white]")
            console.print("[bold white][bold green](06)[/bold green]: Change Name (rainbow)          [bold yellow]100[/bold yellow][/bold white]")
            console.print("[bold white][bold green](07)[/bold green]: Number Plates                  [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](08)[/bold green]: Account Delete                 [bold yellow]Free[/bold yellow][/bold white]")
            console.print("[bold white][bold green](09)[/bold green]: Account Register               [bold yellow]Free[/bold yellow][/bold white]")
            console.print("[bold white][bold green](10)[/bold green]: Delete Friends                 [bold yellow]500[/bold yellow][/bold white]")
            console.print("[bold white][bold green](11)[/bold green]: Unlock Lamborghinis (ios only) [bold yellow]5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](12)[/bold green]: Unlock All Cars                [bold yellow]6K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](13)[/bold green]: Unlock All Cars Siren          [bold yellow]3.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](14)[/bold green]: Unlock W16 Engine              [bold yellow]4K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](15)[/bold green]: Unlock All Horns               [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](16)[/bold green]: Unlock Disable Damage          [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](17)[/bold green]: Unlock Unlimited Fuel          [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](18)[/bold green]: Unlock Home 3                  [bold yellow]4K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](19)[/bold green]: Unlock Smoke                   [bold yellow]4K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](20)[/bold green]: Unlock Wheels                  [bold yellow]4K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](21)[/bold green]: Unlock Animations              [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](22)[/bold green]: Unlock Equipaments M           [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](23)[/bold green]: Unlock Equipaments F           [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](24)[/bold green]: Change Race Wins               [bold yellow]1K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](25)[/bold green]: Change Race Loses              [bold yellow]1K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](26)[/bold green]: Clone Account                  [bold yellow]7K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](27)[/bold green]: Custom HP                      [bold yellow]2.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](28)[/bold green]: Custom Angle                   [bold yellow]1.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](29)[/bold green]: Custom Tire burner             [bold yellow]1.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](30)[/bold green]: Custom Car Millage             [bold yellow]1.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](31)[/bold green]: Custom Car Brake               [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](32)[/bold green]: Remove Rear Bumper             [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](33)[/bold green]: Remove Front Bumper            [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](34)[/bold green]: Change Account Password        [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](35)[/bold green]: Change Account Email           [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](36)[/bold green]: Custom Spoiler                 [bold yellow]10K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](37)[/bold green]: Custom BodyKit                 [bold yellow]10K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](38)[/bold green]: Unlock Premium Wheels          [bold yellow]4.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](39)[/bold green]: Unlock Toyota Crown            [bold yellow]2K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](40)[/bold green]: Unlock Clan Hat (m)            [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](41)[/bold green]: Remove Head Male               [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](42)[/bold green]: Remove Head Female             [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](43)[/bold green]: Unlock Clan Top 1 (m)          [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](44)[/bold green]: Unlock Clan Top 2 (m)          [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](45)[/bold green]: Unlock Clan Top 3 (m)          [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](46)[/bold green]: Unlock Clan Top 1 (fm)         [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](47)[/bold green]: Unlock Clan Top 2 (fm)         [bold yellow]3K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](48)[/bold green]: Unlock Mercedes Cls            [bold yellow]4K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](49)[/bold green]: Stance Camber                  [bold yellow]1K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](50)[/bold green]: Custom HP  All  Cars           [bold yellow]2.5K[/bold yellow][/bold white]")
            console.print("[bold white][bold green](51)[/bold green]: Login Another Account          [bold yellow]Free[/bold yellow][/bold white]")
            console.print("[bold white][bold green](0) [/bold green]: Exit From Tool [/bold white]")
            
            
            console.print("[bold yellow]===============[bold green][ Pakundo ][/bold green]===============[/bold yellow]")
            
            service = IntPrompt.ask(f"[bold][?] Select a Service [yellow][1-{choices[-1]} or 0][/yellow][/bold]", choices=choices, show_choices=False)
            
            console.print("[bold yellow]===============[bold green][ Pakundo ][/bold green]===============[/bold yellow]")
            
            if service == 0: # Exit
                console.print("[bold green] Thank You for using my tool[/bold green]")
            elif service == 1: # Increase Money
                console.print("[bold white][bold green][?][/bold green] Insert how much money do you want[/bold white]")
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Saving your data: ", end=None)
                if amount > 0 and amount <= 500000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                        console.print("[bold green]======================================[/bold green]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                        else: continue
                    else:
                        console.print("[bold yellow]FAILED (✘)[/bold yellow]")
                        console.print("[bold yellow]please try again later! (✘)[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FAILED (✘)[/bold yellow]")
                    console.print("[bold yellow]please use valid values! (✘)[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 2:  # Increase Coins
                console.print("[bold white][bold green][?][/bold green] Insert how much coins do you want[/bold white]")
                amount = IntPrompt.ask("[?] Amount")
                print("[ % ] Saving your data: ", end="")
                if amount > 0 and amount <= 500000:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                        console.print("[bold green]======================================[/bold green]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                        else: continue
                    else:
                        console.print("[bold yellow]FAILED[/bold yellow]")
                        console.print("[bold yellow]Please Try Again[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] 'Please use valid values[/bold white]")
                    sleep(2)
                    continue
            elif service == 3: # King Rank
                console.print("[bold yellow][!] Note:[/bold yellow]: if the king rank doesn't appear in game, close it and open few times.", end=None)
                console.print("[bold yellow][!] Note:[/bold yellow]: please don't do King Rank on same account twice.", end=None)
                sleep(2)
                console.print("[%] Giving you a King Rank: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold white] SUCCESSFUL[/bold white]")
                    console.print("[bold white] '======================================[/bold white]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 4: # Change ID
                console.print("[bold white] '[?] Enter your new ID[/bold white]")
                new_id = Prompt.ask("[?] ID")
                console.print("[%] Saving your data: ", end=None)
                if len(new_id) >= 8 and len(new_id) <= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold white] SUCCESSFUL[/bold white]")
                        console.print("[bold white] '======================================[/bold white]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                        else: continue
                    else:
                        console.print("[bold yellow]FAILED[/bold yellow]")
                        console.print("[bold yellow]Please Try Again[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] 'Please use valid ID[/bold white]")
                    sleep(2)
                    continue
            elif service == 5: # Change Name
                console.print("[bold white] '[?] Enter your new Name[/bold white]")
                new_name = Prompt.ask("[?] Name")
                console.print("[%] Saving your data: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(new_name):
                        console.print("[bold white] SUCCESSFUL[/bold white]")
                        console.print("[bold white] '======================================[/bold white]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                        else: continue
                    else:
                        console.print("[bold yellow]FAILED[/bold yellow]")
                        console.print("[bold yellow]Please Try Again[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] 'Please use valid values[/bold white]")
                    sleep(2)
                    continue
            elif service == 6: # Change Name Rainbow
                console.print("[bold white] '[?] Enter your new Rainbow Name[/bold white]")
                new_name = Prompt.ask("[?] Name")
                console.print("[%] Saving your data: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        console.print("[bold white] SUCCESSFUL[/bold white]")
                        console.print("[bold white] '======================================[/bold white]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                        else: continue
                    else:
                        console.print("[bold yellow]FAILED[/bold yellow]")
                        console.print("[bold yellow]Please Try Again[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] 'Please use valid values[/bold white]")
                    sleep(2)
                    continue
            elif service == 7: # Number Plates
                console.print("[%] Giving you a Number Plates: ", end=None)
                if cpm.set_player_plates():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 8: # Account Delete
                console.print("[bold white] '[!] After deleting your account there is no going back !![/bold white]")
                answ = Prompt.ask("[?] Do You want to Delete this Account ?!", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    console.print("[bold white] SUCCESSFUL[/bold white]")
                    console.print("[bold white] '======================================[/bold white]")
                    console.print("[bold white] f'Thank You for using our tool, please join our telegram channe: @{__CHANNEL_USERNAME__}[/bold white]")
                else: continue
            elif service == 9: # Account Register
                console.print("[bold white] '[!] Registring new Account[/bold white]")
                acc2_email = prompt_valid_value("[?] Account Email", "Email", password=False)
                acc2_password = prompt_valid_value("[?] Account Password", "Password", password=False)
                console.print("[%] Creating new Account: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold white] SUCCESSFUL[/bold white]")
                    console.print("[bold white] '======================================[/bold white]")
                    console.print("[bold white] f'INFO: In order to tweak this account with Telmun[/bold white]")
                    console.print("[bold white] 'you most sign-in to the game using this account[/bold white]")
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] 'This email is already exists ![/bold white]")
                    sleep(2)
                    continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 10: # Delete Friends
                console.print("[%] Deleting your Friends: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 11: # Unlock All Lamborghinis
                console.print("[!] Note: this function takes a while to complete, please don't cancel.", end=None)
                console.print("[%] Unlocking All Lamborghinis: ", end=None)
                if cpm.unlock_all_lamborghinis():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 12: # Unlock All Cars
                console.print("[%] Unlocking All Cars: ", end=None)
                if cpm.unlock_all_cars():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 13: # Unlock All Cars Siren
                console.print("[%] Unlocking All Cars Siren: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 14: # Unlock w16 Engine
                console.print("[%] Unlocking w16 Engine: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 15: # Unlock All Horns
                console.print("[%] Unlocking All Horns: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 16: # Disable Engine Damage
                console.print("[%] Unlocking Disable Damage: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 17: # Unlimited Fuel
                console.print("[%] Unlocking Unlimited Fuel: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 18: # Unlock House 3
                console.print("[%] Unlocking House 3: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 19: # Unlock Smoke
                console.print("[%] Unlocking Smoke: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 20: # Unlock Smoke
                console.print("[%] Unlocking Wheels: ", end=None)
                if cpm.unlock_wheels():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(8)
                    continue
            elif service == 21: # Unlock Smoke
                console.print("[%] Unlocking Animations: ", end=None)
                if cpm.unlock_animations():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 22: # Unlock Smoke
                console.print("[%] Unlocking Equipaments Male: ", end=None)
                if cpm.unlock_equipments_male():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 23: # Unlock Smoke
                console.print("[%] Unlocking Equipaments Female: ", end=None)
                if cpm.unlock_equipments_female():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 24: # Change Races Wins
                console.print("[bold white] '[!] Insert how much races you win[/bold white]")
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if amount > 0 and amount <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
                    if cpm.set_player_wins(amount):
                        console.print("[bold white] SUCCESSFUL[/bold white]")
                        console.print("[bold white] '======================================[/bold white]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                        else: continue
                    else:
                        console.print("[bold yellow]FAILED[/bold yellow]")
                        console.print("[bold yellow]Please Try Again[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] '[!] Please use valid values[/bold white]")
                    sleep(2)
                    continue
            elif service == 25: # Change Races Loses
                console.print("[bold white] '[!] Insert how much races you lose[/bold white]")
                amount = IntPrompt.ask("[?] Amount")
                console.print("[%] Changing your data: ", end=None)
                if amount > 0 and amount <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999:
                    if cpm.set_player_loses(amount):
                        console.print("[bold white] SUCCESSFUL[/bold white]")
                        console.print("[bold white] '======================================[/bold white]")
                        answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                        if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                        else: continue
                    else:
                        console.print("[bold yellow]FAILED[/bold yellow]")
                        console.print("[bold white] '[!] Please use valid values[/bold white]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] '[!] Please use valid values[/bold white]")
                    sleep(2)
                    continue
            elif service == 26: # Clone Account
                console.print("[bold white] '[!] Please Enter Account Detalis[/bold white]")
                to_email = prompt_valid_value("[?] Account Email", "Email", password=False)
                to_password = prompt_valid_value("[?] Account Password", "Password", password=False)
                console.print("[%] Cloning your account: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:     
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] '[!] THAT RECIEVER ACCOUNT IS GMAIL PASSWORD IS NOT VALID OR THAT ACCOUNT IS NOT REGISTEyellow[/bold white]")
                    sleep(2)
                    continue
            elif service == 27:
                console.print("[bold white][!] Note[/bold white]: original speed can not be restoyellow!.")
                console.print("[bold white][!] Enter Car Details.[/bold white]")
                car_id = IntPrompt.ask("[bold][?] Car Id[/bold]")
                new_hp = IntPrompt.ask("[bold][?]Enter New HP[/bold]")
                new_inner_hp = IntPrompt.ask("[bold][?]Enter New Inner Hp[/bold]")
                new_nm = IntPrompt.ask("[bold][?]Enter New NM[/bold]")
                new_torque = IntPrompt.ask("[bold][?]Enter New Torque[/bold]")
                console.print("[bold white][%] Hacking Car Speed[/bold white]:",end=None)
                if cpm.hack_car_speed(car_id, new_hp, new_inner_hp, new_nm, new_torque):
                    console.print("[bold green]SUCCESFUL (✔)[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white] '[!] Please use valid values[/bold white]")
                    sleep(2)
                    continue
            elif service == 28: # ANGLE
                console.print("[bold white] '[!] ENTER CAR DETALIS[/bold white]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold white] '[!] ENTER STEERING ANGLE[/bold white]")
                custom = IntPrompt.ask("[yellow][?]﻿ENTER THE AMOUNT OF ANGLE YOU WANT[/yellow]")                
                console.print("[yellow][%] HACKING CAR ANGLE[/yellow]: ", end=None)
                if cpm.max_max1(car_id, custom):
                    console.print("[bold white] SUCCESSFUL[/bold white]")
                    answ = Prompt.ask("[yellow][?] DO YOU WANT TO EXIT[/yellow] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 29: # tire
                console.print("[bold white] '[!] ENTER CAR DETALIS[/bold white]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold white] '[!] ENTER PERCENTAGE[/bold white]")
                custom = IntPrompt.ask("[pink][?]﻿ENTER PERCENTAGE TIRES U WANT[/pink]")                
                console.print("[yellow][%] Setting Percentage [/yellow]: ", end=None)
                if cpm.max_max2(car_id, custom):
                    console.print("[bold white] SUCCESSFUL[/bold white]")
                    answ = Prompt.ask("[bold green][?] DO YOU WANT TO EXIT[/bold green] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 30: # Millage
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER NEW MILLAGE![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿ENTER MILLAGE U WANT[/bold blue]")                
                console.print("[bold yellow][%] Setting Percentage [/bold yellow]: ", end=None)
                if cpm.millage_car(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 31: # Brake
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER NEW BRAKE![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿ENTER BRAKE U WANT[/bold blue]")                
                console.print("[bold yellow][%] Setting BRAKE [/bold yellow]: ", end=None)
                if cpm.brake_car(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 32: # Bumper rear
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")                
                console.print("[bold yellow][%] Removing Rear Bumper [/bold yellow]: ", end=None)
                if cpm.rear_bumper(car_id):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 33: # Bumper front
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")                
                console.print("[bold yellow][%] Removing Front Bumper [/bold yellow]: ", end=None)
                if cpm.front_bumper(car_id):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 34:
                console.print("[bold]Enter New Password![/bold]")
                new_password = prompt_valid_value("[bold][?] Account New Password[/bold]", "Password", password=False)
                console.print("[bold yellow][%] Changing Password [/bold yellow]: ", end=None)
                if cpm.change_password(new_password):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green]Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold white]FAILED[/bold white]")
                    console.print("[bold white]PLEASE TRY AGAIN[/bold white]")
                    sleep(2)
                    continue
            elif service == 36: # telmunnongodz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER SPOILER ID![/bold]")
                custom = IntPrompt.ask("[bold blue][?]ENTER NEW SPOILER ID[/bold blue]")                
                console.print("[bold yellow][%] SAVING YOUR DATA [/bold yellow]: ", end=None)
                if cpm.telmunnongodz(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 37: # telmunnongonz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER BODYKIT ID![/bold]")
                custom = IntPrompt.ask("[bold blue][?]INSERT BODYKIT ID[/bold blue]")                
                console.print("[bold yellow][%] SAVING YOUR DATA [/bold yellow]: ", end=None)
                if cpm.telmunnongonz(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 52: # copy_livery
                console.print("[bold]ENTER SOURCE CAR ID![/bold]")
                source_car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER TARGET CAR ID![/bold]")
                target_car_id = IntPrompt.ask("[bold blue][?]INSERT TARGET CAR ID[/bold blue]")                
                console.print("[bold yellow][%] COPYING LIVERY [/bold yellow]: ", end=None)
                if cpm.copy_livery(source_car_id, target_car_id):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 49: # telmunnongonz
                console.print("[bold]ENTER CAR DETAILS![/bold]")
                car_id = IntPrompt.ask("[bold][?] CAR ID[/bold]")
                console.print("[bold]ENTER VALUE FOR STANCE [/bold]")
                custom = IntPrompt.ask("[bold blue][?]INSERT VALUE[/bold blue]")                
                console.print("[bold yellow][%] SAVING YOUR DATA [/bold yellow]: ", end=None)
                if cpm.incline(car_id, custom):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 35:
                console.print("[bold]Enter New Email![/bold]")
                new_email = prompt_valid_value("[bold][?] Account New Email[/bold]", "Email")
                console.print("[bold yellow][%] Changing Email [/bold yellow]: ", end=None)
                if cpm.change_email(new_email):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    answ = Prompt.ask("[bold][?] DO YOU WANT TO EXIT[/bold] ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green]Thank You for using my tool[/bold green]")
                    else: break
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]EMAIL IS ALREADY REGISTEyellow [/bold yellow]")
                    sleep(4)
            elif service == 38: # SHITTIN
                console.print("[%] Unlocking Premium Wheels..: ", end=None)
                if cpm.shittin():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 39: # Unlock toyota crown
                console.print("[!] Note: this function takes a while to complete, please don't cancel.", end=None)
                console.print("[%] Unlocking Toyota Crown: ", end=None)
                if cpm.unlock_crown():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 40: # Unlock Hat
                console.print("[%] Unlocking Clan Hat: ", end=None)
                if cpm.unlock_hat_m():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 41: # remove head male
                console.print("[%] Removing Male head: ", end=None)
                if cpm.rmhm():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 42: # remove head female
                console.print("[%] Removing Female Head: ", end=None)
                if cpm.rmhfm():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 43: # Unlock TOPM
                console.print("[%] Unlocking Clan clothes Top 1: ", end=None)
                if cpm.unlock_topm():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 44: # Unlock TOPMz
                console.print("[%] Unlocking Clan clothes Top 1: ", end=None)
                if cpm.unlock_topmz():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 45: # Unlock TOPMX
                console.print("[%] Unlocking Clan clothes Top 2: ", end=None)
                if cpm.unlock_topmx():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 46: # Unlock TOPF
                console.print("[%] Unlocking Clan clothes Top: ", end=None)
                if cpm.unlock_topf():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 47: # Unlock TOPFZ
                console.print("[%] Unlocking Clan clothes Top 1: ", end=None)
                if cpm.unlock_topfz():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 48: # Unlock Mercedes Cls
                console.print("[%] Unlocking Mercedes Cls: ", end=None)
                if cpm.unlock_cls():
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("[bold green]======================================[/bold green]")
                    answ = Prompt.ask("[?] Do You want to Exit ?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green] Thank You for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold yellow]Please Try Again[/bold yellow]")
                    sleep(2)
                    continue  
            elif service == 50:
                console.print("[bold white][!] Note[/bold white]: This will modify ALL your cars' speed!")
                console.print("[bold white][!] Enter New Engine Specs.[/bold white]")
                new_hp = IntPrompt.ask("[bold][?] Enter New HP[/bold]")
                new_inner_hp = IntPrompt.ask("[bold][?] Enter New Inner HP[/bold]")
                new_nm = IntPrompt.ask("[bold][?] Enter New NM[/bold]")
                new_torque = IntPrompt.ask("[bold][?] Enter New Torque[/bold]")
                console.print("[bold white][%] Hacking All Cars Speed[/bold white]:", end=None)
                if cpm.hack_all_cars_speed(new_hp, new_inner_hp, new_nm, new_torque):
                    console.print("[bold green]SUCCESSFUL (✔)[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask("[?] Do you want to exit?", choices=["y", "n"], default="n")
                    if answ == "y": console.print("[bold green]Thank you for using my tool[/bold green]")
                    else: continue
                else:
                    console.print("[bold yellow]FAILED[/bold yellow]")
                    console.print("[bold white][!] Please use valid values[/bold white]")
                    sleep(2)
                    continue
            elif service == 51: # Clone Account
                print(Colorate.Horizontal(Colors.rainbow, '[!] Please Enter Account Detalis.'))
                to_email = prompt_valid_value("[?] Account Email", "Email", password=False)
                to_password = prompt_valid_value("[?] Account Password", "Password", password=False)
                console.print("[%] Account log in: ", end=None)
                if cpm.login(to_email, to_password):
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))
                    sleep(2)
                    continue
                else:     
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESSFUL.'))
                    sleep(2)
                    continue
            else: continue
            break      
