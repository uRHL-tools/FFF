# Font-Family Finder (FFF)

Script to retrieve all the different font-families employed in a web page. 

## Quick usage (JavaScript)

1. Navigate to the desired URL using your favorite browser. 
2. Open DevTools (from option menu or pressing F12).
3. Paste the [following code](source/quick_fff.js) in the console and press enter

## Advanced usage

Follow this guide to install GetFF in your computer.

### Installation

> Python 3 is required. Download it from the [official page](https://www.python.org/downloads/)

```cmd
# 1. Clone the repo, either via Git or download zip
git clone https://github.com/uRHL-tools/FFF
# TODO: windows
# Linux
cd FFF
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### Usage

> Remember to activate the virtual environment before executing
 
```cmd
# To enable virtual environment
source venv/bin/activate
# Windows
python __main__.py -h

# Linux
python3 __main__.py -h
```


