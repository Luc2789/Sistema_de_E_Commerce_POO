# models/relatorio.py
import datetime

class Relatorio:
    def __init__(self, relatorio_id: int, tipo_relatorio: str,
                 data_geracao: datetime.datetime,
                 periodo_inicio: datetime.datetime,
                 periodo_fim: datetime.datetime):
        self.relatorio_id = relatorio_id
        self.tipo_relatorio = tipo_relatorio  # "VENDAS", "ESTOQUE", "CLIENTES" etc.
        self.data_geracao = data_geracao
        self.periodo_inicio = periodo_inicio
        self.periodo_fim = periodo_fim

    def gerarRelatorio(self) -> None:
        print(f"[Relatório] Gerando relatório do tipo '{self.tipo_relatorio}' "
              f"de {self.periodo_inicio.date()} até {self.periodo_fim.date()}...")

    def exportarPDF(self) -> None:
        print(f"[Relatório] Exportando relatório {self.relatorio_id} em PDF...")

    def exportarExcel(self) -> None:
        print(f"[Relatório] Exportando relatório {self.relatorio_id} em Excel...")
