import traceback, argparse, textwrap, re

class Command(object):

    @classmethod
    def manipulate_string(cls, args):

        try:

            # Criando um objeto StringManipulator 
            # como os argumentos passados pelo o usuario
            _sManipulator = StringManipulator(args.text, args.characters_line)

            # Gerando a String manipulada conforme o solicitado
            _final_string = _sManipulator.manipulate()

            # Listando no console a string 
            print('%s\n' % '\n'.join(_final_string))

        except Exception as e:
            traceback.print_exc()
            raise e

    @classmethod
    def cmd(cls, *args, **kwargs):

        try:

            # Declarando os arugumentos que o programa aceita
            _parse = argparse.ArgumentParser(description='Manipulador de strings')
            _parse.add_argument('-t', '--text', help = 'Texto para manipular string', 
                default='And God said, "Let there be light," and there was light. God saw that the light was good, and he separated the light from the darkness. God called the light "day," and the darkness he called "night." And there was evening, and there was morning - the first day.')
            _parse.add_argument('-cl', '--characters-line', default=40, type=int, help = 'Numero maximo de caracteres por linha')
            _parse.set_defaults(func=cls.manipulate_string)
    
            _args_cmd = _parse.parse_args() 
            if(hasattr(_args_cmd, 'func')):
                _args_cmd.func(_args_cmd)

        except Exception as e:
            traceback.print_exc()
            raise e

class StringManipulator(object):

    __lead_re__ = re.compile(r'(^\s+)(.*)$')

    def __init__(self, text, characters_line):

        self.text = text
        self.characters_line = characters_line

    def manipulate(self):
        
        # No primenro momento eu splito a string pela quantidade de caraceteres
        _splitted = textwrap.wrap(self.text, self.characters_line) 
        
        wrapped = []

        # percorro a lista ate que ela fique vazia
        while len(_splitted) > 0:
            # retiro a linha da lista
            line = _splitted.pop(0)
            # e envio ela para alinhar
            aligned = self.__align_string(line)
            # salvo a linha alinhada na lista
            wrapped.append(aligned)
        
        return wrapped

    def __align_string(self, s):

        items_len = lambda l: sum([ len(x) for x in l] )

        # Detctando e salvando espacos em branco
        m = self.__lead_re__.match(s) 
        if m is None:
            left, right, w = '', s, self.characters_line
        else:
            left, right, w = m.group(1), m.group(2), width - len(m.group(1))

        items = right.split()

        # adicionando o espaço necessario para cada palavra
        for i in range(len(items) - 1):
            items[i] += ' '

        # Numeros de espacos para adicionar
        left_count = w - items_len(items)
        while left_count > 0 and len(items) > 1:
            for i in range(len(items) - 1):
                items[i] += ' '
                left_count -= 1
                if left_count < 1:  
                    break

        res = left + ''.join(items)
        return res

if __name__ == '__main__':
    Command.cmd()

