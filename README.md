<h1 align="center">
  <br>
  <img src="https://i.imgur.com/AjjrXQ4.jpg">
  <br>
  Daily Hoyolab Auto Check-in
  <br>
</h1>

# What is it?
This is a simple script for automatic Hoyolab daily check-in.

* Supports **Genshin Impact,** **Honkai Impact 3rd,** **Honkai: Star Rail** and **Zenless Zone Zero**
* Works with multiple Hoyoverse accounts
* Can send discord notifications

# Requirements

* Python 3.x
* pip (python package manager)

# Installation

## 1. Clone this repository...
```
 git clone https://github.com/realw98/hoyolab-auto-checkin.git
```

**or**

download from <a href="https://github.com/realw98/hoyolab-auto-checkin/releases">releases</a> and unpack. It is implied that unpacked sources are in `hoyolab-auto-checkin` folder. 

## 2. Install required modules

Enter new directory
```
cd hoyolab-auto-checkin
```
and create virtual environment (recommended)
```
python -m venv .
```

Then install dependecies.

Linux:
```
./bin/pip3 install -r requirements.txt
```
Windows:
```
.\Scripts\pip3 install -r requirements.txt
``` 
## 3. Copy config_example.json file to config.json

## 4. Set cookies for Hoyolab account

1. Go to the Hoyolab website https://www.hoyolab.com/
2. Login with your account
3. Open the developer tools on your web browser (usually F12 or Ctrl+Shift+i).
4. Go to Application tab, select Cookies at the left, https://www.hoyolab.com.
5. You need three values: `ltoken_v2`,`ltuid_v2` and `ltmid_v2`. Usually ltuid_v2 is a 9-digit number, and ltoken_v2 is a long string starting with v2_. Copy them to appropriate place in config.json.

## 4.1 (Optional) If you have multiple accounts
 If you have multiple accounts, do the same for each account, so `accounts` array in config.json should look like this
```
"accounts": [
  {
    "cookies":
      {
        "ltuid_v2": "123456789",
        "ltoken_v2": "v2_ABCbcdefghiljdsadsad",
        "ltmid_v2": "abcdefg"
      },
    "games": [],
  },
  {
    "cookies": {
      "ltuid_v2": "098765432",
      "ltoken_v2": "v2_abcdefghiljdsadsad",
      "ltmid_v2": "abcdefg"

    },
    "games": [],
  }
]
``` 

## 5. Select games you want to check
  Put game names in `"games"` array in config.json for each account.
 
  Recognizeable game names are:
  - `hk4e_global` for Genshin (global)
  - `bh3_global` for Honkai Imapct 3 (global)
  - `hkrpg_global` for HSR (global)
  - `nap_global` for ZZZ (global).

  Example:
  ```
  "games": ["hk4e_global", "hkrpg_global", "nap_global"],
  ```

```

## 7. (Optional) Setup discord notification
1. Create your own discord server and private channel.
2. Click on channel settings
3. Go into Integrations tab and click "View Webhooks"
4. Create new webhook and copy its URL
5. Paste this URL in **config.json** as `discord_webhook_url`

## 8. Check if it works

Run script manually.

Linux:
```
./bin/python main.py
```
Windows:
```
.\Scripts\python main.py
```

If everything is ok you should see something like this:
<img src="https://i.imgur.com/Z7vmAhH.png"/>


## 9. Setup scheduler (optional)

### For Windows: ###

1. Press Win+R
2. Run **taskschd.msc**
3. Actions -> Create simple task
4. Select python.exe from hoyolab-auto-checkin\Scripts directory as program
5. Use full path to main.py as argument 

### For Linux: ###

**Crontab example**

This will do check-in every day at 6:00am:
```
00 06 * * * /home/username/hoyolab-auto-checkin/bin/python /home/username/hoyolab-auto-checkin/main.py
```

**Systemd service and timer (user)**

```
mkdir -p ~/.config/systemd/user
cp ./systemd/* ~/.config/systemd/user
systemctl --user daemon-reload
systemctl --user enable hoyolab-auto-checkin.timer
```
Run manually to check if it works
```
systemctl --user start hoyolab-auto-checkin.service
systemctl --user status hoyolab-auto-checkin.service
```
Note: in this case you need to be logged in at scheduled time or timer won't run.

**Systemd service and timer (system-wide)**
```
sudo cp ./systemd/* /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable hoyolab-auto-checkin.timer
```
Do not forget to fix path in hoyolab-auto-checkin.service file before installation.

