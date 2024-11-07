from . import db

class Usuario(db.Model):
    """
    Modelo para a tabela 'usuarios'.
    Armazena informações de login e senha dos usuários.
    """
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)  # Hash da senha

class Funcionario(db.Model):
    """
    Modelo para a tabela 'funcionarios'.
    Armazena informações dos funcionários da empresa.
    """
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50))
    rg = db.Column(db.String(20))
    cpf = db.Column(db.String(11), unique=True)
    cargo = db.Column(db.String(50))
    data_admissao = db.Column(db.Integer)  # Data no formato AAAAMMDD
    conta_bancaria = db.Column(db.String(20))
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos.id'))
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'))

class Cliente(db.Model):
    """
    Modelo para a tabela 'clientes'.
    Armazena informações dos clientes, sejam pessoas físicas ou jurídicas.
    """
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # "Física" ou "Jurídica"
    cpf_cnpj = db.Column(db.String(14), unique=True)
    representante_nome = db.Column(db.String(50))
    representante_sobrenome = db.Column(db.String(50))
    representante_rg = db.Column(db.String(20))
    representante_cpf = db.Column(db.String(11))
    endereco_id = db.Column(db.Integer, db.ForeignKey('enderecos.id'))
    contato_id = db.Column(db.Integer, db.ForeignKey('contatos.id'))

class Produto(db.Model):
    """
    Modelo para a tabela 'produtos'.
    Armazena informações dos produtos disponíveis para venda.
    """
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    peso = db.Column(db.Float)
    quantidade_estoque = db.Column(db.Integer)

class Venda(db.Model):
    """
    Modelo para a tabela 'vendas'.
    Armazena informações das vendas realizadas.
    """
    __tablename__ = 'vendas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_venda = db.Column(db.Integer)  # Data no formato AAAAMMDD
    endereco_envio_id = db.Column(db.Integer, db.ForeignKey('enderecos.id'))
    frete = db.Column(db.Float)
    itens = db.relationship('ItemVenda', backref='venda', lazy=True)

class ItemVenda(db.Model):
    """
    Modelo para a tabela 'itens_venda'.
    Armazena os produtos e quantidades de cada venda.
    """
    __tablename__ = 'itens_venda'
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)

class Despesa(db.Model):
    """
    Modelo para a tabela 'despesas'.
    Armazena informações das despesas da empresa.
    """
    __tablename__ = 'despesas'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    nome = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_despesa = db.Column(db.Integer)  # Data no formato AAAAMMDD

class Endereco(db.Model):
    """
    Modelo para a tabela 'enderecos'.
    Armazena informações de endereços, reutilizáveis por várias entidades.
    """
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(100))
    numero = db.Column(db.String(10))
    bairro = db.Column(db.String(50))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    cep = db.Column(db.String(8))

class Contato(db.Model):
    """
    Modelo para a tabela 'contatos'.
    Armazena informações de contato, reutilizáveis por várias entidades.
    """
    __tablename__ = 'contatos'
    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(15))
    email = db.Column(db.String(100))

class Banco(db.Model):
    """
    Modelo para a tabela 'bancos'.
    Armazena informações bancárias associadas aos funcionários.
    """
    __tablename__ = 'bancos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    agencia = db.Column(db.Integer)
    conta_corrente = db.Column(db.Integer)
    pix = db.Column(db.String(50))
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
