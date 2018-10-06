import traceback, argparse, requests
from bs4 import BeautifulSoup
from telethon import TelegramClient, utils
import telethon.sync
from telethon.tl.functions.messages import SendMessageRequest

class Command(object):

    @classmethod
    def execute_crawler(cls, args):

        try:

            # Instanciando um objeto Crawler
            _crawler = Crawler(args.subrredits, args.min_score, 
                args.pages, args.send_message, args.entity)

            # Coletando as informações
            _crawler.collect()
            
            # Listando resultados no terminal
            if args.show:
                _crawler.show()

            # Enviando o resultado por menssagem             
            if _crawler.send_message:
                _crawler.send()
                _crawler.client.disconnect()

        except Exception as e:
            traceback.print_exc()
            raise e

    @classmethod
    def cmd(cls, *args, **kwargs):

        try:

            # Declarando os arugumentos que o programa aceita
            _parse = argparse.ArgumentParser(description='Crawler')

            _parse.add_argument('-sb', '--subrredits', nargs='+',  default=['programming', 
                'dogs', 'brazil'], help = 'Lista de reedits')

            _parse.add_argument('-nda', '--nada-para-fazer', dest="send_message", action='store_true', default=False, 
                help = 'Enviar dados coletados para o Telegram')
            
            _parse.add_argument('-s', '--show', action='store_true', default=True, 
                help = 'Listar Dados no console')

            _parse.add_argument('-min', '--min-score', type=int, default=5000, 
                help = 'Minimo Score para consulta')

            _parse.add_argument('-pg', '--pages', type=int, default=1000, 
                help = 'Quantidade de paginas usado para consulta')

            _parse.add_argument('-e', '--entity', 
                help="Numero do telefone ou nome do usuario da sua lista de contato para envio da menssagem")

            _parse.set_defaults(func=cls.execute_crawler)
    
            _args_cmd = _parse.parse_args() 
            if(hasattr(_args_cmd, 'func')):
                _args_cmd.func(_args_cmd)

        except Exception as e:
            traceback.print_exc()
            raise e

class Crawler(object):

    def __init__(self, subrredits, min_score, pages, send_message, entity):

        self._api_base = "https://old.reddit.com"
        self.subrredits = subrredits
        self.min_score = min_score
        self.pages = pages
        self.data = []
        self.send_message = send_message
        self.api_id = 393731
        self.api_hash = 'c9063f355bcb76b0267dfddde0bc5744'
        self.username = 'Artur Ribeiro'
        # Verificando se devo enviar menssagem
        if self.send_message:
            # Vertificando se eu tenho o numero do usuario pois isto eh obrigatorio para mandar a menssagem
            if not entity:
                # Caso o usuario nao tenha passado eu gero um execao
                raise AttributeError("O numero do usuario é obrigatorio ser informado para a enviar a menssagem")
            # Inicio a Conexao como a api do Telegram 
            self.client = TelegramClient(self.username, self.api_id, self.api_hash)
            self.client.start()
            # Recupero o usuario conforme os meus contatos            
            self.entity = self.client.get_entity(entity)
            self.peer = utils.get_input_peer(self.entity)

    @property
    def api(self):

        try:
            return '/r/{}/?count={}'.join([self._api_base, ''])
        except Exception as ex:
            traceback.print_exc()
            raise ex

    def collect(self):

        try:
            # Percorro a lista de subrredits que o usuario digitou
            for subrredit in self.subrredits:

                # Formo a url do subrredit
                _url = self.api.format(subrredit, 0)

                # Depois percorro a quantidade de paginas que o usuario
                #  deseja procurar por subrredit
                for p in range(self.pages):
                    
                    # Envio a requisicao
                    _response = self.__send_request(_url)

                    # Validando se o resonse eh valido 
                    if _response:
                        # Converto o resultado
                        _soup = self.__parser(_response.text, subrredit)

                        # Verificando se tenho mais paginas para coletar
                        # pois nem todos os subrredits tem a quantidade de paginas
                        # que o usuario solicitou
                        _next_url = _soup.find("span", {"class": "next-button"})

                        if _next_url:
                            _url = _next_url.a.attrs.get('href')
                        else:
                            # Se nao eu saio deste loop para o proximo subrredit
                            break 
                    else:
                        # Se nao e saio deste loop para o proximo subrredit
                        break


        except Exception as ex:
            traceback.print_exc()
            raise ex

    def __parser(self, data, subrredit): 

        try:
            # Criando o objeto soup
            _soup = BeautifulSoup(data, 'html.parser')

            # Buscanso todos os artigos
            _articles = _soup.find_all("div", {"class": "thing"})

            # COnvertendo os artigos que encontramos em dicionarios
            for article in _articles:

                # Recuperando do artigo a variavel Score
                _score = article.attrs.get("data-score")

                # E caso o score dela eh maior igual 
                # ao minimo score solicitado pelo usuario 
                # eu crio um dicionario com as informacoes 
                # para ser usado depois
                if int(_score) >= self.min_score: 

                    _subrredit = subrredit
                    _url_comments = article.attrs.get("data-permalink")
                    _url = article.attrs.get("data-url")
                    _title = article.find_all("p", {"class": "title"})[0].text

                    self.data.append({
                        "subrredit": _subrredit,
                        "score": _score,
                        "titulo": _title,
                        "comentarios": self._api_base + _url_comments,
                        "url": _url
                    })

            return _soup

        except Exception as ex:
            traceback.print_exc()
            raise ex

    def __send_request(self, url): 

        try:

            _session = requests.Session()
            # Criando um User-Agent qualquer para que 
            # o site https://old.reddit.com nao entenda que eh um bot malicioso
            _headers = {
                'User-Agent': 'My User Agent 1.0',
                'From': 'youremail@domain.com'
            }

            _response = _session.get(url, headers=_headers)

            if _response.status_code > 400:
                raise

            return _response

        except Exception as ex:
            print("Erro na request da url {}".format(url))
            return None
    
    def __formater(self, data):

        try:
            # Retorno uma srting formatada 
            # a partir do dicionario data
            return "Subrredit : {}\n"\
            "Titulo: {}\n"\
            "Score: {}\n"\
            "Comentatios: {}\n"\
            "Url: {}\n".format(data['subrredit'], 
            data['titulo'], data['score'], 
            data['comentarios'], data['url'])
        except Exception as ex:
            traceback.print_exc()
            raise ex

    def show(self):

        # Listando todos os dados coletados
        for data in self.data:

            print(self.__formater(data))
        
    def send(self):

        _results = []
        # Enviando menssagens conforme os dados coletados
        for data in self.data:
            _results.append(self.client(SendMessageRequest(self.peer, self.__formater(data))))

        return _results

if __name__ == '__main__':
    Command.cmd()