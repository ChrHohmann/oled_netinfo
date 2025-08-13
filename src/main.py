#!/usr/bin/python
# -*- coding:utf-8 -*-

# Waveshare OLED module 0.91" has 128*32 pixels

import os
import logging
import time
import socket
import subprocess
from waveshare_OLED import OLED_0in91

from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)

# EEE wlan settings
EEE_SSID = "EEE"
# EEE_SSID = "JonasiPhone"
EEE_DOMAIN = "simple.eee.intern"

def get_wifi_ssid():
    """ Holt die aktuelle WLAN-SSID """
    try:
        ssid = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
        return ssid if ssid else None
    except:
        return None

def get_ip_address():
    """ Holt die IP-Adresse des Raspberry Pi """
    try:
        ip = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True).decode().strip()
        return ip if ip else "Keine IP"
    except:
        return "Keine IP"

def get_mac_address(interface):
    """ Holt die MAC-Adresse einer bestimmten Netzwerkschnittstelle """
    try:
        mac = subprocess.check_output(f"cat /sys/class/net/{interface}/address", shell=True).decode().strip()
        return mac if mac else "Keine MAC"
    except:
        return "Keine MAC"

try:
    disp = OLED_0in91.OLED_0in91()
    logging.info("\r0.91inch OLED Module ")
    disp.Init()

    # clear display
    logging.info("clear display")
    disp.clear()

    # generate new blank image as background (either black or white based on WLAN state)
    ssid = get_wifi_ssid()

    if ssid == EEE_SSID:
        image = Image.new('1', (disp.width, disp.height), "WHITE")  # black background -> waveshare oled module 0.91 inch has inverted background color since it is a monchromous display and PIL.Image expects RGB
        text_color = 0  # white font
        bg_color = "WHITE"
        message1 = f"{socket.gethostname()}.{EEE_DOMAIN}"
        message2 = get_ip_address()
    else:
        image = Image.new('1', (disp.width, disp.height), "BLACK")  # white background -> waveshare oled module 0.91 inch has inverted background color since it is a monchromous display and PIL.Image expects RGB
        text_color = 255  # black font
        bg_color = "BLACK"
        message1 = "Keine WLAN-Verbindung"
        message2 = get_mac_address("wlan0")

    draw = ImageDraw.Draw(image)

    # load font
    font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic', 'Font.ttc')
    font = ImageFont.truetype(font_path, 11) if os.path.exists(font_path) else ImageFont.load_default()

    # generate/add text to (blank) image
    draw.text((0, 2), message1, font=font, fill=text_color)
    draw.text((0, 18), message2, font=font, fill=text_color)

    # draw image / update screen
    disp.ShowImage(disp.getbuffer(image))
    # time.sleep(3)
    # disp.clear()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()
