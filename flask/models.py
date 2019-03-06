from app import db


# modelos do SQLAlchemy
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    profissao = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Pessoa %r>' % self.id


# modelos do SQLAlchemy
class TipoServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('atendimento', 'alocacao', name='types'), nullable=False)
    nome = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<TipoServico %r>' % self.id


class Doutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Doutor %r>' % self.id


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problema = db.Column(db.Text, nullable=False)
    dh_agendamento_cliente = db.Column(db.Date, nullable=False)
    cep = db.Column(db.String(8), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    cidade = db.Column(db.String(80), nullable=True)
    bairro = db.Column(db.String(80), nullable=True)
    logradouro = db.Column(db.String(80), nullable=True)
    numero = db.Column(db.String(80), nullable=True)
    complemento = db.Column(db.String(80), nullable=True)
    longitude = db.Column(db.Float(20, 15), nullable=False)
    latitude = db.Column(db.Float(20, 15), nullable=False)
    tipo = db.Column(
        db.Enum('atendimento', 'alocacao', name='types'),
        nullable=False
    )
    id_tipo_servico = db.Column(
        db.Integer,
        db.ForeignKey('tipo_servico.id'),
    )
    tipo_servico = db.relationship('TipoServico', backref=db.backref('jobs', lazy=True))
    id_doutor = db.Column(
        db.Integer,
        db.ForeignKey('doutor.id'),
        nullable=False
    )
    doutor = db.relationship('Doutor', backref=db.backref('jobs', lazy=True))

    def __repr__(self):
        return '<Job %r>' % self.id


class CustoAtendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_job = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    job = db.relationship('Job', backref=db.backref('custos', lazy=True))
    id_atendimento = db.Column(db.Integer, nullable=False)
    id_doutor = db.Column(db.Integer, db.ForeignKey('doutor.id'), nullable=False)
    doutor = db.relationship('Doutor', backref=db.backref('custos', lazy=True))
    dh_ult_encerramento = db.Column(db.Date, nullable=False)
    dt_ciclo = db.Column(db.Date, nullable=False)
    dt_previsao_pagamento = db.Column(db.Date, nullable=False)
    dt_pagamento = db.Column(db.Date, nullable=True)
    dt_ult_agendamento = db.Column(db.Date, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    trimestre = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    valor_atendimento = db.Column(db.Float(10, 2), nullable=False)
    valor_horas_extras = db.Column(db.Float(10, 2), nullable=False)
    valor_reembolso = db.Column(db.Float(10, 2), nullable=False)
    total_atendimento = db.Column(db.Float(10, 2), nullable=False)

    def __repr__(self):
        return '<Custo %r>' % self.id
