# CP2 — Modelagem da Sprint 2: Dimensionamento Fotovoltaico Residencial

## Épico
Permitir gerar uma proposta preliminar de sistema fotovoltaico residencial integrada ao imóvel e ao consumo registrado, com seleção técnica básica, opção de baterias e orçamento de equipamentos rastreável.

## Product Backlog — User Stories e critérios de aceite

### US01 — Dimensionar geração fotovoltaica (Prioridade alta)
**Como** usuário, **quero** informar localização, HSP e percentual de atendimento, **para** estimar a potência FV necessária à residência.

**Critérios de aceite:** o consumo médio/histórico do imóvel é sugerido; localização, consumo e HSP são informados; valida consumo e HSP positivos, fator de desempenho entre 0 e 1 e atendimento entre 1% e 100%; calcula `E_FV = C_m × f` e `P_FV = E_FV / (HSP × 30 × η)`; apresenta as premissas, potência calculada e potência instalada.

**Tasks:** integrar consumo do imóvel; acrescentar campos de localização e fonte HSP; implementar fórmulas; validar limites; mostrar resultados e premissas.

### US02 — Manter datasets rastreáveis de equipamentos (Prioridade alta)
**Como** equipe, **quero** datasets CSV de módulos, inversores e baterias, **para** comparar produtos comercializados no Brasil.

**Critérios de aceite:** pelo menos 10 módulos, 8 inversores e 6 baterias; campos e unidades padronizados; links de fonte e data de coleta; preço vazio quando não confirmado; nenhum preço fictício; sistema não usa registros sem dados essenciais para orçar.

**Tasks:** modelar schemas; coletar ficha técnica; pesquisar fornecedor/preço; registrar URLs e data; validar quantidades e campos; revisar rastreabilidade.

### US03 — Selecionar módulo e inversor compatíveis (Prioridade alta)
**Como** usuário, **quero** que o sistema verifique limites elétricos básicos, **para** evitar combinações claramente incompatíveis.

**Critérios de aceite:** quantidade de módulos arredondada para cima; potência instalada calculada; não seleciona item sem preço; valida potência nominal/máxima FV, tensão Voc da string, faixa MPPT, corrente e quantidade de MPPT; informa erro quando não encontra combinação válida; exibe uma configuração de strings preliminar.

**Tasks:** ler CSVs; validar campos; calcular quantidade; procurar configuração de strings iguais; filtrar inversores; criar testes para incompatibilidades.

### US04 — Dimensionar armazenamento opcional (Prioridade média)
**Como** usuário, **quero** escolher se desejo baterias e informar autonomia, **para** estimar a capacidade de armazenamento necessária.

**Critérios de aceite:** sem bateria, quantidade e custo são zero; com bateria, autonomia entre 1 e 24 horas; calcula energia de autonomia, capacidade nominal considerando DoD e eficiência, quantidade e capacidade instalada; só considera inversor híbrido e bateria com preço e dados de tensão/capacidade; usa marca igual como filtro conservador e informa que isso não substitui confirmação do fabricante.

**Tasks:** criar formulário condicional; calcular autonomia; filtrar inversores híbridos; selecionar bateria; calcular custos; testar cenários com e sem bateria.

### US05 — Gerar resumo e orçamento (Prioridade alta)
**Como** usuário, **quero** receber os equipamentos, premissas, geração e custos, **para** avaliar a proposta preliminar.

**Critérios de aceite:** apresenta consumo, localização, fonte HSP, percentual, energia alvo, fator de desempenho, potência calculada/instalada, quantidade/modelo dos módulos, configuração preliminar de strings, inversor, baterias quando houver, geração estimada, custos por categoria e total; identifica exclusões; não usa preço ausente como zero nem cria cotação fictícia.

**Tasks:** montar resumo; somar valores; exibir limitações; registrar fontes; gerar cenários de teste e instruções de execução.

## Dependências
US01 depende do cadastro do imóvel e de consumo disponível. US03 depende de US01 e US02. US04 depende de dados de bateria e de inversor híbrido. US05 depende das seleções válidas de US01–US04.

## Kanban sugerido para registro no quadro da equipe

| A fazer | Em andamento | Concluído nesta versão |
|---|---|---|
| Confirmar preços de todos os modelos sem cotação pública | Revisar datasheets individuais dos inversores que ainda não foram validados | Integrar rota fotovoltaica ao imóvel |
| Validar HSP geográfica por localização usando fonte solar local | Capturar evidências visuais dos cenários no ambiente da equipe | Implementar cálculo de potência, módulos, strings e orçamento |
| Registrar tarefas e responsáveis no quadro real do grupo | Conferir preços e estoque no dia da apresentação | Adicionar campos de localização e fonte de HSP |
| Avaliar instalação, estruturas e demais custos se a equipe decidir incluí-los |  | Implementar testes unitários de cenários com/sem bateria e de incompatibilidade |

## Cenários de evidência reproduzíveis

**Cenário A — sem baterias:** consumo 300 kWh/mês, HSP 5 h/dia, atendimento 80%, fator 0,80. Energia-alvo = 240 kWh/mês; potência necessária = 2,00 kWp. Com módulo de 550 Wp, quantidade = 4 módulos e potência instalada = 2,20 kWp. O teste de integração confirma seleção de inversor com dados e preço disponíveis.

**Cenário B — com baterias:** mesmos valores, autonomia 8 h. Consumo diário = 10 kWh/dia; energia para 8 h = 3,33 kWh; capacidade nominal estimada = `3,33 / (0,90 × 0,90) ≈ 4,12 kWh`. A quantidade final depende da capacidade útil da bateria selecionada e do filtro de compatibilidade do inversor híbrido.

Os testes automatizados ficam em `projeto_dimensionamento/tests/test_fotovoltaico.py` e podem ser executados com `python -m unittest discover -s tests -v` a partir de `projeto_dimensionamento`.

## Premissas e limites

HSP de 4,5 h/dia e fator global de 0,80 são premissas de simulação; o sistema solicita que o usuário registre a fonte de HSP. O cálculo de strings é simplificado e não substitui engenharia, análise térmica, proteção, normas, homologação ou vistoria do imóvel. Os preços são referências pontuais, não propostas comerciais. A metodologia e as URLs de origem estão em `src/dados/fotovoltaico/FONTES_E_METODOLOGIA.md`.

### Orçamento demonstrativo gerado pelo sistema (preços observados em 09/10/2026)

| Item | Sem bateria | Com bateria (8 h) |
|---|---:|---:|
| 4 módulos Canadian Solar CS6W-550MS | R$ 2.641,20 | R$ 2.641,20 |
| 1 inversor SAJ H2-5K-LS2 | R$ 7.890,77 | R$ 7.890,77 |
| 1 bateria SAJ B3-5.0-LV | R$ 0,00 | R$ 6.499,90 |
| **Total dos equipamentos** | **R$ 10.531,97** | **R$ 17.031,87** |

Entradas do cenário: consumo 300 kWh/mês, HSP 5 h/dia, atendimento 80% e fator global 0,80. Resultado: energia-alvo de 240 kWh/mês, potência calculada de 2,00 kWp, potência instalada de 2,20 kWp e geração simplificada estimada de 264 kWh/mês. Para a alternativa com bateria, a capacidade necessária calculada é aproximadamente 4,12 kWh e uma bateria de 5,12 kWh nominais (aprox. 4,61 kWh úteis pelo DoD de 90%) atende à estimativa simplificada. Os valores são demonstração reproduzível com os preços gravados nos CSVs, não cotação comercial vigente.
