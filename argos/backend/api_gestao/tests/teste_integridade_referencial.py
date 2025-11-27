import requests
import json

# Configurações
API_URL = "http://localhost:8000"
CREDENCIAIS_GESTOR = {"email": "gestor@argos.com", "senha": "senha123"}

def teste_integridade_referencial():
    print("\n🧪 --- INICIANDO TESTE CT-08: Integridade Referencial ---")

    # PASSO 1: Autenticação (Login)
    print("1️⃣  Realizando Login como Gestor...")
    try:
        login_resp = requests.post(f"{API_URL}/auth/login", json=CREDENCIAIS_GESTOR)
        login_resp.raise_for_status() # Lança erro se não for 200 OK
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("   ✅ Login OK!")
    except Exception as e:
        print(f"   ❌ Erro no Login: {e}")
        print("      (Certifique-se de ter rodado o seed.py antes)")
        return

    # PASSO 2: Requisição GET /usuarios/
    print("\n2️⃣  Buscando lista de usuários (GET /usuarios/)...")
    resp = requests.get(f"{API_URL}/usuarios/", headers=headers)
    
    if resp.status_code != 200:
        print(f"   ❌ Erro ao buscar usuários: {resp.text}")
        return
    
    usuarios = resp.json()
    print(f"   ✅ Lista recebida com {len(usuarios)} usuário(s).")

    # PASSO 3: Encontrar "Sherlock" e Analisar
    print("\n3️⃣  Analisando JSON do usuário 'Sherlock'...")
    
    # Busca o usuário na lista usando list comprehension
    sherlock = next((u for u in usuarios if "Sherlock" in u["nome"]), None)

    if not sherlock:
        print("   ❌ Usuário 'Sherlock' não encontrado na lista.")
        return

    # PASSO 4: Verificação do Campo 'perfil'
    perfil_campo = sherlock.get("perfil")
    
    print(f"   🔍 Conteúdo bruto do campo 'perfil':")
    print(f"      {json.dumps(perfil_campo, indent=4, ensure_ascii=False)}")

    # Validação Lógica
    if isinstance(perfil_campo, dict) and "nome" in perfil_campo:
        print("\n📊 RESULTADO DO TESTE:")
        print("   ✅ SUCESSO! O campo 'perfil' é um OBJETO COMPLETO.")
        print(f"      - Nome do Perfil: {perfil_campo['nome']}")
        print(f"      - ID do Perfil:   {perfil_campo.get('id') or perfil_campo.get('_id')}")
        print("   Isso confirma que o 'fetch_links=True' funcionou no Backend.")
    else:
        print("\n📊 RESULTADO DO TESTE:")
        print("   ❌ FALHA! O campo 'perfil' veio apenas como ID ou Nulo.")

if __name__ == "__main__":
    teste_integridade_referencial()