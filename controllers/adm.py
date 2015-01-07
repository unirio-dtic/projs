# coding=utf-8
from sie.SIEProjetos import SIEProjetos
from gluon.tools import Crud
from tables import TableAvaliacao

def cadastro_edicoes():
    edicoes = Crud(db).select(db.edicao)
    form = SQLFORM(db.edicao)

    if form.process().accepted:
        response.flash = 'form accepted'

    return dict(
        edicoes=edicoes if edicoes else "Nenhuma edição cadastrada",
        form=form
    )


def avaliacao():
    if not session.edicao:
        redirect(URL("default", "edicao"))

    ID_CLASSIFICACAO_ENSINO = 40161

    projetos = SIEProjetos().projetosDeEnsino(session.edicao, {"ID_CLASSIFICACAO": ID_CLASSIFICACAO_ENSINO})

    table = TableAvaliacao(projetos)

    return dict(
        projetos=projetos,
        table=table.printTable()
    )