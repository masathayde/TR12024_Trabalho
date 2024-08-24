# Teleinformática e Redes 1 2024: Simulador Enlace-Físico

- Marco Antônio Souza de Athayde - _180126814_
- Mateus Elias de Macedo - _222011561_
- Victor Hugo Rodrigues Fernandes - _180132041_

## Como utilizar o simulador

Rodar **client_gui.py**, **meio.py** e **server_gui.py** ao mesmo tempo. </br>
O programa **meio.py** pode ser configurado com argumentos adicionais no terminal, escrevendo `python -m meio arg1 arg2 arg3`:
  - Probabilidade de erro (valor entre 0 e 1, padrão é 0.1)
  - Número máximo de erros (padrão é 1)
  - Booleano que indica se o programa deve adicionar erro somente na carga de um quadro, evitando erros em cabeçalhos e trelissas (padrão é True)

Configure **client_gui.py** e **server_gui.py** usando os botões. É necessário que as configurações nos dois programas sejam iguais, ou a comunicação não ocorrerá corretamente. </br>
Em **client_gui.py**, use o campo de texto para escrever uma mensagem, então aperte Enter para adicioná-la ao buffer de envio. </br>
Clique em Enviar, para transmitir as mensagens no buffer. Uma janela adicional com uma imagem do sinal modulado deve aparecer. </br>
