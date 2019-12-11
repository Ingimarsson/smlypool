# smlypool - Mining pool for Smileycoin

smlypool is a scrypt based mining pool for smileycoin. 

## Installation

Install programs

    sudo apt install python3
    sudo apt install pip
    sudo apt install python3-venv

Create and enter a virtualenv

    python3 -m venv env
    source env/bin/activate

Install the required packages

    (env) ~$ pip install -r requirements.txt

Run the server

    (env) ~$ python manage.py runserver

## Mining with bfgminer

## To-do list

 - Coinbase creation function (CHECK)
 - Get GBT from wallet. (CHECK)
   - Store as django model
 - Create block template for miners
   - Check if wallet GBT has changed
   - Assign a unique number to coinbase data
   - Calculate Merkle root
   - Construct JSON response
 - Submit block validation
