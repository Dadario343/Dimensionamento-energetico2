import unittest
from src.fotovoltaico import dimensionar, carregar_dataset

MODULOS = [{"id":"M1","fabricante":"Teste","modelo":"Módulo 500","potencia_wp":"500","voc_v":"49.5","isc_a":"13","vmp_v":"41.5","imp_a":"12","preco_brl":"500"}]
INVERSORES = [{"id":"I1","fabricante":"Teste","modelo":"Híbrido 5kW","tipo":"híbrido","potencia_nominal_w":"5000","potencia_max_fv_w":"6500","tensao_max_entrada_v":"600","faixa_mppt_min_v":"40","faixa_mppt_max_v":"550","corrente_max_entrada_a":"20","numero_mppt":"2","compativel_bateria":"sim","preco_brl":"3000"}]
BATERIAS = [{"id":"B1","fabricante":"Teste","modelo":"5kWh","tecnologia":"LiFePO4","tensao_nominal_v":"48","capacidade_kwh":"5","dod_pct":"90","preco_brl":"4000"}]

class TestDimensionamentoFV(unittest.TestCase):
    def test_cenario_sem_bateria(self):
        r = dimensionar(300, 5, 80, MODULOS, INVERSORES, BATERIAS)
        self.assertGreater(r['potencia'], 0)
        self.assertGreaterEqual(r['instalada'], r['potencia'])
        self.assertEqual(r['qtd_baterias'], 0)
        self.assertEqual(r['custo_baterias'], 0)
        self.assertAlmostEqual(r['custo_total'], r['custo_modulos'] + r['custo_inversor'])

    def test_cenario_com_bateria(self):
        r = dimensionar(300, 5, 80, MODULOS, INVERSORES, BATERIAS, True, 8)
        self.assertGreaterEqual(r['qtd_baterias'], 1)
        self.assertGreaterEqual(r['capacidade_instalada'], r['capacidade_necessaria'])
        self.assertGreater(r['custo_total'], r['custo_modulos'] + r['custo_inversor'])

    def test_rejeita_entrada_invalida(self):
        with self.assertRaises(ValueError):
            dimensionar(0, 5, 100, MODULOS, INVERSORES, BATERIAS)

    def test_rejeita_dados_tecnicos_ausentes(self):
        modulo_incompleto = [{"potencia_wp":"500", "preco_brl":"500"}]
        with self.assertRaisesRegex(ValueError, 'especificações elétricas completas'):
            dimensionar(300, 5, 80, modulo_incompleto, INVERSORES, BATERIAS)

    def test_rejeita_inversor_incompativel(self):
        inversor = [dict(INVERSORES[0], tensao_max_entrada_v='45')]
        with self.assertRaisesRegex(ValueError, 'combinação'):
            dimensionar(300, 5, 80, MODULOS, inversor, BATERIAS)


    def test_datasets_atendem_quantidades_minimas(self):
        self.assertGreaterEqual(len(carregar_dataset("modulos.csv")), 10)
        self.assertGreaterEqual(len(carregar_dataset("inversores.csv")), 8)
        self.assertGreaterEqual(len(carregar_dataset("baterias.csv")), 6)

    def test_cenario_real_sem_bateria(self):
        r = dimensionar(300, 5, 80)
        self.assertEqual(r["modulo"]["modelo"], "CS6W-550MS")
        self.assertGreaterEqual(r["instalada"], r["potencia"])
        self.assertGreater(r["custo_total"], 0)
        self.assertGreaterEqual(r["strings"]["numero_strings"], 1)

    def test_cenario_real_com_bateria(self):
        r = dimensionar(300, 5, 80, usar_bateria=True, autonomia_h=8)
        self.assertEqual(r["inversor"]["modelo"], "H2-5K-LS2")
        self.assertEqual(r["bateria"]["modelo"], "B3-5.0-LV")
        self.assertGreaterEqual(r["capacidade_instalada"], r["capacidade_necessaria"])
        self.assertGreater(r["custo_baterias"], 0)

if __name__ == '__main__':
    unittest.main()
