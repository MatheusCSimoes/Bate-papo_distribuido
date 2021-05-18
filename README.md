# Bate-papo
 Tarefa de laboratório para matéria de Sistemas Distribuidos da UFRJ 2020.2 ministrada pela professora Silvada do DCC.

 Objetivo da atividade está descrito no documento lab4-parte2.pdf

 Atividade desenvolvida em dupla pelos alunos:
 
    - Matheus Simões 
    - Daniel Jimenez

Para iniciar o servidor: mainServer.py \
Para iniciar usuários: mainUser.py 

Na tela inicial do usuário, ao clicar em conectar, é chamado o método "connect" da classe User em user.py. Nesse método é iniciado uma nova thread onde ficará o servidor do lado do usuário. Além disso, é enviado uma mensagem ao servidor central com o endereço do usuário.