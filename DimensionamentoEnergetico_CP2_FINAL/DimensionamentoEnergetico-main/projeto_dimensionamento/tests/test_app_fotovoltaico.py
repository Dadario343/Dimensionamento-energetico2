import unittest
from unittest.mock import patch
try:
    import app as app_module
    APP_IMPORT_ERROR = None
except ModuleNotFoundError as erro:
    app_module = None
    APP_IMPORT_ERROR = str(erro)

@unittest.skipIf(app_module is None, "Dependências da aplicação não instaladas no ambiente de teste")
class TestRotaFotovoltaica(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()
        self.patcher_imovel = patch.object(app_module.servicos, "buscar_imovel_srv", return_value={
            "id": 1, "nome": "Casa de teste", "endereco": "São Paulo/SP", "historico_consumo": []
        })
        self.patcher_consumo = patch.object(app_module.servicos, "calcular_consumo_total_estimado_srv", return_value=300.0)
        self.patcher_imovel.start()
        self.patcher_consumo.start()
        with self.client.session_transaction() as sess:
            sess["email_usuario"] = "teste@example.com"

    def tearDown(self):
        self.patcher_imovel.stop()
        self.patcher_consumo.stop()

    def test_pagina_abre_e_exibe_formulario(self):
        resposta = self.client.get("/imoveis/1/fotovoltaico")
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(b"Dimensionamento fotovoltaico", resposta.data)
        self.assertIn(b"Fonte do valor de HSP", resposta.data)

    def test_post_gera_orcamento_sem_bateria(self):
        resposta = self.client.post("/imoveis/1/fotovoltaico", data={
            "consumo_kwh": "300", "localizacao": "São Paulo/SP", "hsp": "5",
            "fonte_hsp": "Fonte de teste", "percentual": "80", "baterias": "nao"
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Orçamento estimado de equipamentos".encode("utf-8"), resposta.data)
        self.assertIn(b"R$ 10531.97", resposta.data)

if __name__ == "__main__":
    unittest.main()
