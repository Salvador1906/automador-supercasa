



# 🏠 Automador de Extração Imobiliária (Supercasa ➔ Google Sheets)

Um pipeline completo de Web Scraping e integração Cloud que extrai dados de anúncios imobiliários e atualiza automaticamente uma folha do Google Sheets em tempo real. 

Este projeto demonstra a capacidade de construir soluções _end-to-end_: desde a recolha contornando sistemas anti-bot, passando pela limpeza dos dados, até à publicação automatizada na nuvem.

## 🚀 Tecnologias e Bibliotecas Utilizadas

* **Python 3:** Linguagem base do projeto.
* **Playwright:** Uma das ferramentas mais modernas para automação de navegadores web. Foi utilizado neste projeto de Web Scraping de sites complexos para renderizar JavaScript e contornar bloqueios dinâmicos. É uma excelente base para a criação de robôs RPA (Automação de Processos).
* **Módulo `re` (Expressões Regulares):** Utilizado como um verdadeiro "bisturi cirúrgico" nativo do Python para procurar, validar e extrair padrões de texto precisos (como limpeza de preços e caracteres indesejados).
* **Pandas:** Responsável pelo tratamento de dados em DataFrames e remoção de anúncios duplicados.
* **Google Sheets API (`gspread`):** Para autenticação via conta de serviço e envio de dados para a cloud em tempo real.

## ⚙️ Funcionalidades

- Abertura de navegador com perfil persistente para evitar verificações de segurança.
- Extração precisa de títulos, preços absolutos, localização e hiperligações da página de destino.
- Processamento e limpeza de dados imperfeitos (ex: strings vazias, formatações de preço não convencionais).
- Ligação direta à Google Cloud para publicação dos dados estruturados numa folha de cálculo.
