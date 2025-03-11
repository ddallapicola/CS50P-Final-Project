import question as qs
import project as gen
from unittest.mock import patch

def test__edit_q_correctness():
    with patch('builtins.input', side_effect=["2"]):
        question = qs.Question("How many legs a spider have?",['Zero legs', 'Four legs', 'Six legs', 'Eight legs'],['Eight legs'])
        result = gen._edit_q_correctness(question)
    assert result == qs.Question("How many legs a spider have?",['Zero legs', 'Four legs', 'Six legs', 'Eight legs'],['Eight legs', 'Zero legs'])

def test__edit_q_option():
    with patch('builtins.input', side_effect=["2", "One single leg"]):
        question = qs.Question("How many legs a spider have?",['Zero legs', 'Four legs', 'Six legs', 'Eight legs'],['Eight legs'])
        result = gen._edit_q_option(question)
    assert result == qs.Question("How many legs a spider have?",['One single leg', 'Four legs', 'Six legs', 'Eight legs'],['Eight legs'])

def test__get_list_opts_anss():
    with patch('builtins.input', side_effect=["3", "Wrong Ans. 1", "n", "Correct Ans. 1", "y", "Wrong Ans. 2", "n"]):
        options, answers = gen._get_list_opts_anss()
    assert options == ['Wrong Ans. 1', 'Correct Ans. 1', 'Wrong Ans. 2']
    assert answers == ['Correct Ans. 1']