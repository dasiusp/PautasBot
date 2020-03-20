# PautasBot

Bot para o Telegram com o objetivo de organizar pautas de reuniões de uma maneira simplificada.

## Utilizando
Para utilizá-lo da forma que está, adicione o `@pautas_bot` ao seu canal do Telegram, e utilize os comandos

| Comando |   Argumento   |                         Funcionalidade                         |
|---------|:-------------:|:--------------------------------------------------------------:|
| start   | N/A           | Inicializa uma nova pauta                                      |
| add     | Item de Pauta | Adiciona um item à pauta                                       |
| remove  | Item de Pauta | Remove o item digitado da pauta                                |
| list    | N/A           | Lista todos os itens contidos na pauta                         |
| finish  | N/A           | Finaliza a pauta criada, listando todos os itens e finalizando |

## Workflow da aplicação

O bot é feito utilizando a [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot), biblioteca para bots no Python. A implementação de todos os comandos está contida no arquivo [`main`](main.py).

Todos os comandos utilizam um banco de dados `Firestore` por traz, e a lógica para organizar os registros está em [`database`](database.py). Cada chat único (seja individual com o bot ou num chat em grupo) possui um `chat_id`, que será usado como identificador para todas as chamadas.

## Hospedando

Este bot é hospedado na `Google Cloud`, e utiliza dois componentes principais: O `Cloud Functions`, para receber um evento HTTP e repassá-lo para o `webhook` em [`main.py`](main.py) e o `Firestore` para armazenar os registros.

Essa aplicação cabe facilmente no `Free Tier` da `Google Cloud`, portanto não há nenhum medo relacionado ao seu custo.

## Contribuindo

Se você sentir que existe algo que esse bot poderia fazer mas ainda não faz, por favor sinta-se livre para abrir um `Pull Request`!

## Licença

Como descrito em [LICENSE](LICENSE), este bot possui licença MIT. Basicamente, faça o que você quiser, só não nos processe.