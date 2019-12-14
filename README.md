# smlypool - Mining pool for Smileycoin

smlypool is a scrypt based mining pool for smileycoin. The purpose of this project was to understand the protocols behind mining pools and develop a functional prototype.

A detailed report on this project can be found [here](paper/main.pdf).

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

Edit the RPC username, password and port settings found in settings.py

Run the server

    (env) ~$ python manage.py runserver

Test the server by opening http://localhost:8000/info

## Mining with bfgminer

If the mining pool is running you should be able to start mining. We tested the pool with an ASIC miner called FutureBit Moonlander 2 using the following command.

    $ bfgminer --scrypt -o http://pool.binni.org:8000 -u [address] -p y -S ALL --set MLD:clock=600 --no-getwork --no-stratum

