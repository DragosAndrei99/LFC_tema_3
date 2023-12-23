import json

class AFD():
    def __init__(self, path: str):
        self.path = path
        input: dict = self._read_AFD_elements(path)

        self._states = input['Q']
        self._sigma = input['sigma']
        self._initial_state = input['stare_initiala']
        self._final_state = input['F']
        self._input_alphabet = input['alfabet_de_intrare']
        if(self._validate()):
            self._current_state = self._initial_state
            print("Automatul este valid")
            self._display()
        else:
            print("Automatul este invalid")
            quit()

    _states: list[str] = []
    _sigma: list[list[str]] = []
    _initial_state: str = ''
    _final_state: list[str] = []
    _input_alphabet: list[str] = []
    _current_state: str = ''

    def _read_AFD_elements(self, path: str)->dict:
        with open(path) as user_file:
            parsed_json = json.load(user_file)
        return parsed_json

    def _read_word(self)->str:
        word = input('Introduceti un cuvant:' )
        for i, v in enumerate(word):
            if v not in self._input_alphabet:
                print('Cuvantul introdus contine caractere ce nu apartin alfabetului')
                return ''
        return word


    def _validate(self)-> bool:
        has_valid_states = len(self._states) == len(set(self._states))
        has_valid_input_alphabet = len(self._input_alphabet) > 0
        has_valid_sigma_1st_row = set(self._sigma[0][1:]).issubset(set(self._input_alphabet))
        has_valid_sigma_other_rows = True
        for i in range(1, len(self._sigma)):
            if not set(self._sigma[i]).issubset(set(self._states)):
                has_valid_sigma_other_rows = False
        has_valid_initial_state = self._initial_state in self._states
        has_valid_final_state = set(self._final_state).issubset(self._states)

        return (has_valid_states and has_valid_input_alphabet and has_valid_sigma_1st_row and has_valid_sigma_other_rows and has_valid_initial_state and has_valid_final_state)


    def _display(self)->None:
        print('---------------------------------------------------------\n')
        print('M = (' + '{ ' + ', '.join(self._states) + ' }, ' + '{ ' + ', '.join(self._input_alphabet) + ' }, sigma, ' + self._initial_state + ', { ' + ','.join(self._final_state) + ' } )\n')
        print(f'Functia de tranzitie:\n')
        self._display_sigma()

    def _display_sigma(self)->None:
        for i in range(len(self._sigma)):
            print(' | '.join(self._sigma[i]))
            print('--------------------------\n')

    def _process_word(self, word)->None:
        can_process: bool = True
        i: int = 0
        while can_process:
            print(f'({self._current_state, word[i:]}) |- \n')
            letter: str = word[i]
            index_first_letter: int = self._sigma[0].index(letter)
            index_current_state_row: int = int(self._current_state[1])+1

            next_state: str = self._sigma[index_current_state_row][index_first_letter]

            if next_state == '-':
                can_process = False
                print('Blocaj!')

            if len(word)-2 < i:
                can_process = False
                if next_state not in self._final_state:
                    print(f'Starea finala este {next_state} deci cuvantul {word} este RESPINS')
                else:
                    print(f'Starea finala este {next_state} deci cuvantul {word} este ACCEPTAT')

            self._current_state = next_state
            i += 1

    def start_AFD(self):
        keep_reading: bool = True
        while keep_reading: 
            word: str = self._read_word()
            if word:
                self._process_word(word)

            input_keep_reading: str = input('Doriti sa mai introduceti un cuvant? (y/n)')
            keep_reading = True if input_keep_reading == "y" else False
            self._current_state = self._initial_state

if __name__ == '__main__':
    afd = AFD("input_tema_3.json")
    afd.start_AFD()


