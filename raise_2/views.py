from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Shares, Buy, User, Holders, Profile, Plan, History, Sell, Raise, Favoriten
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm, TradeForm, LoginForm, PlanForm, PlanTagForm
from django.db.models import Avg, Count, Min, Sum
#import pandas_datareader.data as web #for pandas
import datetime #for pandas
import requests_cache #for pandas
#import matplotlib.pyplot as plt
#from matplotlib import style
import requests 
import  time
from django.contrib import messages
import json
#import gviz_api
import math


# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ROG.VX&interval=15min&apikey=I0QZAT30WNKVI2YE
API_KEY = 'I0QZAT30WNKVI2YE'  # für alphavantage (gratis)
BEP = 500
GEBUEHR = 0.01



###### Seiten ######

# Zur Startseite
def index(request):
    return render(request, 'raise_2/main_page.html')

# zu mein Konto
def mein_konto(request):
    my_shares_list = Holders.objects.filter(user = request.user.id)
    if my_shares_list:
        for object in my_shares_list:
            f = Shares.objects.get(id=object.share.id)
            object.wert_aktuell = f.wert * object.anzahl
            object.gewinn = object.wert_aktuell - object.wert_schnitt
            object.prozent = object.gewinn/object.wert_schnitt*100
            object.save()
            object.wert_aktuell = round(object.wert_aktuell, 2)
            object.anzahl = round(object.anzahl, 2)
            object.wert_schnitt = round(object.wert_schnitt, 2)
            object.gewinn = round(object.gewinn, 2)
            object.prozent = round(object.prozent, 2)
        profile = request.user.profile
        profile.balance = round(profile.balance,2)
        total_wert = Holders.objects.filter(user = request.user.id).aggregate(value = Sum('wert_aktuell')) 
        total_gewinn = Holders.objects.filter(user = request.user.id).aggregate(value = Sum('gewinn')) 
        total_prozent = total_gewinn.get('value')/(total_wert.get('value')-total_gewinn.get('value'))*100
        total_wert = round(total_wert.get('value'),2)
        total_gewinn = round(total_gewinn.get('value'),2)
        buy_list = Buy.objects.filter(user = request.user.id)
        sell_list = Sell.objects.filter(user = request.user.id)
    else:
        total_wert = 0 
        total_gewinn = 0
        total_prozent = 0
        profile = request.user.profile
        profile.balance = round(profile.balance,2)
        buy_list = Buy.objects.filter(user = request.user.id)
        sell_list = Sell.objects.filter(user = request.user.id)

    #chart
    chart_list = []
    chart_list.append(['Aktie', 'Wert'])
    for file in my_shares_list:
        chart_list.append([ file.share.name , float(file.wert_aktuell) ])

    context = {
        'my_shares_list': my_shares_list,
        'profile': profile,
        'buy_list': buy_list,
        'sell_list': sell_list,
        'total_wert': total_wert,
        'total_gewinn': total_gewinn,
        'total_prozent': round(total_prozent,2),
        'chart_list': json.dumps(chart_list),
        }
    return render(request, 'raise_2/mein_konto.html', context)



# zu RAISE
def raise_main(request):
    my_shares_list = Raise.objects.all()
    if my_shares_list:
        for object in my_shares_list:
            f = Shares.objects.get(id=object.share.id)
            object.wert_aktuell = f.wert * object.anzahl
            object.gewinn = object.wert_aktuell - object.wert_schnitt
            if object.wert_schnitt != 0:
                object.prozent = object.gewinn/object.wert_schnitt*100
            object.save()
            object.wert_aktuell = round(object.wert_aktuell, 2)
            object.anzahl = round(object.anzahl, 2)
            object.wert_schnitt = round(object.wert_schnitt, 2)
            object.gewinn = round(object.gewinn, 2)
            object.prozent = round(object.prozent, 2)
            object.gebuehren = round(object.gebuehren, 2)
        total_wert = Raise.objects.all().aggregate(value = Sum('wert_aktuell')) 
        total_gewinn = Raise.objects.all().aggregate(value = Sum('gewinn')) 
        if (total_wert.get('value')-total_gewinn.get('value')) != 0:
            total_prozent = total_gewinn.get('value')/(total_wert.get('value')-total_gewinn.get('value'))*100
        else:
            total_prozent =0
        total_gebuehren = Raise.objects.all().aggregate(value = Sum('gebuehren')) 
        total_kursgewinn = Raise.objects.all().aggregate(value = Sum('kursgewinn')) 
        total_balance = Profile.objects.all().aggregate(value = Sum('balance')) 
        total_aktienwert = Holders.objects.all().aggregate(value = Sum('wert_aktuell')) 
        total_wert = round(total_wert.get('value'),2)
        total_gewinn = round(total_gewinn.get('value'),2)
        total_gebuehren = round(total_gebuehren.get('value'),2)
        total_kursgewinn = round(total_kursgewinn.get('value'),2)
        total_balance = round(total_balance.get('value'),2)
        total_aktienwert = round(total_aktienwert.get('value'),2)
    else:
        total_wert = 0
        total_gewinn =  0
        total_prozent =  0
        total_gebuehren =  0
        total_kursgewinn = 0
        total_balance =  0
        total_aktienwert = 0
    #chart
    chart_list = []
    chart_list.append(['Aktie', 'Wert'])
    for file in my_shares_list:
        chart_list.append([ file.share.name , float(file.wert_aktuell) ])

    context = {
        'my_shares_list': my_shares_list,
        'total_wert': total_wert,
        'total_gewinn': total_gewinn,
        'total_prozent': round(total_prozent,2),
        'total_gebuehren': total_gebuehren,
        'total_kursgewinn': total_kursgewinn,
        'chart_list': json.dumps(chart_list),
        'total_balance': total_balance,
        'total_aktienwert': total_aktienwert,
        }
    return render(request, 'raise_2/raise.html', context)



# zu favoriten
def favoriten(request):
    shares_list = Favoriten.objects.filter(user = request.user)
    context = {'shares_list': shares_list}
    return render(request, 'raise_2/favoriten.html', context)


def favorisieren(request, id):
    try:
        f = Favoriten.objects.get(user = request.user, aktie = id)
        f.delete()
    except:
        f= Favoriten()
        f.user = request.user
        f.aktie = Shares(id)
        f.save()
    return redirect('/raise_2/wertschrift/'+ str(id) + '/')

# zu market
def market(request):
    shares_list = Shares.objects.order_by('name')
    context = {'shares_list': shares_list}
    return render(request, 'raise_2/market_layout.html', context)

# wertschriftenseite
def wertschrift(request, id):
    '''shares_list = Shares.objects.all()[:50]
    context = {'shares_list': shares_list}'''
    thisshare = Shares.objects.get(id=id) # diese aktie laden
    value = 00
    #chart_list = getchart(thisshare.kürzel)
    context = {
        'thisshare': thisshare,
        'value': value,
        #'chart_list': chart_list
        }  # übergabe an html
    return render(request, 'raise_2/wertschrift.html', context)

# zu mein Plan
def plan(request):
    my_shares_list = Plan.objects.filter(user = request.user.id)
    for object in my_shares_list:
        f = Shares.objects.get(id=object.share.id)
        object.volume = round( object.value / f.wert, 2)
        object.save()
    chart_list = []
    chart_list.append(['Aktie', 'Wert'])
    for file in my_shares_list:
        chart_list.append([ file.share.name , float(file.value) ])
    summe = Plan.objects.filter(user = request.user.id).aggregate( value = Sum('value'))

    if request.method == 'POST':
        form = PlanTagForm(request.POST)
        if form.is_valid():   # einen Buy Auftrag erstellen
            plan_liste = Plan.objects.filter(user = request.user.id)

            for object in plan_liste:
                object.day = form.cleaned_data.get('Tag')
                object.save()
            return redirect('/raise_2/plan')
    else:
        form = PlanTagForm()

    context = {'my_shares_list': my_shares_list,
        'chart_list': json.dumps(chart_list),
        'gesamtwert': summe.get('value'),
        'form': form}
    return render(request, 'raise_2/plan.html', context)

# zu einstellungen, mit preis aktualisierung test (funkioniert nicht mehr)
def einstellungen(request):
    getprice()
    # dataForAllDays = context['Time Series (Daily)']
    # dataForAllDays = dataForAllDays[datetime.date.all_weekdays()]
    # # dataForSingleDate = dataForAllDays[datetime.date.today().strftime("%Y-%m-%d")]
    # # print(dataForSingleDate['1. open'])
    # # print(dataForSingleDate['2. high'])
    # # print(dataForSingleDate['3. low'])
    # print(dataForAllDays['4. close'])
    # # print (dataForSingleDate['5. volume'])
    # # contextt = dataForSingleDate
    # print( datetime.date.today() )
    # start = datetime.datetime(2018, 1, 1)
    # end = datetime.datetime(2018, 1, 27)
    # expire_after = datetime.timedelta(days=3)
    # session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)
    # df = web.DataReader("TSLA", 'yahoo', start, end, session=session)
    # df.ix['2018-01-04']
    # context = {'data_frame': df.to_dict()}
    # print(context) 
    #print(contextt)
    return render(request, 'raise_2/einstellungen.html')

def deleteplan(request, id):
    p = Plan.objects.get(id = id)
    p.delete()
    return redirect('/raise_2/plan')


def deletefavorit(request, id):
    p = Favoriten.objects.get(id = id)
    p.delete()
    return redirect('/raise_2/favoriten')


def deletebuy(request, id):
    p = Buy.objects.get(id = id)
    profile = Profile.objects.get(user = request.user)
    profile.balance += p.buy_value + p.gebuehren
    profile.save()
    p.delete()
    return redirect('/raise_2/mein_konto')


def deletesell(request, id):
    p = Sell.objects.get(id = id)
    p.delete()
    return redirect('/raise_2/mein_konto')


# sign up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.vorname = form.cleaned_data.get('vorname')
            user.profile.name = form.cleaned_data.get('name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/raise_2/mein_konto')
    else:
        form = SignUpForm()
    return render(request, 'raise_2/signup.html', {'form': form})


# handelsfunktion
def trade(request, id):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():   # einen Buy Auftrag erstellen
            s = Shares.objects.get(id=id)
            if form.cleaned_data.get('Art') == 'Buy':
                bb = Buy()
            elif form.cleaned_data.get('Art') == 'Sell':
                bb = Sell()
            #bb = Buy()
            bb.aktie = Shares(id)
            bb.user = request.user
            # menge festlegen und speichern
            if form.cleaned_data.get('Menge') == None:
                # bb.buy_value =  s.wert *  form.cleaned_data.get('Menge') # wert aktuell x menge
                bb.buy_volume = (1-GEBUEHR)*form.cleaned_data.get('Preis') / s.wert
                bb.buy_value = bb.buy_volume * s.wert
                bb.gebuehren = GEBUEHR*form.cleaned_data.get('Preis')
            elif form.cleaned_data.get('Preis') == None:
                bb.buy_volume = form.cleaned_data.get('Menge')
                bb.buy_value = bb.buy_volume * s.wert 
                bb.gebuehren = bb.buy_volume * s.wert * GEBUEHR
            else:
                form = TradeForm()
                return render(request, 'raise_2/form_trade.html', {'form': form, 'aktie': s})
            if form.cleaned_data.get('Art') == 'Buy':
                if bb.buy_value + bb.gebuehren > request.user.profile.balance:
                    print('Get some Money bro!!')
                    return render(request, 'raise_2/form_trade.html', {'form': form, 'aktie': s})
                bb.save()
                p = Profile.objects.get(user = request.user)
                print(p.balance)
                p.balance -= (bb.buy_volume * s.wert + bb.gebuehren)
                print(p.balance)
                p.save()
                collect_raise(id, bb)
                if bb.id != None:
                    collect(id) # function zum Kaufen
            elif form.cleaned_data.get('Art') == 'Sell':
                if bb.buy_volume > Holders.objects.get(user = request.user, share = id).anzahl:
                    print('Get some Money bro!!')
                    return render(request, 'raise_2/form_trade.html', {'form': form, 'aktie': s})
                bb.save()
                collect_sell(id)
            
            return redirect('/raise_2/mein_konto')
    else:
        form = TradeForm()
    return render(request, 'raise_2/form_trade.html', {'form': form, 'aktie': Shares.objects.get(id=id)})




# planfunktion
def plan_form(request, id):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():   # einen Buy Auftrag erstellen
            try:
                bb = Plan.objects.get(share = id, user = request.user)
            except:
                bb = Plan()
            bb.share = Shares(id)
            bb.user = request.user
            s = Shares.objects.get(id=id)
            bb.day = form.cleaned_data.get('Tag')
            # menge festlegen und speichern
            bb.value += form.cleaned_data.get('Preis')
            bb.volume = bb.value / s.wert
            bb.save()
            print(request.user.profile.balance)
            return redirect('/raise_2/plan')
    else:
        form = PlanForm()
    return render(request, 'raise_2/form_plan.html', {'form': form, 'aktie': Shares.objects.get(id=id)})





# HISTORY
def compute(request):
    #history
    history = []
    history.append(['Monat', 'Wert', 'Gewinn'])
    my_history = History.objects.filter(user = request.user.id)
    for file in my_history:
        history.append([ file.monat , float(file.wert), float(file.gewinn) ])
    context = {'history': history}
    return render(request, 'raise_2/history.html', context)





###### Funktionen ######

# Aktienpreise aktualisieren
def getprice():
        for object in Shares.objects.all():
            try:
                r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + object.kürzel + '&apikey=' + API_KEY)
                price = r.json()
                lastupdate = price['Meta Data']['3. Last Refreshed']
                object.wert = round( float( price['Time Series (Daily)'][lastupdate]['4. close'] ), 2) #datetime.date.today().strftime("%Y-%m-%d")
                d = datetime.datetime.strptime(lastupdate, "%Y-%m-%d")
                d = d - datetime.timedelta(days=1) # gestern
                lastclose = datetime.date.strftime(d,"%Y-%m-%d")
                yes = 0
                # suche letzten close wert (zb über feiertage)
                while not yes:
                    try:   
                        p = price['Time Series (Daily)'][lastclose]['4. close']
                        yes=1
                    except:
                        lastclose = datetime.date.strftime(d,"%Y-%m-%d")
                        d = d - datetime.timedelta(days=1)
                object.close = round( float( price['Time Series (Daily)'][lastclose]['4. close'] ), 2)
                object.plus = round( object.wert - object.close, 2)
                object.prozent = round( object.plus/object.close*100 , 2)
                object.save()
                print("loaded " + object.name)
            except:
                print("NOT loaded " + object.name)



def getchart(kürzel):
    try:
        print(kürzel)
        r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + kürzel + '&outputsize=full&apikey=' + API_KEY)
        price = r.json()
        lastupdate = price['Meta Data']['3. Last Refreshed']
        i = 0
        ss=0
        d = datetime.datetime.strptime(lastupdate, "%Y-%m-%d")
        d = d - datetime.timedelta(days=365) # gestern
        lastupdate = datetime.date.strftime(d,"%Y-%m-%d")
        chart_list = []
        chart_list.append(['Datum', 'Wert'])
        while i < 365 :
            try:   
                p = price['Time Series (Daily)'][lastupdate]['4. close']
                chart_list.append([ lastupdate , float(p) ])
                d = datetime.datetime.strptime(lastupdate, "%Y-%m-%d")
                d = d + datetime.timedelta(days=1) # gestern
                lastupdate = datetime.date.strftime(d,"%Y-%m-%d")
                ss = p
                i += 1
            except:
                chart_list.append([ lastupdate , float(ss) ])
                d = datetime.datetime.strptime(lastupdate, "%Y-%m-%d")
                d = d + datetime.timedelta(days=1) # gestern
                lastupdate = datetime.date.strftime(d,"%Y-%m-%d")
                i += 1
        print(chart_list)
        print("charted ")
        return chart_list
    except:
        print("NOT charted ")
    


## Collect Versucht Päckchen zu machen aus der Buy Liste
def collect (aktie_id):
    summe = Buy.objects.filter(aktie = aktie_id).aggregate( value = Sum('buy_volume')) #summe bilden von dieser aktie
    s = Shares.objects.get(id = aktie_id)
    menge = math.ceil(summe.get('value'))-summe.get('value')
    # wenn genug buys zusammenkommen ausführen
    if summe.get('value')*s.wert > BEP:
        set_raise(s,menge, 0)
        for objects in Buy.objects.filter(aktie = aktie_id):
            set_holder(aktie_id, objects)
            set_raise(s, 0, objects.gebuehren)
            Buy.objects.filter(aktie = aktie_id).delete()


## Collect_sell Versucht Päckchen zu machen aus der Buy Liste
def collect_sell (aktie_id):
    summe = Sell.objects.filter(aktie = aktie_id).aggregate( value = Sum('buy_volume')) #summe bilden von dieser aktie
    s = Shares.objects.get(id = aktie_id)
    menge = summe.get('value')-math.floor(summe.get('value'))
    # wenn genug buys zusammenkommen ausführen
    if summe.get('value')*s.wert > BEP:
        set_raise(s,menge,0)
        for objects in Sell.objects.filter(aktie = aktie_id):
            get_holder(aktie_id, objects)
            set_raise(s, 0, objects.gebuehren)
            Sell.objects.filter(aktie = aktie_id).delete()


#collect_raise gibt di aktien von raise zum verkauf 
def collect_raise(id, buy):
    try:
        aktie_raise = Raise.objects.get(share = id)
        print(aktie_raise)
        if buy.buy_volume < aktie_raise.anzahl:
            s = Shares.objects.get(id = id)
            set_holder(id, buy)
            aktie_raise.wert_schnitt -= buy.buy_volume * aktie_raise.wert_schnitt/aktie_raise.anzahl
            aktie_raise.kursgewinn += round(aktie_raise.gewinn * buy.buy_volume/aktie_raise.anzahl,2)
            aktie_raise.anzahl -= buy.buy_volume
            aktie_raise.wert_aktuell = aktie_raise.anzahl * s.wert
            aktie_raise.gewinn = aktie_raise.wert_aktuell - aktie_raise.wert_schnitt
            aktie_raise.prozent = aktie_raise.gewinn/aktie_raise.wert_schnitt*100
            aktie_raise.gebuehren += round(buy.gebuehren,2) 
            aktie_raise.save()
            buy.delete()
    except:
        i=1


## Make a Holder
def set_holder(aktie_id, objects):
    s = Shares.objects.get(id = aktie_id)
    try: # überpfüfen ob dieser Benutzer die aktie schon hat
        hold = Holders.objects.get(share = aktie_id, user = objects.user)
    except:
        hold = Holders()
    hold.share = Shares(aktie_id)
    hold.user = objects.user
    hold.anzahl += objects.buy_volume  #  menge
    hold.wert_aktuell = hold.anzahl * s.wert
    hold.wert_schnitt +=  objects.buy_volume * s.wert + objects.gebuehren
    hold.gewinn = hold.wert_aktuell - hold.wert_schnitt
    hold.prozent = hold.gewinn/hold.wert_schnitt*100
    hold.save()


## Sell from a Holder
def get_holder(aktie_id, objects):
    s = Shares.objects.get(id = aktie_id)
    try: # überpfüfen ob dieser Benutzer die aktie schon hat
        sold = Holders.objects.get(share = aktie_id, user = objects.user)
    except:
        print('Keine Aktie gefunden')
    sold.share = Shares(aktie_id)
    sold.user = objects.user
    sold.wert_schnitt -=  objects.buy_volume * sold.wert_schnitt/sold.anzahl - objects.gebuehren # gewinnprozent bleibt gleich
    sold.anzahl -= objects.buy_volume  #  menge
    sold.wert_aktuell = sold.anzahl * s.wert
    sold.gewinn = sold.wert_aktuell - sold.wert_schnitt
    sold.prozent = sold.gewinn/sold.wert_schnitt*100
    if sold.wert_aktuell<=0.1:
        sold.delete()
    else:
        sold.save()
    p = Profile.objects.get(user = objects.user)
    p.balance += objects.buy_volume * s.wert
    p.save()



## Make a Holder
def set_raise(s, menge, gebuehr):
    try: # überpfüfen ob dieser Benutzer die aktie schon hat
        f = Raise.objects.get(share = s.id)
    except:
        f = Raise()
    f.share = s
    f.anzahl += menge  #  menge
    f.wert_aktuell = f.anzahl * s.wert
    f.wert_schnitt +=  menge * s.wert
    f.gewinn = f.wert_aktuell - f.wert_schnitt
    if f.wert_schnitt != 0:
        f.prozent = f.gewinn/f.wert_schnitt*100
    f.gebuehren += round(gebuehr,2)
    f.save()

