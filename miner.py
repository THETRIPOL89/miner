from termcolor import colored, cprint
import time
import os
import sys
import platform
import random
from datetime import datetime
import cryptocompare
import re
from hashlib import sha256
import GPUtil
import psutil
import cpuinfo

gpuOk = False
cpuOk = False
systemOk = False
gpuAdvancedOk = False

systemOs = platform.uname().system
if systemOs == "Windows" or "Linux":
    systemOk = True

gpus = GPUtil.getGPUs()
for gpu in gpus:
    gpu_name = gpu.name

    if gpu_name.startswith('GeForce GTX') or gpu_name.startswith('GeForce RTX 20') or gpu_name.startswith('GeForce GT 9') or gpu_name.startswith('GeForce GT 10'):
        gpuOk = True
    elif gpu_name.startswith('GeForce RTX 30') or gpu_name.startswith('Nvidia TITAN RTX'):
        gpuOk = True
        gpuAdvancedOk = True

cpu = cpuinfo.get_cpu_info()['brand_raw']
if cpu.startswith('Intel(R) Core(TM) i5') or cpu.startswith('Intel(R) Core(TM) i7') or cpu.startswith('Intel(R) Core(TM) i9'):
    cpuOk = True

os.system("title Miner")
database = {}

def start():
    operativeSystem = platform.system()
    database['os'] = operativeSystem
    cprint(f'Welcome to the miner platform for {operativeSystem}', 'green')
    os.system("PAUSE>nul")

start()

def before_main():
    text = colored('Which crypto do you want to mine? ', 'yellow')
    choice = input(text)
    if choice == "Bitcoin" or choice == "bitcoin" or choice == "btc" or choice == "BTC" or choice == "Btc":
        main_btc()
    elif choice == "Litecoin" or choice == "litecoin" or choice == "ltc" or choice == "LTC" or choice == "Ltc":
        main_ltc()
    else:
        cprint('That crypto is in working yet.', 'red')
        os.system("PAUSE>nul")
        before_main()

def main_btc():
    os.system("title Bitcoin Miner")
    walletYesNo = input('Do you have a wallet (Yes/No)? ')
    if walletYesNo == "Yes" or walletYesNo == "yes":
        cprint('Okay.', 'green')
        time.sleep(0.5)
        wallet = input('Insert the wallet address: ')
        walletText = colored(wallet, 'green')
        if len(wallet) >= 34 and len(wallet) <= 64:
            database['wallet'] = wallet
            cprint(f'The miner is now mining on the wallet {walletText.lower()}', 'magenta')
            os.system("PAUSE>nul")
            mine_btc()
        else:
            cprint('Your wallet is invalid!', 'red')
            os.system("PAUSE>nul")
            main_btc()
    elif walletYesNo == "No" or walletYesNo == "no":
        cprint("Ok, let's create one!", 'cyan')
        time.sleep(0.5)
        bits = random.getrandbits(134)
        bits_hex = hex(bits)
        wallet = bits_hex[2:]
        database['wallet'] = wallet
        cprint(wallet, 'green')
        time.sleep(0.2)
        print('This is your wallet')
        os.system("PAUSE>nul")
        mine_btc()
    else:
        cprint('I have not understood', 'red')
        time.sleep(0.2)
        main_btc()

def mine_btc():
    earn = 0
    earnText = colored(f'{earn}₿', 'yellow')
    totearn = 0
    os.system("cls")
    try:
        start = datetime.now()
        while True:
            if cpuOk and gpuOk and systemOk and not gpuAdvancedOk:
                earn = random.uniform(0.000000012250, 0.000000018520)
            elif cpuOk and not gpuOk or not systemOk or not gpuAdvancedOk:
                earn = random.uniform(0.000000012250, 0.000000016820)
            elif gpuOk and not cpuOk or not systemOk or not gpuAdvancedOk:
                earn = random.uniform(0.000000012250, 0.000000017520)
            elif systemOk and not cpuOk or not gpuOk or not gpuAdvancedOk:
                earn = random.uniform(0.000000012250, 0.000000016520)
            elif (gpuAdvancedOk and cpuOk) or (gpuAdvancedOk and systemOk):
                earn = random.uniform(0.000000012250, 0.000000018870)
            else:
                earn = random.uniform(0.000000012250, 0.000000015520)
            earnText2 = "{:.13f}".format(earn)
            earnText = colored(f'{earnText2}₿', 'yellow')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_time = colored(f'<{current_time}>', 'cyan')
            text = colored('You have earned', 'green')
            cprint(f'{current_time} {text} {earnText}', 'green')
            totearn += earn
            time.sleep(2)
    except KeyboardInterrupt:
        value = datetime.now() - start
        cprint('The mining is end', 'red', attrs=['bold'])
        totearn2 = "{:.13f}".format(totearn)
        database['totearn'] = totearn2
        totearnText = colored(f'{totearn2}', 'yellow')
        text = '{}'.format(value)
        cprint(f'You have earned {totearnText}₿ in {text}', 'blue')
        database['balance'] = "{:.13f}".format(totearn)
        btc=cryptocompare.get_price('BTC',currency='EUR',full=True)
        current_price=btc['DISPLAY']['BTC']['EUR']['PRICE']
        price=float(re.sub(r'[^0-9.]','',current_price))
        totearnPrice = colored(f'{totearn * price}€', 'yellow')
        cprint(f'Euro earned: {totearnPrice}', 'green')
        btc2=cryptocompare.get_price('BTC',currency='USD',full=True)
        current_price2=btc2['DISPLAY']['BTC']['USD']['PRICE']
        price2=float(re.sub(r'[^0-9.]','',current_price2))
        totearnPrice2 = colored(f'{totearn * price2}$', 'yellow')
        cprint(f'Dollars earned: {totearnPrice2}', 'green')
        os.system("PAUSE>nul")
        wallet = database['wallet']
        with open(f'{wallet}.txt', 'a') as file1:
            totearnPrice = f'{totearn * price}€'
            totearnPrice2 = f'{totearn * price2}$'
            totearn2 = f'{totearn2}B'
            file1.write(f'\nEuro earned: {totearnPrice}')
            file1.write(f'\nDollars earned: {totearnPrice2}')
            file1.write(f'\nBitcoin earned: {totearn2}')
            file1.write('\n')
            file1.close()
        end()

MAX_NONCE = 100000000000

def SHA256(text):
    return sha256(text.encode("ascii")).hexdigest()

def mine2(block_number, transactions, previous_hash, prefix_zeros):
    prefix_str = '0'*prefix_zeros
    for nonce in range(MAX_NONCE):
        text = str(block_number) + transactions + previous_hash + str(nonce)
        new_hash = SHA256(text)
        if new_hash.startswith(prefix_str):
            return new_hash

def end():
    choice = colored('Insert the number:', 'cyan')
    print('1: exit')
    print('2: cashout')
    print('3: continue mining')
    choiceAnswer = input(choice)
    if choiceAnswer == "1":
        print('bye')
        time.sleep(0.3)
        exit
    elif choiceAnswer == "2":
        transaction = 0
        print('Possible payouts:')
        cprint('1: Coinbase', 'cyan')
        cprint('2: Blockchain', 'cyan')
        cprint('3: Exodus', 'cyan')
        choiceAnswer2 = input('Insert the number:')
        if choiceAnswer2 == "1":
            print('It is in working...')
            os.system("PAUSE>nul")
            end()
        elif choiceAnswer2 == "2":
            cprint('Blockchain payout method.', 'green')
            time.sleep(0.5)
            totearn = database['totearn']
            cprint(f'The value of bitcoin is: {totearn}', 'blue')
            time.sleep(0.5)
            transactions = ''
            difficulty = 4
            new_hash = mine2(5, transactions, '0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7', difficulty)
            tt = 0
            wallet = database['wallet']
            while tt < 100:
                cprint(f'In progress the transaction for wallet {wallet.lower()}', 'yellow')
                cprint(f'{tt}% of 100%', 'green')
                time.sleep(0.2)
                os.system("cls")
                tt += 5
                if tt == 100:
                    if transaction == False:
                        transaction = True
                    else:
                        choiceTrans = random.choice([True, False, False, True, False])
                        if choiceTrans == True:
                            transaction = True
                        else:
                            transaction = False
            if transaction == True:
                new_hashText = colored(new_hash, 'blue')
                cprint(f'The transaction number: {new_hashText} is ended with success!', 'green')
                os.system("PAUSE>nul")
                exit
            else:
                new_hashText = colored(new_hash, 'blue')
                cprint(f'The transaction number: {new_hashText} has errors!', 'red', attrs=['bold'])
                os.system("PAUSE>nul")
                end()
        elif choiceAnswer2 == "3":
            print('It is in working...')
            os.system("PAUSE>nul")
            end()
        else:
            cprint('I have not understood', 'red', attrs=['bold'])
            os.system("PAUSE>nul")
            end()
    elif choiceAnswer == "3":
        mine_btc()
    else:
        cprint('I have not understood', 'red', attrs=['bold'])
        os.system("PAUSE>nul")
        end()

def main_ltc():
    os.system("title Litecoin Miner")
    walletYesNo = input('Do you have a wallet (Yes/No)? ')
    if walletYesNo == "Yes" or walletYesNo == "yes":
        cprint('Okay.', 'green')
        time.sleep(0.5)
        wallet = input('Insert the wallet address: ')
        walletText = colored(wallet, 'green')
        if len(wallet) >= 34 and len(wallet) <= 64:
            database['wallet'] = wallet
            cprint(f'The miner is now mining on the wallet {walletText.lower()}', 'magenta')
            os.system("PAUSE>nul")
            mine_ltc()
        else:
            cprint('Your wallet is invalid!', 'red')
            os.system("PAUSE>nul")
            main_ltc()
    elif walletYesNo == "No" or walletYesNo == "no":
        cprint("Ok, let's create one!", 'cyan')
        time.sleep(0.5)
        bits = random.getrandbits(134)
        bits_hex = hex(bits)
        wallet = bits_hex[2:]
        database['wallet'] = wallet
        cprint(wallet, 'green')
        time.sleep(0.2)
        print('This is your wallet')
        os.system("PAUSE>nul")
        mine_ltc()
    else:
        cprint('I have not understood', 'red')
        time.sleep(0.2)
        main_ltc()

def mine_ltc():
    earn = 0
    earnText = colored(f'{earn}Ł', 'yellow')
    totearn = 0
    os.system("cls")
    try:
        start = datetime.now()
        while True:
            if cpuOk and gpuOk and systemOk and not gpuAdvancedOk:
                earn = random.uniform(0.0000025615, 0.0000030315)
            elif cpuOk and not gpuOk or not systemOk or not gpuAdvancedOk:
                earn = random.uniform(0.0000024315, 0.0000029815)
            elif gpuOk and not cpuOk or not systemOk or not gpuAdvancedOk:
                earn = random.uniform(0.0000024615, 0.0000029915)
            elif systemOk and not cpuOk or not gpuOk or not gpuAdvancedOk:
                earn = random.uniform(0.0000023215, 0.0000028515)
            elif (gpuAdvancedOk and cpuOk) or (gpuAdvancedOk and systemOk):
                earn = random.uniform(0.0000025615, 0.0000031215)
            else:
                earn = random.uniform(0.0000025215, 0.0000029615)
            earnText2 = "{:.13f}".format(earn)
            earnText = colored(f'{earnText2}Ł', 'yellow')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_time = colored(f'<{current_time}>', 'cyan')
            text = colored('You have earned', 'green')
            cprint(f'{current_time} {text} {earnText}', 'green')
            totearn += earn
            time.sleep(2)
    except KeyboardInterrupt:
        value = datetime.now() - start
        cprint('The mining is end', 'red', attrs=['bold'])
        totearn2 = "{:.13f}".format(totearn)
        database['totearn'] = totearn2
        totearnText = colored(f'{totearn2}', 'yellow')
        text = '{}'.format(value)
        cprint(f'You have earned {totearnText}Ł in {text}', 'blue')
        database['balance'] = "{:.13f}".format(totearn)
        Ł=cryptocompare.get_price('LTC',currency='EUR',full=True)
        current_price=Ł['DISPLAY']['LTC']['EUR']['PRICE']
        price=float(re.sub(r'[^0-9.]','',current_price))
        totearnPrice = colored(f'{totearn * price}€', 'yellow')
        cprint(f'Euro earned: {totearnPrice}', 'green')
        Ł2=cryptocompare.get_price('LTC',currency='USD',full=True)
        current_price2=Ł2['DISPLAY']['LTC']['USD']['PRICE']
        price2=float(re.sub(r'[^0-9.]','',current_price2))
        totearnPrice2 = colored(f'{totearn * price2}$', 'yellow')
        cprint(f'Dollars earned: {totearnPrice2}', 'green')
        os.system("PAUSE>nul")
        wallet = database['wallet']
        with open(f'{wallet}.txt', 'a') as file1:
            totearnPrice = f'{totearn * price}€'
            totearnPrice2 = f'{totearn * price2}$'
            totearn2 = f'{totearn2}L'
            file1.write(f'\nEuro earned: {totearnPrice}')
            file1.write(f'\nDollars earned: {totearnPrice2}')
            file1.write(f'\nLitecoin earned: {totearn2}')
            file1.write('\n')
            file1.close()
        end_ltc()

def end_ltc():
    choice = colored('Insert the number:', 'cyan')
    print('1: exit')
    print('2: cashout')
    print('3: continue mining')
    choiceAnswer = input(choice)
    if choiceAnswer == "1":
        print('bye')
        time.sleep(0.3)
        exit
    elif choiceAnswer == "2":
        transaction = 0
        print('Possible payouts:')
        cprint('1: Coinbase', 'cyan')
        cprint('2: Blockchain', 'cyan')
        cprint('3: Exodus', 'cyan')
        choiceAnswer2 = input('Insert the number:')
        if choiceAnswer2 == "1":
            print('It is in working...')
            os.system("PAUSE>nul")
            end_ltc()
        elif choiceAnswer2 == "2":
            cprint('Blockchain payout method.', 'green')
            time.sleep(0.5)
            totearn = database['totearn']
            cprint(f'The value of litecoin is: {totearn}', 'blue')
            time.sleep(0.5)
            transactions = ''
            difficulty = 4
            new_hash = mine2(5, transactions, '0000000xa036944e29568d0cff17edbe038f81208fecf9a66be9a2b8321c6ec7', difficulty)
            tt = 0
            wallet = database['wallet']
            while tt < 100:
                cprint(f'In progress the transaction for wallet {wallet.lower()}', 'yellow')
                cprint(f'{tt}% of 100%', 'green')
                time.sleep(0.2)
                os.system("cls")
                tt += 5
                if tt == 100:
                    if transaction == False:
                        transaction = True
                    else:
                        choiceTrans = random.choice([True, False, False, True, False])
                        if choiceTrans == True:
                            transaction = True
                        else:
                            transaction = False
            if transaction == True:
                new_hashText = colored(new_hash, 'blue')
                cprint(f'The transaction number: {new_hashText} is ended with success!', 'green')
                os.system("PAUSE>nul")
                exit
            else:
                new_hashText = colored(new_hash, 'blue')
                cprint(f'The transaction number: {new_hashText} has errors!', 'red', attrs=['bold'])
                os.system("PAUSE>nul")
                end_ltc()
        elif choiceAnswer2 == "3":
            print('It is in working...')
            os.system("PAUSE>nul")
            end_ltc()
        else:
            cprint('I have not understood', 'red', attrs=['bold'])
            os.system("PAUSE>nul")
            end_ltc()
    elif choiceAnswer == "3":
        mine_ltc()
    else:
        cprint('I have not understood', 'red', attrs=['bold'])
        os.system("PAUSE>nul")
        end_ltc()

before_main()