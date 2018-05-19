#!/usr/bin/env python3

# andysircbot.py - A simple IRC-bot written in python
#
# Copyright (C) 2015 : Niklas Hempel - http://liq-urt.de
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import re
import socket
import time
import virtualkeyboard as vkb
# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = "#daiphai"                               # Channelname = #{Nickname} Channel for the bot to be in
NICK = "audebot"                                # Nickname = Twitch bot username
PASS = "oauth:8dwhoduwuzl5b482l0duj4kxn11umi"   # www.twitchapps.com/tmi/ will help to retrieve the required authkey

oplist = {'kenwayauditore', 'daiphai', 'primalcarnag3', 'momo2532'} # The list of users able to use commands
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def parse_message(msg):
    if len(msg) >= 1 and sender in oplist:
        msg = msg.split(' ')
        options = {'!test': command_test,
                   '!gamecam': switch_cam1,
                   '!facecam': switch_cam2,
                   '!brbcam': switch_cam3}
        if msg[0] in options:
            options[msg[0]]()
# --------------------------------------------- End Helper Functions -----------------------------------------------

# --------------------------------------------- Start Command Functions --------------------------------------------
def command_test():
    send_message(CHAN, 'Testing command')

# Sends the keyboard input CTRL + Shift + F3
def switch_cam1():
    send_message(CHAN, 'SWITCHING TO GAMECAM SCENE')
    vkb.SendInput(vkb.Keyboard(vkb.VK_CONTROL), vkb.Keyboard(vkb.VK_SHIFT), vkb.Keyboard(vkb.VK_F3))
    time.sleep(0.2)
    vkb.SendInput(vkb.Keyboard(vkb.VK_CONTROL, vkb.KEYEVENTF_KEYUP),
                  vkb.Keyboard(vkb.VK_SHIFT, vkb.KEYEVENTF_KEYUP),
                  vkb.Keyboard(vkb.VK_F3,  vkb.KEYEVENTF_KEYUP))
    time.sleep(0.2)

# Sends the keyboard input CTRL + Shift + F4
def switch_cam2():
    send_message(CHAN, 'SWITCHING TO FACECAM SCENE')
    vkb.SendInput(vkb.Keyboard(vkb.VK_CONTROL), vkb.Keyboard(vkb.VK_SHIFT), vkb.Keyboard(vkb.VK_F4))
    time.sleep(0.2)
    vkb.SendInput(vkb.Keyboard(vkb.VK_CONTROL, vkb.KEYEVENTF_KEYUP),
                  vkb.Keyboard(vkb.VK_SHIFT, vkb.KEYEVENTF_KEYUP),
                  vkb.Keyboard(vkb.VK_F4,  vkb.KEYEVENTF_KEYUP))
    time.sleep(0.2)

# Sends the keyboard input CTRL + Shift + F5
def switch_cam3():
    send_message(CHAN, 'SWITCHING TO BRB SCENE')
    vkb.SendInput(vkb.Keyboard(vkb.VK_CONTROL), vkb.Keyboard(vkb.VK_SHIFT), vkb.Keyboard(vkb.VK_F5))
    time.sleep(0.2)
    vkb.SendInput(vkb.Keyboard(vkb.VK_CONTROL, vkb.KEYEVENTF_KEYUP),
                  vkb.Keyboard(vkb.VK_SHIFT, vkb.KEYEVENTF_KEYUP),
                  vkb.Keyboard(vkb.VK_F5,  vkb.KEYEVENTF_KEYUP))
    time.sleep(0.2)

# --------------------------------------------- End Command Functions ----------------------------------------------


# ------------------------------------ Let's the user know the bot is now running-----------------------------------
print("Hello! Welcome to Andy\'s IRC bot!")
print("The following commands that are implemented are: !gamecam, !facecam, and !brbcam")
print("Please enjoy the user of this program LUL - Andy A.K.A. twitch.tv/DAIPHAI\n")
# ------------------------------------------------------------------------------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)

data = ""

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()

        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(message)

                    print(sender + ": " + message)

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")