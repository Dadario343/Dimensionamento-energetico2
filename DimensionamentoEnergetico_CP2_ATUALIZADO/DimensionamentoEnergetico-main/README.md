# Dimensionamento Energético
 
Sistema para estimativa do consumo médio mensal de energia elétrica de uma residência, considerando os equipamentos elétricos utilizados, suas potências, quantidades e tempo médio diário de utilização.

# Integrantes

| Nome | RM |
|------------|------------|
| Mateus de Oliveira Fernandes Neves | RM572431 |
| Paulo Henrique Lira Bilac | RM569496 | 
| Pedro Soares de Souza | RM571285 | 
| Olavo Dadario Vianna Barreto | RM569272 |

# Funcionalidades

* Adicionar informações da residência (user)
* Adicionar equipamento (user)
* Informar potência do equipamento (user)
* Informar a quantidade de equipamentos (user)
* Remover residências (user / sistema)
* Gerar relatório (user / sistema)
* Gerar calculos (sistema)
* Sair (user)

# Product Backlog - Sistema de Dimensionamento Energético Residencial


# Product Backlog

| ID   | Utilizador (Épico) | User Story                                                                                                            |
| ---- | ------------------ | --------------------------------------------------------------------------------------------------------------------- |
| PB01 | Usuário            | Como usuário, quero me cadastrar no sistema para manter meus imóveis e análises salvos.                               |
| PB02 | Usuário            | Como usuário, quero acessar minha conta para consultar meus imóveis cadastrados.                                      |
| PB03 | Imóvel             | Como usuário, quero cadastrar um imóvel para realizar seu dimensionamento energético.                                 |
| PB04 | Imóvel             | Como usuário, quero editar ou excluir um imóvel cadastrado.                                                           |
| PB05 | Consumo            | Como usuário, quero informar o consumo mensal de energia do imóvel.                                                   |
| PB06 | Consumo            | Como usuário, quero cadastrar vários meses de consumo para representar melhor o perfil energético da residência.      |
| PB07 | Consumo            | Como usuário, quero consultar o histórico de consumo do imóvel.                                                       |
| PB08 | Dimensionamento    | Como usuário, quero que o sistema identifique automaticamente o maior consumo mensal registrado.                      |
| PB09 | Dimensionamento    | Como usuário, quero visualizar também o consumo médio mensal para contextualizar o pico de consumo.                   |
| PB10 | Dimensionamento    | Como usuário, quero saber em qual mês ocorreu o maior consumo.                                                        |
| PB11 | Resultado          | Como usuário, quero visualizar um resumo energético do imóvel.                                                        |
| PB12 | Resultado          | Como usuário, quero visualizar graficamente meu histórico de consumo.                                                 |
| PB13 | Validação          | Como usuário, quero ser alertado sobre dados de consumo inválidos ou incompletos antes de realizar o dimensionamento. |
| PB14 | Persistência       | Como usuário, quero que os dados permaneçam disponíveis após sair do sistema.                                         |
| PB15 | Segurança          | Como usuário, quero que os dados dos meus imóveis sejam privados.                                                     |

# Termos de Aceite

| ID   | Termo de Aceite                                                                    |
| ---- | ---------------------------------------------------------------------------------- |
| PB01 | O usuário deve conseguir criar uma conta preenchendo os dados necessários.         |
| PB02 | O usuário deve conseguir realizar login e acessar seus imóveis cadastrados.        |
| PB03 | O usuário deve conseguir cadastrar um imóvel e visualizar seus dados.              |
| PB04 | O usuário deve conseguir editar ou excluir um imóvel cadastrado.                   |
| PB05 | O sistema deve permitir informar o consumo mensal em kWh.                          |
| PB06 | O usuário deve conseguir cadastrar o consumo de diferentes meses.                  |
| PB07 | O sistema deve apresentar o histórico de consumo do imóvel.                        |
| PB08 | O sistema deve identificar e apresentar o maior consumo registrado.                |
| PB09 | O sistema deve calcular e apresentar o consumo médio mensal.                       |
| PB10 | O sistema deve informar o mês em que ocorreu o maior consumo.                      |
| PB11 | O sistema deve apresentar um resumo com os principais dados energéticos do imóvel. |
| PB12 | O sistema deve gerar um gráfico utilizando o histórico de consumo.                 |
| PB13 | O sistema deve alertar o usuário quando houver dados inválidos ou incompletos.     |
| PB14 | Os dados cadastrados devem permanecer disponíveis após o usuário sair do sistema.  |
| PB15 | O usuário deve conseguir acessar somente os dados dos seus próprios imóveis.       |

# Prioridade 

| Prioridade | Funcionalidades                                                 |
| ---------- | --------------------------------------------------------------- |
| **Alta**   | Cadastro, login e gerenciamento dos imóveis.                    |
| **Alta**   | Cadastro dos equipamentos, potência, quantidade e tempo de uso. |
| **Alta**   | Cálculo do consumo estimado em kWh/mês.                         |
| **Alta**   | Apresentação do consumo médio e maior consumo.                  |
| **Média**  | Histórico e gráfico de consumo.                                 |
| **Média**  | Validação de dados incorretos ou incompletos.                   |
| **Baixa**  | Melhorias de visualização e recursos adicionais.                |

# Tasks

| ID | Task | Relacionada | Prioridade |
|---|---|---|---|
| T01 | Criar estrutura inicial do sistema | — | Alta |
| T02 | Criar menu principal | — | Alta |
| T03 | Criar cadastro de usuário | PB01 | Alta |
| T04 | Validar dados do cadastro | PB01/PB13 | Alta |
| T05 | Criar sistema de login | PB02 | Alta |
| T06 | Validar usuário e senha | PB02/PB13 | Alta |
| T07 | Criar sistema de logout | PB02 | Média |
| T08 | Criar cadastro de imóvel | PB03 | Alta |
| T09 | Listar imóveis cadastrados | PB03 | Alta |
| T10 | Criar edição de imóvel | PB04 | Alta |
| T11 | Criar exclusão de imóvel | PB04 | Alta |
| T12 | Criar cadastro de equipamentos | PB03/PB05 | Alta |
| T13 | Informar potência do equipamento | PB05 | Alta |
| T14 | Informar quantidade de equipamentos | PB05 | Alta |
| T15 | Informar tempo médio diário de uso | PB05 | Alta |
| T16 | Criar cálculo de consumo por equipamento | PB05/PB08 | Alta |
| T17 | Calcular consumo total mensal | PB08/PB09 | Alta |
| T18 | Identificar maior consumo | PB08 | Alta |
| T19 | Calcular consumo médio mensal | PB09 | Alta |
| T20 | Identificar mês de maior consumo | PB10 | Alta |
| T21 | Registrar consumo mensal | PB06 | Alta |
| T22 | Criar histórico de consumo | PB07 | Média |
| T23 | Criar resumo energético | PB11 | Média |
| T24 | Criar gráfico de consumo | PB12 | Média |
| T25 | Criar validação dos dados | PB13 | Média |
| T26 | Implementar salvamento dos dados | PB14 | Alta |
| T27 | Implementar carregamento dos dados | PB14 | Alta |
| T28 | Garantir que os dados sejam vinculados ao usuário | PB15 | Alta |
| T29 | Impedir acesso aos imóveis de outros usuários | PB15 | Alta |
| T30 | Criar relatório final | PB11/PB12 | Média |
| T31 | Realizar testes do sistema | Todos | Alta |
| T32 | Corrigir erros encontrados nos testes | Todos | Alta |
| T33 | Documentar funcionamento no README | — | Média |

# Objetivo Final

O objetivo do sistema é fornecer de uma forma simples o consumo médio mensal de energia elétrica de uma residência, permitindo ao usuário visualizar quais equipamentos possuem maior participação no consumo e obter uma estimativa geral em kWh/mês.

# Como Rodar a Aplicação

A aplicação possui uma versão web desenvolvida em Python com Flask. Para executá-la, é necessário ter o Python instalado no computador.

Primeiro, abra o terminal dentro da pasta `projeto_dimensionamento`:

```bash
cd projeto_dimensionamento
```

Depois, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

Após a instalação, execute a aplicação web:

```bash
python app.py
```

Quando o servidor iniciar, acesse no navegador:

```text
http://127.0.0.1:5000
```

A partir daí, é possível realizar o cadastro, fazer login, cadastrar imóveis, adicionar equipamentos, registrar consumos e consultar os resultados do dimensionamento energético.

Também existe uma versão em modo de terminal. Para executá-la, dentro da pasta `projeto_dimensionamento`, utilize:

```bash
python main.py
```

# O que a Aplicação Resolve

O sistema resolve a dificuldade de acompanhar e estimar o consumo de energia elétrica de uma residência de forma organizada. A aplicação permite cadastrar imóveis, informar equipamentos, suas potências, quantidades e tempos de utilização, além de registrar o consumo mensal.

Com essas informações, o sistema consegue apresentar dados como consumo médio, maior consumo, mês de maior consumo, histórico e gráfico de consumo. Dessa forma, o usuário consegue ter uma visão mais clara do perfil energético da residência e identificar quais informações podem contribuir para um consumo mais elevado.

# O que Aprendemos

Durante o desenvolvimento do projeto, aprendemos a estruturar uma aplicação em Python utilizando diferentes módulos e separando as responsabilidades do sistema. Também trabalhamos com cadastro e autenticação de usuários, validação de dados, manipulação e persistência de informações, além da criação de cálculos para estimar o consumo de energia.

Também aprendemos a desenvolver uma interface web utilizando Flask, conectar páginas HTML com as regras de negócio do sistema e utilizar sessões para controlar o acesso dos usuários. Além disso, praticamos organização de código, criação de funções, integração entre arquivos, tratamento de erros, testes e documentação do projeto por meio do README.

Segue o link do nosso trello:
https://trello.com/invite/b/6ab11690a9e3f8e2361b3ed5/ATTIf595a13bf0f5e9aeae7eabf0c7a616929C0AE723/dimensionamento-energetico


## CP2 — Dimensionamento fotovoltaico residencial

A versão web inclui uma página de pré-dimensionamento fotovoltaico integrada ao imóvel e ao consumo já registrado. Na página de detalhes do imóvel, acesse **Dimensionar sistema solar** e informe localização, HSP e a fonte consultada, percentual de atendimento e se deseja armazenamento. O sistema estima a potência necessária, quantidade de módulos, configuração preliminar de strings, inversor, baterias quando solicitadas e orçamento dos equipamentos.

Os datasets ficam em `projeto_dimensionamento/src/dados/fotovoltaico/` e atendem às quantidades mínimas da atividade: 11 módulos, 8 inversores e 6 baterias. O arquivo `FONTES_E_METODOLOGIA.md` registra URLs, fórmulas, premissas e limitações. Preços não confirmados ficam vazios e não são usados pelo orçamento; não foram substituídos por valores inventados. Por isso, alguns modelos ainda não entram na seleção/orçamento até a equipe confirmar preço e ficha técnica específica.

### Executar a aplicação web
```bash
cd projeto_dimensionamento
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Acesse `http://127.0.0.1:5000` no navegador, crie uma conta e cadastre um imóvel para testar o dimensionamento.

### Executar testes automatizados
A partir da pasta `projeto_dimensionamento`:
```bash
python -m unittest discover -s tests -v
```
Os testes cobrem cenários com e sem bateria, validações de entrada, dados técnicos incompletos, incompatibilidade e quantidades mínimas dos CSVs.

**Limitação importante:** esta é uma estimativa acadêmica, não um projeto elétrico. A configuração de strings é uma triagem simplificada; HSP deve ser verificada para a localização real; preços e estoque devem ser reconfirmados. A instalação, estrutura, cabeamento, proteções, frete e adequações elétricas não entram no orçamento.
