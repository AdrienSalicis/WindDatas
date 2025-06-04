# test_cdsapirc.py
# ➔ Vérifie si ton .cdsapirc est bien configuré

import os
import cdsapi

def check_cdsapirc():
    cdsapirc_path = os.path.expanduser("~/.cdsapirc")
    
    if not os.path.exists(cdsapirc_path):
        print("[❌] Fichier .cdsapirc introuvable.")
        return
    
    with open(cdsapirc_path, 'r') as f:
        content = f.read()
    
    print("[📄] Contenu actuel de .cdsapirc :\n")
    print(content)
    
    if "url:" not in content or "key:" not in content:
        print("[❌] Le fichier .cdsapirc semble mal formaté.")
        return
    
    print("[✅] .cdsapirc semble présent et bien formaté.")

    try:
        print("[🔍] Test de connexion Copernicus...")
        c = cdsapi.Client()
        print("[✅] Connexion API Copernicus réussie.")
    except Exception as e:
        print(f"[❌] Erreur de connexion API : {e}")

if __name__ == "__main__":
    check_cdsapirc()
