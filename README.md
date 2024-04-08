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

setup.init()
```

É claro que podemos editar o <i>path</i> onde os logs serão registrados e também o nome dos arquivos de log, bastando alterar os parâmetros na função init.


```python
setup.init(
    path = 'hello_world.log',
    dir = 'local_onde_quero_guardar_meus_logs'
)
```

## Registrar log em suas funções

Basta adicionar o decorator onde a função foi definida e, se o logging já foi iniciado, isto é, já foi feita a etapa de setup acima, toda vez que a função for chamada, será automaticamente registrada no arquivo de log.

```python
from logfacil import log

@log.activate
def ola_mundo():
    print('hello world')
```

## Further on

- Providenciar uma api para desativar o registro de log da função
- Providenciar uma api para que todos os metodos de uma função tenham o log ativado e outra para que todos sejam desativados
