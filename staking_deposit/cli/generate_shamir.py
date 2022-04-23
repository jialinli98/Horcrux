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
    generate_keys,
    generate_keys_arguments_decorator,
)

languages = get_first_options(MNEMONIC_LANG_OPTIONS)


@click.command(
    help=load_text(['arg_generate_shamir', 'help'], func='generate_shamir'),
)
@click.pass_context
@jit_option(
    callback=captive_prompt_callback(
        lambda mnemonic_language: fuzzy_reverse_dict_lookup(mnemonic_language, MNEMONIC_LANG_OPTIONS),
        choice_prompt_func(lambda: load_text(['arg_mnemonic_language', 'prompt'], func='generate_shamir'), languages),
    ),
    default=lambda: load_text(['arg_mnemonic_language', 'default'], func='generate_shamir'),
    help=lambda: load_text(['arg_mnemonic_language', 'help'], func='generate_shamir'),
    param_decls='--mnemonic_language',
    prompt=choice_prompt_func(lambda: load_text(['arg_mnemonic_language', 'prompt'], func='generate_shamir'), languages),
)
@generate_keys_arguments_decorator
def generate_shamir(ctx: click.Context, mnemonic_language: str, **kwargs: Any) -> None:
    click.echo('NEW MNEMONIC!')
    mnemonics = get_mnemonics(language=mnemonic_language, words_path=WORD_LISTS_PATH)
    click.echo(mnemonics)

    test_mnemonic = ''
    mnemonics_to_check = mnemonics[:]

    while len(mnemonics_to_check) != 0:
        click.clear()
        click.echo(load_text(['msg_mnemonic_presentation']))
        click.echo('\n\n%s\n\n' % mnemonics)
        click.pause(load_text(['msg_press_any_key']))

        click.clear()
        test_mnemonic = reconstruct_mnemonic(click.prompt(load_text(['msg_mnemonic_retype_prompt']) + '\n\n'), WORD_LISTS_PATH)
        if test_mnemonic in mnemonics_to_check:
            mnemonics_to_check.remove(test_mnemonic)
        
    click.clear()
    # Do NOT use mnemonic_password.
    ctx.obj = {'mnemonic': mnemonic, 'mnemonic_password': ''}
    ctx.params['validator_start_index'] = 0
    ctx.forward(generate_keys)


'', '', ''