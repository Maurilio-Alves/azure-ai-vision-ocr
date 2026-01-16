import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# --- CONFIGURAÇÃO DO QG ---
# --- CONFIGURAÇÃO DO Qpython src/ocr_local.pyG ---
# Substitua pelas suas chaves quando for rodar localmente, 
# mas NUNCA poste suas chaves reais no GitHub!
ENDPOINT = "COLOQUE_SEU_ENDPOINT_AQUI"
SUBSCRIPTION_KEY = "COLOQUE_SUA_CHAVE_AQUI"

def analisar_e_salvar():
    print("\n[SISTEMA]: Inicializando sensores de visão e escrita...")
    
    try:
        client = ImageAnalysisClient(
            endpoint=ENDPOINT,
            credential=AzureKeyCredential(SUBSCRIPTION_KEY)
        )

        # Como o script roda de fora ou de dentro da pasta, 
        # o caminho relativo precisa subir um nível ou ser direto
        caminho_arquivo = "inputs/teste.jpg"
        
        with open(caminho_arquivo, "rb") as f:
            image_data = f.read()

        print(f"[SISTEMA]: Analisando '{caminho_arquivo}'...")
        result = client.analyze(image_data=image_data, visual_features=[VisualFeatures.READ])

        if result.read is not None:
            # --- NOVA MISSÃO: SALVAR EM ARQUIVO TXT ---
            nome_saida = "output/resultado_ocr.txt"
            
            with open(nome_saida, "w", encoding="utf-8") as arquivo_txt:
                arquivo_txt.write("=== RELATÓRIO DE EXTRAÇÃO AZURE ===\n")
                arquivo_txt.write(f"Arquivo analisado: {caminho_arquivo}\n\n")
                
                print("\n[ESCRIBIA]: Gravando dados no arquivo...")
                for block in result.read.blocks:
                    for line in block.lines:
                        arquivo_txt.write(f"{line.text}\n")
            
            print(f"✅ SUCESSO! O texto foi salvo em: {nome_saida}")
            print("="*40)
        else:
            print("[ALERTA]: Nada para salvar, nenhum texto detectado.")

    except Exception as e:
        print(f"\n[ERRO]: {e}")

if __name__ == "__main__":
    analisar_e_salvar()