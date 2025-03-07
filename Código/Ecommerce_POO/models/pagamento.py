from enum import Enum
import random

class StatusPagamento(Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"

class Pagamento:
    def __init__(self, pagamento_id: int, pedido, valor_total: float, metodo_pagamento: str, status_pagamento: str):
        self.pagamento_id = pagamento_id
        self.pedido = pedido          # Tipo: Pedido
        self.valor_total = valor_total
        self.metodo_pagamento = metodo_pagamento  # "Cartão", "Boleto", "Pix", etc.
        self.status_pagamento = StatusPagamento(status_pagamento).value   # Usar enum

    def processarPagamento(self) -> bool:
        """Simulação de integração com gateway. Retorna True se aprovado, False caso contrário."""
        print(f"[Pagamento] Processando pagamento de R${self.valor_total} via {self.metodo_pagamento}...")
        # Exemplo: vamos aprovar aleatoriamente
        aprovado = random.choice([True, False])
        if aprovado:
            print(f"[Pagamento] Pagamento APROVADO.")
            self.status_pagamento = StatusPagamento.APROVADO.value
        else:
            print(f"[Pagamento] Pagamento REJEITADO.")
            self.status_pagamento = StatusPagamento.REJEITADO.value
        return aprovado

    def confirmarPagamento(self) -> None:
        if self.status_pagamento != StatusPagamento.APROVADO.value:
            print("[Pagamento] ERRO: Não é possível confirmar, pagamento não está APROVADO.")
            return
        print(f"[Pagamento] Pagamento {self.pagamento_id} confirmado oficialmente.")
        if self.pedido:
            self.pedido.atualizarStatus(StatusPedido.PAGO.value)

    def cancelarPagamento(self) -> None:
        self.status_pagamento = StatusPagamento.REJEITADO.value
        print(f"[Pagamento] Pagamento {self.pagamento_id} cancelado!")
        if self.pedido:
            self.pedido.atualizarStatus(StatusPedido.CANCELADO.value)