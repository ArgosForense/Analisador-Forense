from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, Perfil, Permissao, Gestor
from dependencies import pegar_sessao, verificar_token, nivel_acesso_gestor
from main import bcrypt_context
from schemas import UsuarioSchema, PerfilSchema
from sqlalchemy.orm import Session
import secrets, string

order_router = APIRouter(prefix="/usuarios", tags=["usuarios"], dependencies=[Depends(verificar_token), Depends(nivel_acesso_gestor)],) 

@order_router.get("/")
async def usuarios():
    """_summary_: Essa é a rota padrão de usuários do sistema. Todas as rotas de usuários precisam de autenticação.        
    """
    return {"mensagem": "Você acessou a rota de usuários"}

@order_router.post("/usuario")
async def criar_usuario(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """_summary_: Rota para criação de um novo usuário. Apenas gestores autenticados podem criar usuários.
    
    O gestor informa dados do usuário: nome, email pessoal e perfil de acesso. O sistema gera email institucional e senha automaticamente, e envia as credenciais para o email pessoal do usuário.
    """
    
    
    senha_aleatoria = gerar_senha_aleatoria()
    senha_criptografada = bcrypt_context.hash(senha_aleatoria)
    email_institucional = gerar_email_institucional(usuario_schema.nome)
    
    novo_usuario = Usuario(usuario_schema.nome, email_institucional, senha_criptografada,  usuario_schema.perfil_id, usuario_schema.gestor_id)
    session.add(novo_usuario)
    session.commit()

    # Envia o email para o email pessoal do usuário com as credenciais#
    enviar_email(usuario_schema.email, email_institucional, senha_aleatoria)
    return {
        "mensagem": f"Usuário criado com sucesso. Credenciais enviadas para {usuario_schema.email}",
        "email_institucional": email_institucional,
        "senha": senha_aleatoria  # Apenas para fins de desenvolvimento, remover em produção
    }
    
@order_router.post("/usuario/desativar/{usuario_id}")
async def desativar_usuario(usuario_id: int, session: Session = Depends(pegar_sessao), pessoa_autenticada = Depends(verificar_token)):
    """_summary_: Rota para desativação de um usuário.
    - Somente gestores podem desativar a conta de um usuário.
    - Usuário desativado não pode mais fazer login no sistema.
    """
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.status = "DESATIVADO"
    session.commit()
    return {"mensagem": f"Usuário número: {usuario.id} desativado com sucesso.",
            "usuario": usuario}

@order_router.post("/usuario/ativar/{usuario_id}")
async def ativar_usuario(usuario_id: int, session: Session = Depends(pegar_sessao), pessoa_autenticada = Depends(verificar_token)):
    """_summary_: Rota para ativação de um usuário.
    - Somente gestores podem ativar a conta de um usuário.
    """
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    usuario.status = "ATIVO"
    session.commit()
    return {"mensagem": f"Usuário número: {usuario.id} Ativado com sucesso.",
            "usuario": usuario}

def gerar_senha_aleatoria(tamanho=10):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

def gerar_email_institucional(nome, dominio="empresa.com"):
    nome_formatado = nome.lower().replace(" ", ".")
    return f"{nome_formatado}@{dominio}"

def enviar_email(destinatario, email_institucional, senha):
    corpo = f"Seu acesso foi criado!\nEmail institucional: {email_institucional}\nSenha: {senha}"
    print(f"[DEV] Simulando envio de email para {destinatario}:\n{corpo}")
    # Em ambiente de produção será necessário vincular a uma API, como do office365 ou Microsoft Graph!
    

@order_router.post("/perfil")
async def criar_perfil(perfil_schema: PerfilSchema, session: Session = Depends(pegar_sessao), pessoa_autenticada = Depends(verificar_token)):
    """_summary_: Rota para criação de um novo perfil. Apenas gestores autenticados podem criar perfis.
    
    - **Perfil**: Cada perfil define um conjunto de permissões que podem ser atribuídas ao usuário. O usuário pode ter apenas um perfil, mas um perfil pode ser atribuído a vários usuários.
    """
    # Se o objeto autenticado não for uma instancia da classe gestor, então bloqueie a ação
    
    novo_perfil = Perfil(perfil_schema.nome, []) # Cria o perfil sem permissões inicialmente
    session.add(novo_perfil)
    session.commit()
     # Adiciona as permissões ao perfil
    for permissao_schema in perfil_schema.permissoes:
        permissao = session.query(Permissao).filter_by(nome=permissao_schema.nome).first()
        if permissao:
            novo_perfil.permissoes.append(permissao)
    session.commit()
    return {"mensagem": f"Perfil criado com sucesso. Perfil: {perfil_schema.nome}"}

permissoes_router = APIRouter(prefix="/permissoes", tags=["permissoes"], dependencies=[Depends(verificar_token), Depends(nivel_acesso_gestor)],)

@permissoes_router.post("/permissao")
async def criar_permissao(
    nome: str,
    session: Session = Depends(pegar_sessao)
):
    """
    Rota para criação de uma nova permissão. 
    - Apenas gestores autenticados podem criar permissões.
    """
    
    # Verifica se já existe uma permissão com esse nome
    permissao_existente = session.query(Permissao).filter_by(nome=nome).first()
    if permissao_existente:
        raise HTTPException(status_code=400, detail="Permissão já existe")
    
    nova_permissao = Permissao(nome=nome)
    session.add(nova_permissao)
    session.commit()
    return {"mensagem": f"Permissão '{nome}' criada com sucesso.", "permissao_id": nova_permissao.id}