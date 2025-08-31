from fastapi import APIRouter, Depends
from models import Usuario, Perfil
from dependencies import pegar_sessao
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
    novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, usuario_schema.senha,  usuario_schema.perfil_id, usuario_schema.gestor_id)
    session.add(novo_usuario)
    session.commit()
    return {"mensagem": f"Usuário criado com sucesso. Usuario: {usuario_schema.email}"}

@order_router.post("/perfil")
async def criar_perfil(perfil_schema: PerfilSchema, session: Session = Depends(pegar_sessao)):
    """_summary_: Rota para criação de um novo perfil. Apenas gestores autenticados podem criar perfis.
    
    - **Perfil**: Cada perfil define um conjunto de permissões que podem ser atribuídas ao usuário. O usuário pode ter apenas um perfil, mas um perfil pode ser atribuído a vários usuários.
    """
    novo_perfil = Perfil(perfil_schema.nome, ",".join(perfil_schema.permissoes)) # Converte a lista de permissões em uma string separada por vírgulas
    session.add(novo_perfil)
    session.commit()
    return {"mensagem": f"Perfil criado com sucesso. Perfil: {perfil_schema.nome}"}