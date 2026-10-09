# Fontes, rastreabilidade e metodologia dos datasets fotovoltaicos

**Data de revisão dos registros:** 09/10/2026. Os preços são valores observados nas páginas dos fornecedores na data de coleta e podem mudar, ficar indisponíveis ou variar por frete, região, forma de pagamento e estoque. O CSV registra apenas preço com fonte de produto identificável; campos vazios significam **preço não confirmado**, não preço zero.

## Arquivos e schema

- `modulos.csv`: 11 modelos (mínimo exigido: 10), com potência, Voc, Isc, Vmp, Imp e eficiência. Os cinco módulos Canadian Solar usam a família CS6W-MS; os seis JA Solar usam a família JAM72S30-MR.
- `inversores.csv`: 8 modelos (mínimo exigido: 8), com tipo, potência nominal e máxima FV, tensão máxima, faixa MPPT, corrente, número de MPPT e indicação de bateria.
- `baterias.csv`: 6 modelos (mínimo exigido: 6), com tecnologia, tensão, capacidade, DoD, ciclos quando publicados e preço quando encontrado.

Todos os campos numéricos são gravados em formato simples para leitura por `csv.DictReader`. Campos não confirmados ficam vazios; não devem ser convertidos em zero para afirmar que o produto não custa nada.

## Fontes técnicas primárias e fontes de preço

### Módulos

- Canadian Solar, ficha técnica da família HiKu6 CS6W-MS: https://www.canadiansolar.com/na/wp-content/uploads/sites/3/2026/01/CS-Datasheet-HiKu6_CS6W-MS_v2.7_EN-2278mm.pdf
- Registro do Inmetro para a família Canadian Solar Si-Mono, com modelos CS6W-540MS a CS6W-560MS: https://registro.inmetro.gov.br/consulta/detalhe.aspx?NumeroRegistro=002567%2F2023&pag=1
- JA Solar, ficha técnica JAM72S30-525/MR a JAM72S30-550/MR: https://www.jasolar.com/uploadfile/2020/1127/20201127115120294.pdf
- Preço registrado para o Canadian Solar CS6W-550MS: Minha Casa Solar, https://www.minhacasasolar.com.br/painel-solar-monocristalino-canadian-cs6w-550ms-83846 . O preço observado no registro foi R$ 660,30; confirmar a página antes de usar em decisão de compra.

### Inversores

- SAJ H2-5K-LS2, ficha técnica do fabricante (potência nominal 5.000 W, arranjo FV máximo 10.000 Wp, tensão CC máxima 500 V, faixa MPPT 90–480 V, corrente de entrada 20 A por entrada/MPPT e 2 MPPT): https://br.saj-electric.com/hubfs/Brazil/Datasheet/H2-%285K-10k%29-LS2_datasheet_pt_BR.pdf
- Growatt MIN 5000TL-X, página técnica da família: https://www.growatt.com/ . Valores cadastrados são parâmetros publicados para o modelo MIN 5000TL-X e devem ser conferidos com a revisão do datasheet aplicável ao produto vendido no Brasil.
- Deye SUN-5K-SG01LP1-US, página oficial com dados elétricos: https://deye.com/pt/product/sun-5-6-7-6-8k-sg01lp1-us/ .
- Sungrow SG5.0RS, manual oficial da família SG2.0RS–SG6.0RS: https://info-support.sungrowpower.com/product-materials/3f9aaa85-76f8-444a-b773-f162c8dc6b26.pdf .
- Solis S6-GR1P5K, página oficial que disponibiliza a ficha técnica da série: https://www.solisinverters.com/br/solarinverter2/2500_6000w_s6_br.html .
- GoodWe GW5000-MS, ficha técnica da série MS: https://en.goodwe.com/Ftp/Downloads/Datasheet/AU/GW_MS_Datasheet-AU.pdf .
- Huawei SUN2000-5KTL-L1, ficha técnica oficial: https://solar.huawei.com/admin/asset/v1/pro/view/1e029d00296a4b87a9823fd083db547e.pdf . A série utiliza baterias Huawei LUNA de alta tensão, não as baterias de baixa tensão deste dataset; por isso, o campo `compativel_bateria` está como `não` para a seleção de armazenamento atual.
- SAJ R5-5K-S2, ficha técnica da série R5-S2: https://img.saj-electric.com/file/R5-3~8K-S2-15%20Series%20Datasheet-20230505093247335.pdf . É inversor on-grid, sem bateria.
- Os links acima sustentam os dados técnicos principais cadastrados; a seleção do sistema continua limitada a modelos com preço preenchido e compatibilidade básica. Preços vazios impedem que os modelos entrem no orçamento nesta versão.
- Preço registrado para SAJ H2-5K-LS2: Meu Gerador, https://www.meugerador.com.br/products/inversor-solar-hibrido-saj-5kw-h2-5k-ls2-220v-2mppt-48v-monitoramento-wifi . Valor observado: R$ 7.890,77; confirmar disponibilidade e condições atuais.

### Baterias

- SAJ B3-5.0-LV, ficha técnica do fabricante: https://br.saj-electric.com/hubfs/Brazil/Datasheet/B3-5.0-LV_datasheet_pt_BR.pdf . Informa 5,12 kWh nominais, 4,6 kWh úteis, 51,2 V, DoD de até 90% e pelo menos 6.000 ciclos nas condições declaradas pelo fabricante.
- Preço registrado para SAJ B3-5.0-LV: Loja Cearasol, https://loja.cearasol.com.br/produto/bateria-saj-b3-5-0-lv/ . Valor registrado no dataset: R$ 6.499,90; confirmar página e estoque.
- Growatt HOPE 5.0L-B1: página oficial do produto e acesso à ficha técnica https://br.growatt.com/products/hope-5.0-b1 .
- GoodWe LX A5.0-30 (Lynx A G3): ficha técnica oficial https://en.goodwe.com/Ftp/EN/Downloads/Datasheet/GW_Lynx-A-G3_Datasheet-EN.pdf . O documento indica energia nominal de 5,12 kWh e energia útil de 5,0 kWh; os campos de DoD/ciclos não confirmados ficaram vazios.
- Hoymiles LB-6D-G3: portal oficial de downloads https://www.hoymiles.com/ysecm_api?c=api&cache_siteid=5&get=&m=template&name=list_data.html&s=download . Os parâmetros elétricos e o preço não foram preenchidos porque não foi possível confirmar a ficha completa e o valor em uma página estável durante a coleta.
- Deye SE-G5.1 Pro-B: página técnica oficial https://deye.com/pt/product/se-g5-1-pro-b/ . Informa LiFePO4, 100 Ah, 51,2 V, 5,12 kWh, tensão de operação 43,2–57,6 V; o folheto da série também informa DoD recomendado e vida em ciclos: https://deye.com/wp-content/uploads/2026/01/deye-se-g5.1-pro-b-series_brochure-20260115AUV1.0.pdf .
- EPEVER LFP5.12KWH25.6V-P65L2GF40: página de produto/fornecedor https://www.neosolar.com.br/loja/bateria-litio-lfp-25v-205ah-5248-wh-epever-p65l2.html . O preço registrado é R$ 5.999,00; confirmar disponibilidade e ficha antes da compra. Esta bateria de 25,6 V não passa no filtro simplificado de bateria de 40–60 V usado para o inversor selecionado.

## Recurso solar (HSP)

A aplicação exige que o usuário informe a localização, o valor de HSP e a fonte consultada. Para o Brasil, uma fonte de referência para pesquisar recurso solar é o CRESESB/SunData: https://cresesb.cepel.br/index.php?section=sundata . O sistema não geocodifica automaticamente o endereço nem consulta uma base solar em tempo real; por isso, a pessoa deve selecionar/registrar o valor correspondente à localização e à inclinação/orientação quando aplicável. O valor padrão de 4,5 h/dia é apenas um valor inicial de simulação.

## Regras de cálculo

- Energia mensal alvo: `E_FV = consumo_mensal × percentual / 100`.
- Potência FV necessária: `P_FV = E_FV / (HSP × 30 × fator_de_desempenho)`.
- Quantidade de módulos: arredondamento para cima de `P_FV × 1000 / potência_do_módulo`.
- Potência instalada: `quantidade × potência_do_módulo / 1000`.
- Geração estimada: `potência_instalada × HSP × 30 × fator_de_desempenho`.
- Autonomia: `E_autonomia = (consumo_mensal / 30) × (autonomia_h / 24)`.
- Capacidade nominal necessária: `E_autonomia / (DoD × eficiência_da_bateria)`, usando eficiência simplificada de 90% e DoD do equipamento escolhido.
- Quantidade de baterias: arredondamento para cima da capacidade necessária dividida pela capacidade útil por bateria.
- Orçamento: soma do custo dos módulos, inversor e baterias quando solicitadas. Instalação, estrutura, cabos, conectores, proteções, frete e adequações elétricas ficam explicitamente fora do valor.

## Regras de seleção e limitações

O sistema ignora preços vazios e equipamentos sem os parâmetros necessários. Para a seleção de módulo/inversor, confere potência, Voc da string, faixa MPPT, corrente, número de MPPT e divisão simples em strings iguais. Para bateria, exige inversor híbrido marcado como compatível, preço/capacidade/DoD/tensão preenchidos e mesma marca como filtro conservador. Mesmo a mesma marca não substitui a lista oficial de baterias compatíveis do fabricante.

O cálculo de string é uma triagem acadêmica. Não calcula Voc em temperatura mínima, corrente de curto-circuito corrigida, orientação, sombreamento, perdas específicas, queda de tensão, cabos, proteções, normas, aprovação da distribuidora ou projeto executivo. HSP padrão de 4,5 h/dia é um valor inicial informado no formulário, não um valor geográfico automaticamente validado. O usuário deve informar a localização e a fonte consultada.

## Pendências de dados explicitamente sinalizadas

O dataset atinge as quantidades mínimas, mas nem todos os produtos têm preço público confirmado no CSV e alguns registros têm campos técnicos em branco por não terem sido confirmados na fonte disponível. Esses registros não entram no orçamento ou na seleção técnica. Para fechar o critério acadêmico de rastreabilidade integral, a equipe deve completar as cotações e os campos que faltam, conferindo a revisão do datasheet de cada modelo. Os dados incompletos são mantidos transparentes, em vez de inventar preço ou declarar compatibilidade sem evidência.
