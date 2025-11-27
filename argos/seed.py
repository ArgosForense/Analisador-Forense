import requests
import json

API_URL = "http://localhost:8000"

def seed():
    print("🌱 Iniciando população do banco de dados...")

    # 1. Criar Empresa
    empresa_data = {"nome": "TechShielld Forense", "cnpj": "11.111.999/0001-99"}
    print(f"📤 Enviando Empresa: {empresa_data}")
    
    resp = requests.post(f"{API_URL}/auth/cadastrar_empresa", json=empresa_data)
    
    if resp.status_code == 201:
        print("✅ Empresa criada!")
        resp_json = resp.json()
        print(f"   Resposta do Servidor: {resp_json}") # Debug
        
        # Tenta pegar 'id' OU '_id'
        empresa_id = resp_json.get("id") or resp_json.get("_id")
        
        if not empresa_id:
            print("❌ ERRO CRÍTICO: O servidor não retornou o ID da empresa.")
            print("   Verifique o EmpresaResponseSchema.")
            return
    else:
        print(f"⚠️ Empresa não criada (Status {resp.status_code}): {resp.text}")
        # Se falhou (ex: já existe), tenta buscar pelo CNPJ ou aborta
        # Para teste limpo, vamos abortar
        return

    print(f"🏢 ID da Empresa: {empresa_id}")

    # 2. Criar Gestor
    gestor_email = "gestorDoGrau@argos.com"
    gestor_pass = "senha123"
    
    gestor_data = {
        "nome": "Gestor Supremo",
        "email": gestor_email,
        "senha": gestor_pass,
        "empresa_id": empresa_id # Agora garantimos que é um ID válido
    }
    
    print(f"\n📤 Criando Gestor: {gestor_email}")
    resp = requests.post(f"{API_URL}/auth/criar_conta", json=gestor_data)
    
    if resp.status_code == 201:
        print("✅ Gestor criado com sucesso!")
    elif resp.status_code == 400:
        print("ℹ️  Gestor já existia.")
    else:
        print(f"❌ Erro ao criar gestor: {resp.text}")
        return

    # 3. Login
    print(f"\n🔑 Tentando Login...")
    login_data = {"email": gestor_email, "senha": gestor_pass}
    resp = requests.post(f"{API_URL}/auth/login", json=login_data)
    
    if resp.status_code == 200:
        token_data = resp.json()
        token = token_data["access_token"]
        print(f"✅ Login Sucesso! Token: {token[:10]}...")
    else:
        print(f"❌ Falha no login: {resp.text}")
        return
    
    # Cabeçalho para próximas requisições
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Criar Permissões
    permissoes = ["Visualizar Logs", "Gerenciar Usuários", "Ver Alertas"]
    perm_ids = []
    print("\n🛡️  Criando Permissões...")
    
    for p in permissoes:
        resp = requests.post(f"{API_URL}/permissoes/", json={"nome": p}, headers=headers)
        if resp.status_code in [200, 201]:
            data = resp.json()
            p_id = data.get("id") or data.get("_id")
            perm_ids.append(p_id)
            print(f"   - '{p}' OK (ID: {p_id})")
        else:
            print(f"   - '{p}' Erro: {resp.text}")

    # 5. Criar Perfil
    if perm_ids:
        print(f"\n👤 Criando Perfil 'Analista SOC'...")
        perfil_data = {"nome": "Analista SOC", "permissoes_ids": perm_ids}
        resp = requests.post(f"{API_URL}/perfis/", json=perfil_data, headers=headers)
        
        if resp.status_code in [200, 201]:
            p_data = resp.json()
            perfil_id = p_data.get("id") or p_data.get("_id")
            print(f"✅ Perfil criado: {perfil_id}")

            # 6. Criar Usuário
            print(f"\n👨‍💻 Criando Usuário 'Sherlock'...")
            user_data = {
                "nome": "Sherlock Holmes",
                "email": "sherlock@investigacao.com",
                "perfil_id": perfil_id
            }
            resp = requests.post(f"{API_URL}/usuarios/", json=user_data, headers=headers)
            if resp.status_code == 201:
                print("✅ Usuário criado com sucesso!")
            else:
                print(f"❌ Erro usuário: {resp.text}")
        else:
             print(f"❌ Erro perfil: {resp.text}")

if __name__ == "__main__":
    seed()