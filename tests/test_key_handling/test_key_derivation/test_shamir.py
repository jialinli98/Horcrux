import os
import json
from py_ecc.bls import G2ProofOfPossession as bls
import pytest
from secrets import randbits

import random


from staking_deposit.utils.constants import (
    MNEMONIC_LANG_OPTIONS,
)
from staking_deposit.key_handling.key_derivation.mnemonic import (
    get_mnemonic,
    reconstruct_mnemonic,
    #added
    get_mnemonics,
    rec
)
from staking_deposit.utils.crypto import (
    Shamir_reconstruct,
    Shamir_split
)


test_vector_filefolder = os.path.join(os.getcwd(), 'tests', 'test_key_handling',
                                      'test_key_derivation', 'test_vectors', 'shamir.json')
with open(test_vector_filefolder, 'r') as f:
    test_vectors = json.load(f)['shamir_tests']


WORD_LISTS_PATH = os.path.join(os.getcwd(), 'staking_deposit', 'key_handling', 'key_derivation', 'word_lists')
all_languages = MNEMONIC_LANG_OPTIONS.keys()


def test_shamir_reconstruct():
    entropy = randbits(256).to_bytes(32, 'big')

    entropy1 = entropy[:16]

    splitkeys = Shamir_split(3, 2, entropy1)

    remover = random.randint(1,3)

    splitkeys.pop(remover - 1)

    recovered = Shamir_reconstruct(splitkeys)

    assert(recovered, entropy1)


@pytest.mark.parametrize(
    'test',
    test_vectors
)
def test_shamir_mnemonic_reconstruct(test):
    schemeinfo = test['scheme'].split("of")
    
    assert shamir_reconstruct()
    assert shamir_split(test['master-secret'], test['scheme']) == test['mnemonics']


def test_shamir_generate():
    mnemonics = get_mnemonics(language="English", words_path=WORD_LISTS_PATH)

