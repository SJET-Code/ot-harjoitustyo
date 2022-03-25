import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_kortin_alku_saldo_on_oikein(self):
        self.assertEqual(str(self.maksukortti), 'saldo: 10')
    
    def test_korttiin_arvon_lataaminen_toimii_oikein(self):
        self.maksukortti.lataa_rahaa(5)
        self.assertEqual(str(self.maksukortti), 'saldo: 15')

    def test_saldo_vahenee_oikein(self):
        self.maksukortti.ota_rahaa(5)
        self.assertEqual(str(self.maksukortti), 'saldo: 5')
    
    def test_saldo_ei_muutu_jos_kortilla_ei_ole_tarpeeksi_rahaa(self):
        self.maksukortti.ota_rahaa(15)
        self.assertEqual(str(self.maksukortti), 'saldo: 10')
    
    def test_palautuu_arvo_true_jos_metodi_onnistuu(self):
        vastaus=self.maksukortti.ota_rahaa(5)
        self.assertEqual(vastaus,True)

    def test_palautuu_arvo_false_jos_metodi_ei_onnistu(self):
        vastaus=self.maksukortti.ota_rahaa(15)
        self.assertEqual(vastaus,False)