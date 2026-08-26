import os
import re
import pandas as pd
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(BASE_DIR, "perfil_chrome_supercasa")

def raspar_supercasa(paginas: int = 2) -> pd.DataFrame:
    imoveis = []

    print("🌐 A iniciar o navegador Playwright com perfil anti-bot...")
    with sync_playwright() as p:
        # Usa o contexto persistente com args anti-bot para contornar o Cloudflare
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.new_page()

        for num_pagina in range(1, paginas + 1):
            url = f"https://supercasa.pt/comprar-casas/porto-distrito/pagina-{num_pagina}"
            print(f"🔍 A raspar página {num_pagina}: {url}")
            
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)  # Pausa de 3s para o JS renderizar
            except Exception as e:
                print(f"⚠️ Erro ao carregar página {num_pagina}: {e}")
                continue

            # Seleciona os cartões de imóveis
            # Removemos seletores perigosos como .card e div[class*=""]
            # O ponto (.) antes do nome garante que apanha apenas a caixa principal, 
            # ignorando as sub-caixas como property-card-image ou property-card-price.
            cartoes = page.query_selector_all('.property-card, .property')
            print(f"  ➜ {len(cartoes)} elementos detetados na página {num_pagina}.")

            for cartao in cartoes:
                try:
                    # 1. Título (Apanha qualquer classe que tenha "title" ou seja um h2)
                    elem_titulo = cartao.query_selector('h2, [class*="title"]')
                    titulo = elem_titulo.text_content().strip() if elem_titulo else ""

                    # Se não houver título, é porque não é um anúncio real
                    if not titulo or len(titulo) < 3:
                        continue

                    # 2. Preço (Apanha qualquer classe que tenha "price")
                    elem_preco = cartao.query_selector('[class*="price"]')
                    if elem_preco and elem_preco.text_content().strip():
                        preco_raw = elem_preco.text_content().strip()
                    else:
                        match = re.search(r'(\d[\d\s\.]*\s*€)', cartao.text_content() or "")
                        preco_raw = match.group(1) if match else "0"
                    
                    # Limpeza com regex (remove letras e símbolos)
                    numeros_preco = re.sub(r'[^\d]', '', preco_raw)
                    preco = int(numeros_preco) if numeros_preco else 0

                    # 3. Localização (Apanha qualquer classe que tenha "location")
                    elem_local = cartao.query_selector('[class*="location"]')
                    localizacao = elem_local.text_content().strip() if elem_local else "N/D"

                    # 4. Link (Apanha o primeiro link dentro da caixa)
                    elem_link = cartao.query_selector('a')
                    link = elem_link.get_attribute('href') if elem_link else ""
                    if link and not link.startswith('http'):
                        link = f"https://supercasa.pt{link}"

                    imoveis.append({
                        'Título': titulo,
                        'Preço (€)': preco,
                        'Localização': localizacao,
                        'Link': link
                    })
                    
                    # O teu aviso de sucesso!
                    print(f"  ✅ Lido com sucesso: {titulo} | {preco} €")
                    
                except Exception as e:
                    continue

        context.close()

    df = pd.DataFrame(imoveis)
    if not df.empty and 'Link' in df.columns:
        df = df.drop_duplicates(subset=['Link'])
    return df