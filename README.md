# rktlnch ("Rocket Launch")
### An Epic Game Store-less Epic Game Store game launcher

`rktlnch` can be used to launch games installed via the Epic Game Store application without having to run the EGS launcher itself.
Many games work offline and don't need this, but for those that have online functionality, rktlnch will enable you to play online or use online functionality without having to run the EGS app.

**Be warned:** this was quickly hacked together and most assuredly contains bugs and issues.

## Usage

0. Install the EGS and some game(s), make sure to check "Remember Me" when logging in
1. Download the latest .exe from the [Releases](https://github.com/derrod/rktlnch/releases/latest) tab
2. Create a Desktop shortcut or add it to Steam, GOG Galaxy, etc.
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

Any additional arguments will be passed on to the game itself.

You can get a list of all installed EGS games and their codenames by simply running `rktlnch.exe --list-games` 

**NOTE:** Do not run EGS and rktlnch at the same time! Since rktlnch will read and write from/to the EGS config this can cause issues (e.g. invalidating your login session, requiring you to login again next time you start EGS).

## Tested Games

#### Confirmed working:
 * Dauntless (`Jackal`)
 * Diabotical (`Honeycreeper`)
 * Fortnite (`Fortnite`)
 * Spellbreak (`Newt`)
 * Subnautica (`Jaguar`) - not really required for this game since it's singleplayer only
 * The Cycle (`AzaleaAlpha`)
 * The Jackbox Party Pack (`Feverfew`)
#### Confirmed **NOT** working
 * N/A

## Why

This was a PoC ("Proof of Concept") I wrote because I was wondering if I can launch Diabotical from my Desktop, or Steam, or whatever, without having to boot up the EGS client each time.

Let's face it, the Epic Game Store launcher is kind of crap. It runs an Unreal Engine application to show you a website.
This in turn means that on a laptop it will run on the dedicated GPU, even if it's not doing anything, causing unnecessary battery drain and your fans to spin up.

With rktlnch it is only needed to install or update games, but playing the game is possible without ever having to launch it.

## How

Curiously the games on the Epic Game Store do not seem to rely on some form of communication with the launcher for their online functionality, instead they get launched with an OAuth token they can use to directly talk to Epic's online services.

Whatever the reason, we can make use of this design choice to run and play games (online) without the EGS Launcher.

`rktlnch` achieves this as follows:
1. Get refresh token from EGS config in `%APPDATA%`
2. Read manifests of installed EGS games in `%PROGRAMDATA%`
3. Check if requested game is installed
4. Authenticate with EGS OAuth API
5. Update EGS config in `%APPDATA%` with new refresh token
6. Check installed game version against version list from EGS API
7. Obtain game OAuth token
8. Launch Game with online authentication parameters

## How to compile the .exe

The exe in releases was built using PyInstaller using the following command:
```
py -3 -O -m PyInstaller --onefile src\rktlnch.py
```
The only other dependency that is required to run rktlnch is `requests`.

## What about Linux/Mac?

Since rktlnch relies on EGS being installed to work it wouldn't directly work on Linux. However I'm sure somebody could adapt the underlying authentication process to work from within e.g. Lutris to launch EGS games on Linux. You would just need some kind of way to obtain the login credentials. 

While I am a recreational Linux user I have no idea about anything macOS, sorry.
