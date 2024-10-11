from datetime import date
from abc import ABC, abstractmethod

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def __str__(self):
        return "\n".join([f"{type(t).__name__}: R$ {t.valor:.2f}" for t in self.transacoes])

class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Conta:
    def __init__(self, numero, agencia, cliente):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.saldo = 0
        self.historico = Historico()

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            transacao = Deposito(valor)
            self.historico.adicionar_transacao(transacao)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito deve ser positivo.")

    def sacar(self, valor):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            transacao = Saque(valor)
            self.historico.adicionar_transacao(transacao)
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            return True
        else:
            print("Saldo insuficiente ou valor inválido.")
            return False

    def obter_saldo(self):
        return self.saldo

    def __str__(self):
        return f"Conta {self.numero} - Agência: {self.agencia}, Saldo: R$ {self.saldo:.2f}"

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.saques = 0

    def sacar(self, valor):
        if 0 < valor <= self.saldo + self.limite:
            self.saldo -= valor
            self.saques += 1
            transacao = Saque(valor)
            self.historico.adicionar_transacao(transacao)
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            return True
        else:
            print("Saldo insuficiente ou valor inválido.")
            return False

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento):
        super().__init__(nome, cpf)
        self.data_nascimento = data_nascimento

# Exemplo de uso
if __name__ == "__main__":
    # Criando um cliente
    cliente1 = PessoaFisica("Maria Silva", "123.456.789-00", date(1990, 5, 17))

    # Criando uma conta corrente
    conta1 = ContaCorrente("0001", "1234", cliente1, limite=500.0)

    # Associando a conta ao cliente
    cliente1.adicionar_conta(conta1)

    # Realizando operações
    conta1.depositar(1000)
    conta1.sacar(150)
    conta1.sacar(600)  # Testando limite
    conta1.depositar(200)

    # Exibindo informações
    print(conta1)
    print("Histórico de transações:")
    print(conta1.historico)
