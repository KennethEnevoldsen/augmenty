from .about import __version__, __download_url__, __title__

from .util import augmenters, docs, texts, keyboards, load, meta

# import augmenters
from .character import (
    create_char_replace_augmenter,
    create_char_swap_augmenter,
    create_char_random_augmenter,
    create_keystroke_error_augmenter,
    create_random_casing_augmenter,
    create_remove_spacing_augmenter,
)
from .token import (
    create_conditional_token_casing_augmenter,
    create_token_swap_augmenter,
    create_spacing_insertion_augmenter,
    create_grundtvigian_spacing_augmenter,
    create_wordnet_synonym_augmenter,
    create_token_replace_augmenter,
    create_starting_case_augmenter,
)
from .span import (
    create_per_replace_augmenter,
    create_ent_format_augmenter,
    create_ent_augmenter,
)
from .doc import create_upper_casing_augmenter, create_spongebob_augmenter
from .lang import (
    create_ru,
    create_qwerty_ro,
    create_qwerty_pt,
    create_qwerty_pl,
    create_qwerty_nl,
    create_qwerty_nb,
    create_mk,
    create_qwerty_lt,
    create_qwerty_it,
    create_qwerty_fr,
    create_qwerty_es,
    create_qwerty_en,
    create_qwerty_el,
    create_qwerty_de,
    create_da_historical_noun_casing_augmenter,
    create_da_æøå_replace_augmenter,
    create_qwerty_da,
)

from .augment_utilities import combine, set_doc_level, yield_original
