# Desafio 1: Crawlers
    
    Programa para coletar dados e enviar via Telegram

## Parametros: 

#### - -subrredits: 

    Descrição: Lista de reedits para coletar dados.
    Tipo: List.
    Default: ['programming', 'dogs', 'brazil']

### - -min-score
    
    Descrição: Defini o minimo de score que o usuario deseja ver nos reedits.
    Tipo: Boolean.
    Default: 5000.

## - -pages

    Descrição: Quantidade de paginas que devo percorrer para coletar dados
    Tipo: Boolean.
    Default: 1000.

### - -nada-para-fazer
    
    Descrição: Enviar dados coletados para o Telegram.
    Tipo: Boolean.
    Default: False.

### - -entity 

    Descrição: Numero do telefone ou nome do usuario da sua lista de contato para envio da menssagem. Obrigatório para enviar a menssagem.
    Tipo: String.

## Requerimentos
    
    Para executar este programa devemos ter um abiente python, para mais informações acesse o link https://conda.io/miniconda.html.

    Após a configuração do ambiente Python devemos instalar os seguintes pacotes para a execução do programa: 

        - pip install beautifulsoup4
        - pip install telethon

## Bibliografia

    - https://towardsdatascience.com/introduction-to-the-telegram-api-b0cd220dbed2
    - https://core.telegram.org/api/obtaining_api_id
    - https://core.telegram.org/method/auth.sendCode
    - https://lonamiwebs.github.io/Telethon/index.html
    - https://telethon.readthedocs.io/en/stable/

## Exemplos

    - python crawlers.py 
    - python crawlers.py --subrredits dogs programming --min-score 100 --pages 10 --nada-para-fazer --entity +551199009900

    Ao executar sera necessario temos que digitar o número do usuário
    
imagem: https://github.com/arturAdr/DesafioIdWall/tree/master/Crawlers/exemplo-1.png

    Depois sera enviado um código ao seu telegram e temos que digitar ele

imagem: https://github.com/arturAdr/DesafioIdWall/tree/master/Crawlers/exemplo-2.png

