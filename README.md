# Portfólio de QA · SauceDemo

[![Selenium tests](https://github.com/meleandromelo/qa-portfolio-selenium-saucedemo/actions/workflows/selenium-tests.yml/badge.svg?branch=main)](https://github.com/meleandromelo/qa-portfolio-selenium-saucedemo/actions/workflows/selenium-tests.yml)

Suíte de sete testes de ponta a ponta para a loja de demonstração [SauceDemo](https://www.saucedemo.com/). O foco é verificar o que o comprador vê, da autenticação à confirmação do pedido. Cada caso abre uma sessão independente do Chrome. Os testes usam as contas públicas do site e dados fictícios de comprador.

## Cobertura

| Caso | Comportamento verificado |
| --- | --- |
| Login válido | O usuário padrão chega a `/inventory.html`, vê o título “Products” e uma lista de produtos. |
| Usuário bloqueado | A loja informa o bloqueio e mantém o usuário na tela de login. |
| Senha incorreta | A loja informa que as credenciais são inválidas. |
| Campos vazios | A loja solicita o nome de usuário ao enviar o formulário vazio. |
| Ordenação | A vitrine conserva os produtos e preços ao ordenar por preço crescente e depois por nome de Z a A. |
| Carrinho | O contador acompanha inclusões e remoções. O item restante persiste após voltar ao inventário e atualizar a página. Ao esvaziar o carrinho, o contador desaparece. |
| Checkout | O resumo conserva os itens, quantidades e preços da vitrine. O teste confere subtotal, imposto de 8% e total com `Decimal`, finaliza o pedido e verifica a confirmação e o carrinho vazio. |

## Como o projeto está organizado

| Caminho | Responsabilidade |
| --- | --- |
| `pages/` | Page Objects de login, inventário, carrinho e checkout. Encapsulam seletores `data-test`, ações e esperas explícitas com `WebDriverWait`. |
| `tests/` | Cenários e asserções do ponto de vista do comprador. Os três logins negativos usam parametrização do Pytest. |
| `data/` | Contas de demonstração, produtos escolhidos e comprador fictício. |
| `utils/` | Configuração do Chrome WebDriver. |
| `conftest.py` | Sessão de navegador por teste, login compartilhado como fixture e captura de tela em falhas. |
| `results/` | Relatórios e capturas gerados durante a execução. |
| `.vscode/` | Configuração do interpretador, descoberta dos testes e extensões recomendadas. |
| `.github/workflows/` | Execução no GitHub Actions e publicação das evidências. |

## Rodar no Windows com PowerShell

Use Python 3.15, Google Chrome e acesso à internet. Na primeira execução, o Selenium Manager pode baixar o ChromeDriver compatível. Depois de clonar o projeto, execute os comandos na raiz do repositório.

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

O padrão é Chrome headless. Para acompanhar o checkout com a janela aberta, execute um único cenário.

```powershell
.\.venv\Scripts\python.exe -m pytest -v tests/test_checkout.py --headed
```

## Rodar no VS Code

1. Abra a pasta do repositório e instale as extensões recomendadas **Python** e **Pylance**.
2. Crie o ambiente e instale as dependências com os dois primeiros comandos acima. A configuração do workspace aponta para `.venv\Scripts\python.exe`. Se o VS Code já tiver outro interpretador selecionado, use **Python: Select Interpreter** para escolher esse executável.
3. Abra o painel **Testing**. Use **Refresh Tests** para descobrir os sete casos e **Run Tests** para executar toda a suíte ou um caso individual.

## Relatórios e integração contínua

Ao final da execução, abra `results/report.html` no navegador. O resultado em formato JUnit fica em `results/junit.xml`. Se uma asserção ou preparação falhar com o navegador disponível, a suíte salva o PNG em `results/screenshots/` e incorpora a imagem ao HTML.

O workflow **Selenium tests** executa a mesma suíte em Chrome headless no Ubuntu em cada push e pull request. A etapa de upload roda também em caso de falha. Na página de uma execução, baixe o artefato **selenium-results** para consultar os relatórios e as capturas geradas. Os artefatos ficam disponíveis por 14 dias.
