from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    vorname = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=50, blank=True)
    balance = models.FloatField(default=0)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#    def __init__(self, user, *args, **kwargs):
#        self.user = user
#        super(RSVPForm, self).__init__(*args, **kwargs)


## Die Aktien
class Shares(models.Model):
    art = models.CharField(max_length=20)
    kürzel = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    wert = models.FloatField(default=0)
    close = models.FloatField(default=0)
    plus = models.FloatField(default=0)
    prozent = models.FloatField(default=0)
    lowhigh = models.CharField(max_length=50)
    jahrlowhigh = models.CharField(max_length=50)
    openclose = models.CharField(max_length=50)
    dividende = models.FloatField(default=0)
    '''dividendedate = models.DateField(_("Date"), default=datetime.date.today)'''
    volumen = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def getvalue(self):
        return self.wert


## Die gehaltenen Aktien
class Holders(models.Model):
    share = models.ForeignKey(Shares, on_delete=models.CASCADE) #abhängig von aktie, on delete löscht alle anhängende dateien
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    anzahl = models.FloatField(default=0)
    wert_aktuell = models.FloatField(default=0)
    wert_schnitt = models.FloatField(default=0)
    gewinn = models.FloatField(default=0)
    prozent = models.FloatField(default=0)


    def __str__(self):
        return str(self.share.name)+"_"+str(self.user)


## Die gehaltenen Aktien
class Raise(models.Model):
    share = models.ForeignKey(Shares, on_delete=models.CASCADE) #abhängig von aktie, on delete löscht alle anhängende dateien
    anzahl = models.FloatField(default=0)
    wert_aktuell = models.FloatField(default=0)
    wert_schnitt = models.FloatField(default=0)
    gewinn = models.FloatField(default=0)
    prozent = models.FloatField(default=0)
    gebuehren = models.FloatField(default=0)
    kursgewinn = models.FloatField(default=0)


    def __str__(self):
        return str(self.share.name)


## Kaufaufträge
class Buy(models.Model):
    aktie = models.ForeignKey(Shares, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    buy_value = models.FloatField(default=0)
    buy_volume = models.FloatField(default=0)
    gebuehren = models.FloatField(default=0)
    
    def __str__(self):
        return self.aktie.name


## Verkaufaufträge #### muss immer gleich sein wie Buy
class Sell(models.Model):
    aktie = models.ForeignKey(Shares, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    buy_value = models.FloatField(default=0)
    buy_volume = models.FloatField(default=0)
    gebuehren = models.FloatField(default=0)

    def __str__(self):
        return self.aktie.name


## Plan
class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.ForeignKey(Shares, on_delete=models.CASCADE)
    day = models.IntegerField(default=0)
    volume = models.FloatField(default=0)
    value = models.FloatField(default=0) #aktuell

    def __str__(self):
        return str(self.user)+"_"+str(self.share.name)


        
## History
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monat = models.CharField(max_length=30)
    wert = models.FloatField(default=0) #Anfang Monat
    gewinn = models.FloatField(default=0)

    def __str__(self):
        return str(self.user)+"_"+str(self.monat)


## Favoriten
class Favoriten(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aktie = models.ForeignKey(Shares, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.aktie.name)+"_"+str(self.user)