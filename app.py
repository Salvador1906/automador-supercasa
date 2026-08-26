import gspread
import pandas as pd
from scraper_supercasa import raspar_supercasa

def enviar_para_google_sheets(df: pd.DataFrame, nome_folha: str = 'Imoveis_Supercasa_Cloud'):
    if df.empty:
        print("⚠️ DataFrame vazio. Nenhum dado recolhido para enviar.")
        return

    try:
        print("🔑 A ligar à API do Google Sheets...")
        gc = gspread.service_account(filename='credentials.json')
        sheet = gc.open(nome_folha)
        worksheet = sheet.get_worksheet(0)

        conteudo = [df.columns.values.tolist()] + df.values.tolist()
        
        print("☁️ A atualizar os dados na folha de cálculo...")
        worksheet.clear()
        worksheet.update(conteudo)
        
        print(f"🚀 SUCESSO! {len(df)} imóveis foram publicados na folha '{nome_folha}'!")

    except Exception as e:
        print(f"❌ Erro ao comunicar com o Google Sheets: {e}")

if __name__ == "__main__":
    NOME_DA_FOLHA = 'Imoveis_Supercasa_Cloud'
    PAGINAS_A_RASPAR = 2

    # 1. Executa o scraper importado do outro ficheiro
    df_imoveis = raspar_supercasa(paginas=PAGINAS_A_RASPAR)

    # 2. Publica os dados na nuvem
    enviar_para_google_sheets(df_imoveis, nome_folha=NOME_DA_FOLHA)