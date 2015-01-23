# coding=utf-8
from gluon import current
from sie.SIETabEstruturada import SIETabEstruturada
from sie.SIEProjetos import SIEParticipantesProjs, SIEProjetos
from gluon.html import *

__all__ = [
    "TableAcompanhamento",
    "TableAvaliacao",
    "TableDeferimento"
]


class TableProjetos(object):
    def __init__(self, projetos):
        """

        :type projetos: list
        """
        self.projetos = projetos

        projetosIds = [p["ID_PROJETO"] for p in self.projetos]
        bolsas = current.db(current.db.bolsas.id_projeto.belongs(projetosIds)).select()
        self.bolsas = {bolsa.id_projeto: bolsa.quantidade_bolsas for bolsa in bolsas}

    def arquivos(self, projeto):
        arquivos = current.db(current.db.projetos.id_projeto == projeto["ID_PROJETO"]).select()
        if len(arquivos) > 3:
            n = 1
        return UL([A(arquivo["anexo_nome"], _href=URL(f='download', args=arquivo["arquivo"])) for arquivo in arquivos])

    def coordenador(self, projeto):
        return SIEProjetos().getCoordenador(projeto['ID_PROJETO'])


    def disciplina(self, projeto):
        return SIEProjetos().getDisciplina(projeto['ID_PROJETO'])

    def situacao(self, projeto):
        try:
            return SIETabEstruturada().descricaoDeItem(projeto["SITUACAO_ITEM"], projeto["SITUACAO_TAB"])
        except AttributeError:
            return "Aguardando..."

    def avaliacao(self, projeto):
        try:
            return SIETabEstruturada().descricaoDeItem(projeto["AVALIACAO_ITEM"], projeto["AVALIACAO_TAB"])
        except AttributeError:
            return "Avaliação não cadastrada"

    def bolsa(self, projeto):
        try:
            return str(self.bolsas[projeto["ID_PROJETO"]])
        except KeyError:
            return "Indefinido"

    def observacao(self, projeto):
        avaliacao = current.db((current.db.avaliacao.id_projeto == projeto['ID_PROJETO'])
                               & (current.db.avaliacao.observacao != None)).select().first()
        if avaliacao:
            if avaliacao.observacao:
                return avaliacao.observacao
        return "Nenhuma observação."


class TableAcompanhamento(TableProjetos):
    def __init__(self, participacoes, projetos):
        super(TableAcompanhamento, self).__init__(projetos)
        self.headers = (
            "#",
            "Data de registro",
            "Num. Processo",
            "Título",
            "Função",
            "Situação",
            "Avaliação",
            "Qtd. Bolsas",
            "Arquivos",
            "Observação"
        )
        self.participacoes = participacoes

    def funcao(self, projeto):
        for i, dic in enumerate(self.participacoes):
            if dic["ID_PROJETO"] == projeto["ID_PROJETO"]:
                try:
                    return SIEParticipantesProjs().descricaoDeFuncaoDeParticipante(self.participacoes[i])
                except TypeError:
                    return 'Indefinido'


    def printTable(self):
        def row(p):
            return TR(p['ID_PROJETO'], p['DT_REGISTRO'], p['NUM_PROCESSO'], p['TITULO'], self.funcao(p),
                      self.situacao(p), self.avaliacao(p), self.bolsa(p), self.arquivos(p), self.observacao(p))

        return TABLE(
            THEAD(TR([TH(h) for h in self.headers])),
            TBODY([row(p) for p in self.projetos if p])
        )


class TableDeferimento(TableProjetos):
    def __init__(self, projetos):
        super(TableDeferimento, self).__init__(projetos)
        self.headers = (
            "#",
            "Data de registro",
            "Num. Processo",
            "Título",
            "Situação",
            "Avaliação",
            "Qtd. Bolsas",
            "Arquivos",
            "Observação"
        )

    def printTable(self):
        def row(p):
            return TR(p['ID_PROJETO'], p['DT_REGISTRO'], p['NUM_PROCESSO'], p['TITULO'],
                      p['SITUACAO'], p['AVALIACAO'], self.bolsa(p), self.arquivos(p), self.observacao(p))

        return TABLE(
            THEAD(TR([TH(h) for h in self.headers])),
            TBODY([row(p) for p in self.projetos if p])
        )


class TableAvaliacao(TableProjetos):
    def __init__(self, projetos):
        self.headers = (
            "#",
            "Coordenador",
            "Disciplina",
            "Arquivos",
            "Situação",
            "Avaliação",
            "Qtd. Bolsas",
            "Avaliar"
        )
        super(TableAvaliacao, self).__init__(projetos)

    def avaliar(self, projeto):
        if not SIEProjetos.isAvaliado(projeto):
            uniqueDOMid = "avaliar%d" % projeto["ID_PROJETO"]

            return SPAN(
                A("Aprovar", _id=projeto["ID_PROJETO"], callback=URL('adm', 'aprovarAjax', vars={"ID_PROJETO": projeto["ID_PROJETO"]}),
                  target=uniqueDOMid),
                " | ",
                A("Reprovar", _id=projeto["ID_PROJETO"], _href=URL('adm', 'avaliacaoPerguntas', vars={"ID_PROJETO": projeto["ID_PROJETO"]})),
                _id=uniqueDOMid
            )
        else:
            return "Avaliado"

    def printTable(self):
        def row(p):
            return TR(str(self.projetos.index(p)+1), self.coordenador(p), self.disciplina(p), self.arquivos(p),
                      self.situacao(p), self.avaliacao(p), self.bolsa(p), self.avaliar(p))

        return TABLE(
            THEAD(TR([TH(h) for h in self.headers])),
            TBODY([row(p) for p in self.projetos if p])
        )