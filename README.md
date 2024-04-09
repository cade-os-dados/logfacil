# Usage

## Instalation

```bash
pip install git+https://github.com/cade-os-dados/logfacil
```

## Setup

Para iniciar o logging das suas funções, basta chamar a função setup.init(). Isto irá criar um diretório <b>logs</b> no diretório atual. <br>
Além disso, iniciará um arquivo com a data do dia <u> exemplo</u>: 2023-01-04.log

```python
from logfacil import setup

handlers = setup.init()
```

É claro que podemos editar o <i>path</i> onde os logs serão registrados e também o nome dos arquivos de log, bastando alterar os parâmetros na função init.


```python
handlers = setup.init(
    path = 'hello_world.log',
    dir = 'local_onde_quero_guardar_meus_logs'
)
```

Para fechar a conexão com os arquivos de log basta utilizar a função close_all

```python
setup.close_all(handlers)
```

## Registrar log em suas funções

Basta adicionar o decorator onde a função foi definida e, se o logging já foi iniciado, isto é, já foi feita a etapa de setup acima, toda vez que a função for chamada, será automaticamente registrada no arquivo de log.

```python
from logfacil import log

@log.activate
def ola_mundo():
    print('hello world')
```

## Ativar e desativar log

O log pode ser ativado e desativado independentemente da função ter sido declarada com o decorator mostrado acima ou não

```python
# vai parar de registrar o log para este função
ola_mundo = log.deactivate(ola_mundo)

# ativar novamente
ola_mundo = log.activate(ola_mundo)
```

## Integração com OOP

Utilizando a API "Controller", o logfacil irá rastrear todos os métodos do seu objeto que não comecem com "__" (2 vezes <i>underline</i>) e registrará toda vez que estes métodos forem chamados.

```python
from logfacil.log import Controller

class Foo():
    ...

foo = Foo()
controlador = Controller()

# ligar os logs para os metódos do objeto
controlador.enable_logs(foo)

# desligar
controlador.disable_logs(foo)
```

Caso queira que algum método não seja registrado no seu log file, então basta dizer ao controler para ignorá-lo.

```python
# ignora o metodo1 do objeto foo
controlador.ignore(foo, 'metodo1')
```