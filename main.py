from winsound import Beep
from colorama import Fore, Style, init
from mss import base, mss
from PIL import ImageGrab, Image
from ctypes import windll
from time import perf_counter, sleep
from os import system
from keyboard import is_pressed
from hashlib import sha256
from random import random
from json import load, dump
import subprocess, requests, time, os




hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
r = requests.get('https://github.com/dBv8mEYgdEfvtgrGrVZidoj7/sBas24xxzW677/blob/main/selam.txt') # Paste your URL  e.g(https://pastebin.com)

print(f'{hwid}')
time.sleep(2)

try:
    if hwid in r.text:
        pass
    else:
        print("[ERROR] Please buy the cheat.")
        time.sleep(5)
        os._exit()
except:
    print("[ERROR] Please buy the cheat.")
    time.sleep(5) 
    os._exit() 


__author__   = 'Niro'
__version__  = 'v1.0.0'


S_HEIGHT, S_WIDTH  = ImageGrab.grab().size
GRABZONE           = 5
IS_HOLDKEY         = True
IS_RUNING          = True
HOLDKEY            = 'shift'
TOGGLEKEY          = 'F6'
SWITCH_KEY         = 'ctrl + tab'
GRABZONE_KEY_UP    = 'ctrl + up'
GRABZONE_KEY_DOWN  = 'ctrl + down'
MODS               = ('0.3s Gecikme', '0.25s Gecikme', '0.2s Gecikme', '0.15s Gecikme', '0.1s Gecikme', 'Gecikmesiz')


class FoundEnemy(Exception):
    pass


class Config:

    base = {
        'Grabzone'  : 5,
        'IsHoldKey' : False,
        'HoldKey'   : 'shift',
        'ToggleKey' : 'F6'
    }

    def __init__(self, configName: str = 'config.json') -> None:
        self.configName = configName
        self.config     = None


    def createBaseConfig(self) -> None:
        with open(self.configName, 'w', encoding='utf-8') as f:
            self.config = self.base
            dump(self.config, f, ensure_ascii=False)


    def cfgLoad(self) -> dict:
        try:
            with open(self.configName, 'r', encoding='utf-8') as f:
                self.config = load(f)
                return self.config
        
        except FileNotFoundError:
            self.createBaseConfig()
            self.config = self.cfgLoad()
            return self.config



    def cfgDump(self) -> None:
        with open(self.configName, 'w', encoding='utf-8') as f:
            dump({
                'Grabzone'  : GRABZONE,
                'IsHoldKey' : IS_HOLDKEY,
                'HoldKey'   : HOLDKEY,
                'ToggleKey' : TOGGLEKEY
            }, f, ensure_ascii=False)


class TriggerBot:

    def __init__(self) -> None:
        self._mode       = 1
        self._last_reac  = 0


    def switch(self) -> None:
        Beep(200, 100)
        if self._mode != 5: self._mode += 1
        else: self._mode = 0


    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 0xAA: return False
        if green >= 0x78: return abs(red - blue) <= 0x8 and red - green >= 0x32 and blue - green >= 0x32 and red >= 0x69 and blue >= 0x69
        
        return abs(red - blue) <= 0xD and red - green >= 0x3C and blue - green >= 0x3C and red >= 0x6E and blue >= 0x64


    def grab(self) -> Image:
        with mss() as sct:
            bbox     = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE), int(S_WIDTH / 2 + GRABZONE))
            sct_img  = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


    def scan(self) -> None:
        start_time  = perf_counter()
        pmap        = self.grab()

        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.color_check(r, g, b): raise FoundEnemy
        
        except FoundEnemy:
            self._last_reac = int((perf_counter() - start_time) * 1000)
            windll.user32.mouse_event(0x2, 0x0, 0x0, 0x0, 0x0), windll.user32.mouse_event(0x4, 0x0, 0x0, 0x0, 0x0)

            if self._mode == 0: sleep(0.3)
            elif self._mode == 1: sleep(0.25)
            elif self._mode == 2: sleep(0.2)
            elif self._mode == 3: sleep(0.15)
            elif self._mode == 4: sleep(0.1)
            elif self._mode == 5: pass


def print_banner(bot: TriggerBot) -> None:
    system('cls')
    print(Style.BRIGHT + Fore.GREEN + f'[+] Trigger Tuşu         :', Fore.BLUE + f'{f"HoldKey [{HOLDKEY}]" if IS_HOLDKEY else f"[{TOGGLEKEY}]"}' + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + f'[+] Mod Değiştirme Tuşu      :', Fore.BLUE + "CTRL + TAB" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + f'[+] Bölge Yakalama Alanı Değiştir :', Fore.BLUE + "CTRL + UP" + '/' + "CTRL + DOWN" + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + f'[+] Mod                 :', Fore.BLUE  + MODS[bot._mode] + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + f'[+] Bölge Yakalama            :', Fore.BLUE  + str(GRABZONE) + 'x' + str(GRABZONE) + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + f'[+] Trigger Durumu       :', Fore.BLUE + f'{f"Hold down the [{HOLDKEY}] key" if IS_HOLDKEY else "Aktif!" if IS_RUNING else Fore.RED + "Pasif!"}' + Style.RESET_ALL)
    print(Style.BRIGHT + Fore.GREEN + f'[+] Tepki Süresi      :', Fore.BLUE  + str(bot._last_reac) + Fore.BLUE + ' ms (' + str((bot._last_reac) / (GRABZONE * GRABZONE)) + 'ms/pix)')


if __name__ == "__main__":
    _hash = sha256(f'{random()}'.encode('utf-8')).hexdigest()
    print(_hash), system(f'title {_hash}'), sleep(0.5), init(), system('@echo off'), system('cls')

    # Config Load
    cfg        = Config().cfgLoad()
    GRABZONE   = cfg['Grabzone']
    IS_HOLDKEY = cfg['IsHoldKey']
    HOLDKEY    = cfg['HoldKey']
    TOGGLEKEY  = cfg['ToggleKey']
    bot        = TriggerBot()

    print_banner(bot)

    while True:
        if is_pressed(SWITCH_KEY):
            bot.switch()
            print_banner(bot)
            continue

        if is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 1
            print_banner(bot), Beep(700, 100) 
            continue  

        if is_pressed(GRABZONE_KEY_DOWN):
            if GRABZONE != 1: GRABZONE -= 1
            print_banner(bot), Beep(700, 100)
            continue

        if IS_HOLDKEY:
            if is_pressed(HOLDKEY):
                bot.scan(), print_banner(bot)
                continue
        
        else:
            if is_pressed(TOGGLEKEY):
                IS_RUNING = not IS_RUNING
                print_banner(bot), Beep(700, 100)

            if IS_RUNING:
                bot.scan(), print_banner(bot)
                continue

        sleep(0.0025)
