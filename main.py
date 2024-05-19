from datetime import datetime
from abc import ABC, abstractmethod


class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def info(self):
        print(f"{self.szobaszam}-s szoba, ára: {self.ar}")

class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, tengerrenez):
        super().__init__(ar, szobaszam)
        self.tengerrenez = tengerrenez

    def info(self):
        print(f"{self.szobaszam}-s szoba, ára: {self.ar}, Tengerre néz: {'igen' if self.tengerrenez else 'nem'}")

class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam, etkezes):
        super().__init__(ar, szobaszam)
        self.etkezes = etkezes

    def info(self):
        print(f"{self.szobaszam}-s szoba, ára: {self.ar}, Reggeli az árban: {'igen' if self.etkezes else 'nem'}")

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def keres_szoba(self, szobaszam):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                return szoba
        print("Nincs ilyen szobaszám a hotelben")
        raise ValueError("Rossz szobaszám")

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def add_foglalas(self, foglalas):
        self.foglalasok.append(foglalas)

    def listazas_foglalas(self):
        print(f"{self.nev} foglalásai:\n")
        for foglalas in self.foglalasok:
            foglalas.info()

    def foglalas(self, szoba, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szoba.szobaszam and foglalas.datum == datum:
                print(f"Az adott napon a {szoba.szobaszam}-s szoba már le van foglalva.")
                return False
        uj_foglalas = Foglalas(szoba, datum)
        self.add_foglalas(uj_foglalas)
        return True

    def foglalas_lemondas(self, szoba, datum):
        for foglalas in self.foglalasok:
            if szoba.szobaszam == foglalas.szoba.szobaszam and datum == foglalas.datum:
                self.foglalasok.remove(foglalas)
                print(f"A {szoba.szobaszam}-s szoba foglalása a {datum.strftime('%Y-%m-%d')} napra sikeresen lemondva.")
                return
        print("A lemondani kívánt foglalás nem létezik.")
        raise ValueError("Nem létező foglalás")

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def info(self):
        self.szoba.info()
        print(f"Dátum: {self.datum.strftime('%Y-%m-%d')} \n")

hotel = Szalloda("Erik Progamozó Szálloda")

egyagyas1 = EgyagyasSzoba(20000, 1, True)
egyagyas2 = EgyagyasSzoba(15000, 2, False)
ketagyas1 = KetagyasSzoba(30000, 3, True)

hotel.add_szoba(egyagyas1)
hotel.add_szoba(egyagyas2)
hotel.add_szoba(ketagyas1)

hotel.add_foglalas(Foglalas(egyagyas1, datetime(2024, 6, 10)))
hotel.add_foglalas(Foglalas(egyagyas1, datetime(2024, 6, 23)))
hotel.add_foglalas(Foglalas(ketagyas1, datetime(2024, 7, 4)))
hotel.add_foglalas(Foglalas(ketagyas1, datetime(2024, 7, 15)))
hotel.add_foglalas(Foglalas(egyagyas2, datetime(2024, 7, 27)))

while True:
    print("\nMit szeretne csinálni?")
    print("1. Foglalások listázása")
    print("2. Szobafoglalás")
    print("3. Foglalás lemondása")
    print("4. Kilépés")

    valasztas = input("Kérem adja meg melyik menüpontot választja: ")

    if valasztas == "1":
        hotel.listazas_foglalas()
    elif valasztas == "2":
        szobaszam = int(input("Add meg a szobaszámot: "))

        try:
            szoba = hotel.keres_szoba(szobaszam)
        except ValueError:
            continue

        datum_str = input("Add meg a foglalás dátumát (YYYY-MM-DD): ")
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            print("Érvénytelen dátumformátum. Kérem YYYY-MM-DD formátumban adja meg a dátumot.")
            continue

        if datetime.now() < datum:
            sikeres = hotel.foglalas(szoba, datum)
            if sikeres:
                print(f"A(z) {szoba.szobaszam}-s számú szoba foglalása sikeres volt a {datum.strftime('%Y-%m-%d')} napra. Ára: {szoba.ar} Ft")
        else:
            print("Érvénytelen dátum. Kérem a jövőbeni dátumot válasszon.")
    elif valasztas == "3":
        szobaszam = int(input("Add meg a szobaszámot: "))

        try:
            szoba = hotel.keres_szoba(szobaszam)
        except ValueError:
            continue

        datum_str = input("Add meg a foglalás dátumát (YYYY-MM-DD): ")
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d")
        except ValueError:
            print("Érvénytelen dátumformátum. Kérem YYYY-MM-DD formátumban adja meg a dátumot.")
            continue

        try:
            hotel.foglalas_lemondas(szoba, datum)
        except ValueError:
            continue

    elif valasztas == "4":
        print("Kilépés...")
        break
    else:
        print("Érvénytelen választás. Kérlek, válassz újra.")