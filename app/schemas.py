from . import ma
from .models import (
    Usuario,
    Funcionario,
    Cliente,
    Produto,
    Venda,
    ItemVenda,
    Despesa,
    Endereco,
    Contato,
    Banco
)

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Usuario.
    """
    class Meta:
        model = Usuario
        load_instance = True
        exclude = ('senha',)  # Não incluir a senha na serialização

class FuncionarioSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Funcionario.
    """
    class Meta:
        model = Funcionario
        load_instance = True

class ClienteSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Cliente.
    """
    class Meta:
        model = Cliente
        load_instance = True

class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Produto.
    """
    class Meta:
        model = Produto
        load_instance = True

class VendaSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Venda.
    """
    itens = ma.Nested('ItemVendaSchema', many=True)

    class Meta:
        model = Venda
        load_instance = True

class ItemVendaSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo ItemVenda.
    """
    class Meta:
        model = ItemVenda
        load_instance = True

class DespesaSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Despesa.
    """
    class Meta:
        model = Despesa
        load_instance = True

class EnderecoSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Endereco.
    """
    class Meta:
        model = Endereco
        load_instance = True

class ContatoSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Contato.
    """
    class Meta:
        model = Contato
        load_instance = True

class BancoSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema para serialização e deserialização do modelo Banco.
    """
    class Meta:
        model = Banco
        load_instance = True
