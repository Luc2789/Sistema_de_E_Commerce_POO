import datetime
from enum import Enum

class StatusEntrega(Enum):
    AGUARDANDO_ENVIO = "AGUARDANDO_ENVIO"
    EM_TRANSITO = "EM_TRANSITO"
    ENTREGUE = "ENTREGUE"

class Entrega:
    def __init__(self, entrega_id: int, pedido, data_envio: datetime.datetime, data_entrega_prevista: datetime.datetime, codigo_rastreio: str, status_entrega: str):
        self.entrega_id = entrega_id
        self.pedido = pedido           # Tipo: Pedido
        self.data_envio = data_envio
        self.data_entrega_prevista = data_entrega_prevista
        self.codigo_rastreio = codigo_rastreio
        self.status_entrega = StatusEntrega(status_entrega).value  # Usar enum

    def atualizarStatusEntrega(self, novo_status: str) -> None:
        novo_status_enum = StatusEntrega(novo_status)
        if novo_status_enum == StatusEntrega.EM_TRANSITO and self.status_entrega != StatusEntrega.AGUARDANDO_ENVIO.value:
            print(f"ERRO: Entrega {self.entrega_id} não pode entrar em trânsito sem estar aguardando envio.")
            return
        if novo_status_enum == StatusEntrega.ENTREGUE and self.status_entrega != StatusEntrega.EM_TRANSITO.value:
            print(f"ERRO: Entrega {self.entrega_id} não pode ser entregue sem estar em trânsito.")
            return
        self.status_entrega = novo_status_enum.value
        print(f"[Entrega] Status da entrega {self.entrega_id} atualizado para {self.status_entrega}.")
        if self.pedido:
            self.pedido.atualizarStatus(StatusPedido.ENVIADO.value if novo_status_enum == StatusEntrega.EM_TRANSITO else StatusPedido.ENTREGUE.value)

    def gerarCodigoRastreio(self) -> None:
        import random
        self.codigo_rastreio = f"TRK{random.randint(1000, 9999)}"
        print(f"[Entrega] Código de rastreio gerado: {self.codigo_rastreio}")