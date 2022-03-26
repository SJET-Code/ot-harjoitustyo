import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(1000)
    
    def test_uuden_kassapaatteen_saldo_on_oikein(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_uuden_kassapaatteen_myytyjen_luonaiden_maara_on_nolla(self):
        self.assertEqual((self.kassa.edulliset,self.kassa.maukkaat), (0,0))
    
    def test_kateisosto_toimii_kun_rahat_riittavat(self):
        emaksu=self.kassa.syo_edullisesti_kateisella(500)
        mmaksu=self.kassa.syo_maukkaasti_kateisella(500)
        self.assertEqual((self.kassa.edulliset,self.kassa.maukkaat,self.kassa.kassassa_rahaa,emaksu,mmaksu), (1,1,100000+640,260,100))

    def test_kateisosto_toimii_kun_rahat_eivat_riita(self):
        emaksu=self.kassa.syo_edullisesti_kateisella(100)
        mmaksu=self.kassa.syo_maukkaasti_kateisella(100)
        self.assertEqual((self.kassa.edulliset,self.kassa.maukkaat,self.kassa.kassassa_rahaa,emaksu,mmaksu), (0,0,100000,100,100))
    
    def test_korttiosto_toimii_kun_kortilla_on_tarpeeksi_rahaa(self):
        emaksu=self.kassa.syo_edullisesti_kortilla(self.kortti)
        mmaksu=self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual((self.kassa.edulliset,self.kassa.maukkaat,self.kassa.kassassa_rahaa,emaksu,mmaksu,self.kortti.saldo), (1,1,100000,True,True,360))
    
    def test_korttiosto_toimii_oikein_kun_kortilla_ei_ole_tarpeeksi_rahaa(self):
        self.kortti.saldo=100
        emaksu=self.kassa.syo_edullisesti_kortilla(self.kortti)
        mmaksu=self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual((self.kassa.edulliset,self.kassa.maukkaat,self.kassa.kassassa_rahaa,emaksu,mmaksu,self.kortti.saldo), (0,0,100000,False,False,100))

    def test_kortille_arvon_lataaminen_lisaa_kortin_saldoa_oikein(self):
        self.kassa.lataa_rahaa_kortille(self.kortti,100)
        self.assertEqual(self.kortti.saldo,1100)
    
    def test_kassan_raha_maara_kasvaa_oikein_kun_kortille_ladataan_rahaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti,100)
        self.assertEqual(self.kassa.kassassa_rahaa,100100)
    
    def test_kortin_arvo_ja_kassan_raha_maara_eivat_muutu_kun_yritetaan_ladata_negatiivinen_maara_rahaa_kortille(self):
        self.kassa.lataa_rahaa_kortille(self.kortti,-100)
        self.assertEqual((self.kassa.kassassa_rahaa,self.kortti.saldo),(100000,1000))