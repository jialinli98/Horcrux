import click
from typing import (
    Any,
)

from staking_deposit.key_handling.key_derivation.mnemonic import (
    get_mnemonic,
    reconstruct_mnemonic,
    get_mnemonics,
)
from staking_deposit.utils.click import (
    captive_prompt_callback,
    choice_prompt_func,
    jit_option,
)
from staking_deposit.utils.constants import (
    MNEMONIC_LANG_OPTIONS,
    WORD_LISTS_PATH,
)
from staking_deposit.utils.intl import (
    fuzzy_reverse_dict_lookup,
    load_text,
    get_first_options,
)

from .generate_keys import (
    generate_keys_shamir,
    generate_keys_arguments_decorator,
)

languages = get_first_options(MNEMONIC_LANG_OPTIONS)


@click.command(
    help=load_text(['arg_new_shamir', 'help'], func='new_shamir'),
)
@click.pass_context
@jit_option(
    callback=captive_prompt_callback(
        lambda mnemonic_language: fuzzy_reverse_dict_lookup(mnemonic_language, MNEMONIC_LANG_OPTIONS),
        choice_prompt_func(lambda: load_text(['arg_mnemonic_language', 'prompt'], func='new_shamir'), languages),
    ),
    default=lambda: load_text(['arg_mnemonic_language', 'default'], func='new_shamir'),
    help=lambda: load_text(['arg_mnemonic_language', 'help'], func='new_shamir'),
    param_decls='--mnemonic_language',
    prompt=choice_prompt_func(lambda: load_text(['arg_mnemonic_language', 'prompt'], func='new_shamir'), languages),
)
@generate_keys_arguments_decorator
def new_shamir(ctx: click.Context, mnemonic_language: str, **kwargs: Any) -> None:
    click.pause(load_text(['msg_shamir_mnemonic_intro']).format(numkeys=3, threshold=2))
    mnemonics = get_mnemonics(language=mnemonic_language, words_path=WORD_LISTS_PATH)

    test_mnemonic = ''
    mnemonics_to_check = mnemonics[:]
    print(mnemonics)

    while len(mnemonics_to_check) != 0:

        while mnemonics_to_check[0] != reconstruct_mnemonic(test_mnemonic, WORD_LISTS_PATH):
            click.clear()
            click.echo(load_text(['msg_mnemonic_presentation']).format(keynum=len(mnemonics)-len(mnemonics_to_check)+1, total=len(mnemonics)))
            click.echo('\n\n%s\n\n' % mnemonics_to_check[0][1])
            click.pause(load_text(['msg_press_any_key']))

            click.clear()
            test_mnemonic = click.prompt(load_text(['msg_mnemonic_retype_prompt']).format(keynum=len(mnemonics)-len(mnemonics_to_check)+1, total=len(mnemonics)) + '\n\n')


        mnemonics_to_check.pop(0)
        
    click.clear()
    # Do NOT use mnemonic_password.
    ctx.obj = {'mnemonics': mnemonics, 'mnemonic_password': ''}
    ctx.params['validator_start_index'] = 0
    ctx.forward(generate_keys_shamir)