# rktlnch (Rocket Launch) - PoC
## What

An Epic Game Store-less Epic Game Store game launcher. I hope that makes sense.

Longer: `rktlnch` can be used to launch games installed via the Epic Game Store launcher without having to run the launcher every time.
Many games work offline and don't need this, but for those that have online functionality, rktlnch will enable you to continue using it without having to run the EGS.

**Be warned:** this was quickly hacked together and is a bit of a mess. 

## Why

This was a PoC I wrote because I was wondering if I can launch Diabotical from my desktop, or Steam, or whatever, without having to run the EGS client each time.

Let's face it, the Epic Game Store launcher is kind of a piece of crap. It runs an Unreal Engine application to show you a website.
This in turn means that on a laptop it will run on the dedicated GPU, even if it's not doing anything, causing unnecessary battery drain and your fans to spin up.

It's also somehow slower than the new Steam UI, despite Valve's best efforts.

## How

For some reason the games on the Epic Game Store do not seem to rely on IPC with the launcher for their online functionality, instead they get launched with an OAuth(?) access token they can use to directly talk to Epic's online services.

Whatever the reason, we can make use of this nice design choice to run and play games (online) without the EGS Launcher.

## Yeah but how do I use it?

1. Download the latest .exe from the [Releases](https://github.com/derrod/rktlnch/releases/latest)
2. Create a shortcut, add it to Steam, whatever
3. Set the command line parameters to `--launch <Epic App Name>`
4. ???
5. Profit!

Usage is fairly simple:
```
usage: rktlnch.exe [-h] (--launch APP_NAME | --list-games)
                   [--skip-version-check]

Launch an EGS game without EGS.

optional arguments:
  -h, --help            show this help message and exit
  --launch APP_NAME     Launch game with codename APP_NAME
  --list-games          List installed app names and their corresponding game
                        names.
  --skip-version-check  Skip version check
```

`APP_NAME` is the codename the game is using on EGS, *not* the actual name of the game. For instance, for Diabotical this is `Honeycreeper`.

You can get a list of all installed EGS games and their codenames by simply running `rktlnch.exe --list-games` 


## How 2 EXE

The exe in releases was built using PyInstaller using the following command:
```
py -3.6 -O -m PyInstaller --onefile src\rktlnch.py
```

Yes I'm still running Python 3.6. Yes I know I should update. Please don't remind me. 

## What about Linux?

idk I guess this could run in WINE? Somebody else can take this example and make their own thing.

