import vihollinen


class Peli:
    def __init__(self, gamerID, yhteys):
        self.gamerID = gamerID
        self.yhteys = yhteys
        self.viholliset = []
        self.pisteet = 0
        self.polttoaine = 100
        self.hp = 3
        self.havinnyt = False

    def tietokanta_siirto(self):
        sql = f"update player set points={self.pisteet}, hp={self.hp}, fuel={self.polttoaine} where ID='{self.gamerID}'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)

        sql = f"update enemy, player set e1='{self.viholliset[0].tyyppi}',e2='{self.viholliset[1].tyyppi}',e3='{self.viholliset[2].tyyppi}',e4='{self.viholliset[3].tyyppi}',e5='{self.viholliset[4].tyyppi}', e1_moves={self.viholliset[0].siirrot},e2_moves={self.viholliset[1].siirrot},e3_moves={self.viholliset[2].siirrot},e4_moves={self.viholliset[3].siirrot},e5_moves={self.viholliset[4].siirrot} where player.ID='{self.gamerID}' AND enemy.enemy_ID=player.ID"
        kursori.execute(sql)


    def tee_vihollislista(self):
        tmp = []
        for vihollinen in self.viholliset:
            tmp.append([vihollinen.tyyppi, vihollinen.siirrot])
        return tmp

    def hae_viholliset(self):
        sql = f"select e1, e1_moves, e2, e2_moves, e3, e3_moves, e4, e4_moves, e5, e5_moves from enemy, player where player.ID='{self.gamerID}' AND enemy.enemy_ID=player.ID"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)
        tmp = kursori.fetchone()
        print(self.gamerID)
        for i in range(0, 10, 2):
            self.viholliset.append(vihollinen.Vihollinen(tmp[i], tmp[i+1]))

    def hae_pisteet(self):
        sql = f"select points from player where player.ID='{self.gamerID}'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)
        tmp = kursori.fetchone()
        self.pisteet = tmp[0]

    def hae_polttoaine(self):
        sql = f"select fuel from player where player.ID='{self.gamerID}'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)
        tmp = kursori.fetchone()
        self.polttoaine = tmp[0]

    def hae_hp(self):
        sql = f"select hp from player where player.ID='{self.gamerID}'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)
        tmp = kursori.fetchone()
        self.hp = tmp[0]


    def lisaa_vihollinen(self, n):
        for i in range(n):
            uusi_vihollinen = vihollinen.Vihollinen('peukaloinen', 2)
            uusi_vihollinen.anna_tyyppi()
            uusi_vihollinen.anna_siirrot()
            uusi_vihollinen.anna_heikkous()
            self.viholliset.append(uusi_vihollinen)

    def tuhoa_vihollinen(self, sijainti, pelaaja):
        tiedot = pelaaja.hae_tiedot(sijainti)
        for vihollinen in self.viholliset:
            if vihollinen.tyyppi == 'peukaloinen':
                if tiedot[3] == 'large_airport':
                    self.viholliset.remove(vihollinen)
                    self.pisteet += vihollinen.pistemaara
                    break
            elif vihollinen.tyyppi == 'jättiläinen':
                if tiedot[3] == 'small_airport' or tiedot[3] == 'heliport':
                    self.viholliset.remove(vihollinen)
                    self.pisteet += vihollinen.pistemaara
                    break
            elif vihollinen.tyyppi == 'jäämies':
                if tiedot[0] < 62.242603:
                    self.viholliset.remove(vihollinen)
                    self.pisteet += vihollinen.pistemaara
                    break
            elif vihollinen.tyyppi == 'tuliukko':
                if tiedot[0] > 65.012093:
                    self.viholliset.remove(vihollinen)
                    self.pisteet += vihollinen.pistemaara
                    break
            elif vihollinen.tyyppi == 'hujoppi':
                if tiedot[2] < 311:
                    self.viholliset.remove(vihollinen)
                    self.pisteet += vihollinen.pistemaara
                    break
            elif vihollinen.tyyppi == 'pätkä':
                if tiedot[2] > 311:
                    self.viholliset.remove(vihollinen)
                    self.pisteet += vihollinen.pistemaara
                    break
        if len(self.viholliset) < 5:
            self.lisaa_vihollinen(1)

        for vihollinen in self.viholliset:
            if vihollinen.siirrot <= 0:
                self.viholliset.remove(vihollinen)
                self.lisaa_vihollinen(1)


