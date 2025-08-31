from fastapi import APIRouter, Depends
from models import Usuario, Perfil, Permissao
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, PerfilSchema
from sqlalchemy.orm import Session

order_router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@order_router.get("/")
async def usuarios():
    """_summary_: Essa é a rota padrão de usuários do sistema. Todas as rotas de usuários precisam de autenticação.        
    """
    return {"mensagem": "Você acessou a rota de usuários"}

@order_router.post("/usuario")
async def criar_usuario(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """_summary_: Rota para criação de um novo usuário. Apenas gestores autenticados podem criar usuários.
    
    - **usuario_schema**: Dados do usuário a ser criado, conforme o esquema definido em UsuarioSchema.
    """
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada,  usuario_schema.perfil_id, usuario_schema.gestor_id)
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": f"Usuário criado com sucesso. Usuario: {usuario_schema.email}"}

@order_router.post("/perfil")
async def criar_perfil(perfil_schema: PerfilSchema, session: Session = Depends(pegar_sessao)):
    """_summary_: Rota para criação de um novo perfil. Apenas gestores autenticados podem criar perfis.
    
    - **Perfil**: Cada perfil define um conjunto de permissões que podem ser atribuídas ao usuário. O usuário pode ter apenas um perfil, mas um perfil pode ser atribuído a vários usuários.
    """
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