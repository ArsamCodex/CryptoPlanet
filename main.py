import datetime
import io
from datetime import datetime
import mysql.connector
import numpy as np
from django.shortcuts import redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from flask import Flask, render_template, request, Response, url_for
import requests
import pandas as pd
import matplotlib.pyplot as plt

import json
import pandas_datareader.data as pdr
import plotly.offline as py
import plotly.graph_objs as go





app = Flask(__name__)



#https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical
# List of all blokchain network
#https://api.coingecko.com/api/v3/asset_platforms
#https://api.coingecko.com/api/v3/search?query=bitcoin  info about coin
#Trending coin https://api.coingecko.com/api/v3/search/trending
#https://api.coingecko.com/api/v3/companies/public_treasury/bitcoin companys btc hold

#chart info 1H
#https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=50







@app.route('/')
def homePage():
    global each_crypto_id, cryotSymbol, cryptoIdEth, curentRateEth, cryptoSymbolEth, cryptoIdUsdt, curentRateUsdt, cryptoSymbolUsdt, cryptoIdBnbt, curentRateBnb, cryptoSymbolBnb, cryptoIdxrp, curentRatexrp, cryptoSymbolxrp

    coin_information = json.loads(requests.get('https://api.coincap.io/v2/rates').content).get('data')

    current_rate = 0

    for coin in coin_information:
        if coin.get('symbol') == 'BTC':
            current_rate = float(coin.get('rateUsd'))
            each_crypto_id = coin.get('id')
            cryotSymbol = coin.get('symbol')
        elif coin.get('symbol') == 'ETH':
            curentRateEth = float(coin.get('rateUsd'))
            cryptoIdEth = coin.get('id')
            cryptoSymbolEth  = coin.get('symbol')
            print(cryptoSymbolEth,cryptoIdEth,curentRateEth)
        elif coin.get('symbol') == 'USDT':
            curentRateUsdt = float(coin.get('rateUsd'))
            cryptoIdUsdt = coin.get('id')
            cryptoSymbolUsdt = coin.get('symbol')
        elif coin.get('symbol') == 'BNB':
            curentRateBnb = float(coin.get('rateUsd'))
            cryptoIdBnbt = coin.get('id')
            cryptoSymbolBnb = coin.get('symbol')


    df_line = pd.DataFrame([[each_crypto_id.upper(), datetime.utcnow(), current_rate, cryotSymbol],
                            [cryptoIdEth.upper(), datetime.utcnow(), curentRateEth, cryptoSymbolEth],
                            [cryptoIdUsdt.upper(), datetime.utcnow(), curentRateUsdt, cryptoSymbolUsdt],
                            [cryptoIdBnbt.upper(), datetime.utcnow(), curentRateBnb, cryptoSymbolBnb],
                            ],
                           columns=['id', 'time', 'rate', 'symbol'])
    last_update_time = datetime.utcnow()

    print(df_line)

    return render_template("index.html", content=current_rate,btc=each_crypto_id.upper(),price=current_rate,symbol=cryotSymbol,ethName=cryptoSymbolEth,ethSymbol=cryptoIdEth.upper(),ethPrice=curentRateEth,usdtName=cryptoIdUsdt.upper(),usdtSymbol=cryptoSymbolUsdt,usdtPrice=curentRateUsdt
                           ,bnbName=cryptoIdBnbt.upper(),bnbSymbol=cryptoSymbolBnb,bnbPrice=curentRateBnb
                           ,time=datetime.utcnow(),info=current_rate,info2=curentRateEth,info3=curentRateUsdt,info4=curentRateBnb)


@app.route('/login/',methods=['POST','GET'])
def login():
    dataBase = mysql.connector.connect(
        host="localhost",
        user="root",
        password="0",
        database="messages"
    )
    username  = request.form.get('username')
    message = request.form.get('message')

    mycursor = dataBase.cursor()


    sql = "INSERT INTO messages (name, message) VALUES (%s, %s)"
    val = (username , message)

    mycursor.execute(sql, val)
    dataBase.commit()
    dataBase.close()
    s = 'Your Message Has Been Sented'


    return render_template("login.html",message=[val,s])


@app.route('/btcownchart',methods=['POST','GET'])
def btcGraph():
     start = datetime.datetime(2020,1,1)
     end  = datetime.datetime(2022,4,1)
     df = pdr.DataReader('BTC-USD','yahoo',start,end)

     data = [go.Candlestick(x=df.index,
                            open=df.Open,
                            high=df.High,
                            low=df.Low,
                            close=df.Close)]

     layout = go.Layout(title='Bicoin CryptoPlanet Chart',
                        xaxis={'rangeselector': {'buttons': [{'count': 7,
                                                              'label': '1w',
                                                              'step': 'day',
                                                              'stepmode': 'backward'},
                                                             {'count': 1,
                                                              'label': '1m',
                                                              'step': 'month',
                                                              'stepmode': 'backward'},
                                                             {'count': 3,
                                                              'label': '3m',
                                                              'step': 'month',
                                                              'stepmode': 'backward'},
                                                             {'count': 6,
                                                              'label': '6m',
                                                              'step': 'month',
                                                              'stepmode': 'backward'},
                                                             {'count': 1,
                                                              'label': '1y',
                                                              'step': 'year',
                                                              'stepmode': 'backward'},
                                                             ]
                                                 },
                               'rangeslider': {'visible': True}})

     fig = go.Figure(data=data, layout=layout)

     fig8 = py.plot(fig)


     # return tt

     return render_template("bitcoin.html")









@app.route('/trend')
def trending():
    global trendName, trendSymbol, trendId, trendm, trend
    trendingcoinsInformation = json.loads(requests.get('https://api.coingecko.com/api/v3/search/trending').content).get('coins')

    for trend in trendingcoinsInformation:
        if trend.get('id') == 'radix':

         print(trend)
    df_line2 = pd.DataFrame([[trendm]], columns=['name'])
    print(df_line2)

    return render_template("trandingcoins.html", trending=trend)








@app.route('/email/', methods=['POST', 'GET'])
def email1():







    return render_template("email.html")

@app.route('/tel/', methods=['POST', 'GET'])
def tel():
    return render_template("tel")



# @app.route('/header')
#
# def header_construct():
#
#
#
#     market_info = "https://api.coin360.com/global/latest"
#     marketInfo = requests.get(market_info)
#     header = marketInfo.json()
#
#     return header


@app.route('/api/' , methods=['POST', 'GET'])
def api():
    return render_template("api.html")

@app.route('/test')
#This is going to initialize footer section , or simple way it give to footer values
def footer_construct():
    footerinfo =  "https://api.coingecko.com/api/v3/asset_platforms"
    info = requests.get(footerinfo)
    footer = info.text

    print(footer)
    return footer

@app.route('/test2')
def test2():



    with open('ids.txt') as json_file:
        data = json.load(json_file)
        store_list = []
        for item in data:
            store_details = {"id": None}

            store_details['id'] = item['id']


            store_list.append(store_details)
            store_list2 = store_list
            print(store_list2[-1])
            # print(store_list2)
            storelistvertical = store_list2[-1]

            # factom1 = store_list2[0]




        # print(store_list2)
    return render_template("test.html" , test=store_list2 , headerr=storelistvertical)

@app.route('/btcchart')
def btcChart():
    return render_template("bitcoin.html")



@app.route('/lastadded')
def lastListingCryptos():
    global data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/new'
    parameters = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'b4666977-739e-47bd-8ad6-02ad69bfd85f',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    return render_template("lastcoins.html",recentlly=data)



plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
@app.route('/print-plot')
def plot_png():

   fig = Figure()
   axis = fig.add_subplot(1, 1, 1)
   xs = np.random.rand(100)
   ys = np.random.rand(100)
   axis.plot(xs, ys)
   output = io.BytesIO()
   FigureCanvas(fig).print_png(output)
   return Response(output.getvalue(), mimetype='image/png')

@app.route('/transactions/', methods=['GET'])
def AnonymouseTransactionsETH():
    '''''at the time just return empty page we fill it up later '''
    return render_template('transaction.html')



@app.route('/wallet1/', methods=['GET'])
def wallet1():
    '''''at the time just return empty page we fill it up later '''
    return render_template('wallet.html')



@app.route('/ercgenerate/', methods=['GET','POST'])
def generateERC20Address():
    global priv, acct
    from web3 import Web3



    infura_url = "https://mainnet.infura.io/v3/7892bc8457dd4b1389ffe11107e7bb08"
    web3 = Web3(Web3.HTTPProvider(infura_url))
    # print(web3)
    # print(web3.isConnected())
    #
    # print(web3.eth.blockNumber)

    # # Fill in your account here
    # balance = web3.eth.getBalance("0x6dcf3C877bDeEA62C2683C1653A2495310793f71")
    # print(web3.fromWei(balance, "ether"))

    from eth_account import Account
    import secrets

    username = request.form.get('username')
    if username is None:
        return render_template("wallet.html")
    else:

        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        print("SAVE BUT DO NOT SHARE THIS:", private_key)
        acct = Account.from_key(private_key)
        print("Address:", acct.address)

    return render_template("wallet.html", privateKey=priv , Walletaddress=acct.address)







#
#
# @app.route('/db')
# def testDatabase():
#
#     mydb= mysql.connector.connect(host='localhost',
#                             database='python',
#                             user='root',
#                             password='0')
#
#     mycursor = mydb.cursor()
#     sql = "INSERT INTO Student (Name, Roll) VALUES (%s, %s)"
#     val = ("Ram", "85")
#
#     mycursor.execute(sql, val)
#     mydb.commit()
#
#     print(mycursor.rowcount, "details inserted")
#     toShow = mycursor.rowcount + 'data'+ val+'Onserted To DAtabase'
#
#     # disconnecting from server
#     mydb.close()
#
#     CONFIRM = 'iTSoK'
#
#
#     return render_template("db.html" , db=[toShow])
#
#

# @app.route('/eth')
# def ethereumGenerator():
#
#     coin_information = json.loads(requests.get('https://api.coincap.io/v2/rates').content).get('data')
#     # print(response2.json())
#
#
#     for coin in coin_information:
#         if coin.get('symbol') == 'ETH':
#          current_rate2 = float(coin.get('rateUsd'))
#          return current_rate2
#
#
#





    # return print(p['id'])

    # url1= requests.get('https://api.coingecko.com/api/v3/asset_platforms')
    # load_cdata = json.loads(url1)


    # f = urllib.urlopen("http://domain/path/jsonPage")
    # values = json.load(f)
    # f.close()
    # print(f)
    # return f

    # coininfoinmerhod = list.loads(requests.get('https://api.coingecko.com/api/v3/asset_platforms').content).get('data')
    #
    # converttojson = json.dumps(coininfoinmerhod)
    # print(converttojson)

    # for blokchain in converttojson:
    #
    #     if blokchain.get('id') == 'cosmos':
    #         id2 =blokchain.get('id')
    #         footerData2 = pd.DataFrame([[id2]],columns=['id'])
    # print(id2)
    #
    # return id2
# @app.route('/save')
# def saveDataTotext():
#     f = requests.get('https://api.coingecko.com/api/v3/asset_platforms')
#     with open('ids.txt', 'w') as fd:
#         fd.write(f.text)

    # while True:
    #     global footer
    #     footerInfoLink = "https://api.coingecko.com/api/v3/asset_platforms"
    #     footerIno = requests.get(footerInfoLink)
    #     footer = footerIno.json()
    #     print(footer)
    #     return footer








# def coinmarketCapAPI():
#     url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#     parameters = {
#         'start': '1',
#         'limit': '5000',
#         'convert': 'USD'
#     }
#     headers = {
#         'Accepts': 'application/json',
#         'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c',
#     }
#
#     session = Session()
#     session.headers.update(headers)
#
#     try:
#         response = session.get(url, params=parameters)
#         data = json.loads(response.text)
#         print(data)
#     except (ConnectionError, Timeout, TooManyRedirects) as e:
#         print(e)


if __name__ == "__main__":
    app.run(debug=True)
