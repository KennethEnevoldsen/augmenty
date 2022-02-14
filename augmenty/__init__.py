from .about import __version__, __download_url__, __title__  # noqa

from .util import augmenters, docs, texts, keyboards, load, meta  # noqa

# import augmenters
from .character import (  # noqa
    create_char_replace_augmenter_v1,
    create_char_swap_augmenter_v1,
    create_char_random_augmenter_v1,
    create_keystroke_error_augmenter_v1,
    create_random_casing_augmenter_v1,
    create_remove_spacing_augmenter_v1,
)
from .token import (  # noqa
    create_conditional_token_casing_augmenter_v1,
    create_token_swap_augmenter_v1,
    create_spacing_insertion_augmenter_v1,
    create_letter_spacing_augmenter_v1,
    create_wordnet_synonym_augmenter_v1,
    create_token_replace_augmenter_v1,
    create_starting_case_augmenter_v1,
    create_token_insert_random_augmenter_v1,
    create_token_insert_augmenter_v1,
    create_random_synonym_insertion_augmenter_v1,
    create_duplicate_token_augmenter_v1,
)
from .span import (  # noqa
    create_per_replace_augmenter_v1,
    create_ent_format_augmenter_v1,
    create_ent_augmenter_v1,
)
from .doc import (  # noqa
    create_upper_casing_augmenter_v1,
    create_spongebob_augmenter_v1,
    create_paragraph_subset_augmenter_v1,
)
from .lang import (  # noqa
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
    create_da_historical_noun_casing_augmenter_v1,
    create_da_æøå_replace_augmenter_v1,
    create_qwerty_da,
)

from .augment_utilities import combine, set_doc_level, yield_original, repeat  # noqa
