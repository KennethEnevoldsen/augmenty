from .about import __download_url__, __title__, __version__  # noqa
from .augment_utilities import set_doc_level  # noqa
from .augment_utilities import combine, repeat, yield_original  # noqa

# import augmenters
from .character import create_char_random_augmenter_v1  # noqa
from .character import create_char_replace_augmenter_v1  # noqa
from .character import create_char_swap_augmenter_v1  # noqa
from .character import (  # noqa
    create_keystroke_error_augmenter_v1,
    create_random_casing_augmenter_v1,
    create_remove_spacing_augmenter_v1,
)
from .doc import create_paragraph_subset_augmenter_v1  # noqa
from .doc import create_spongebob_augmenter_v1  # noqa
from .doc import create_upper_casing_augmenter_v1  # noqa
from .lang import create_da_historical_noun_casing_augmenter_v1  # noqa
from .lang import create_da_æøå_replace_augmenter_v1  # noqa
from .lang import create_mk  # noqa
from .lang import (  # noqa
    create_qwerty_da,
    create_qwerty_de,
    create_qwerty_el,
    create_qwerty_en,
    create_qwerty_es,
    create_qwerty_fr,
    create_qwerty_hu,
    create_qwerty_it,
    create_qwerty_lt,
    create_qwerty_nb,
    create_qwerty_nl,
    create_qwerty_pl,
    create_qwerty_pt,
    create_qwerty_ro,
    create_ru,
)
from .span import create_ent_augmenter_v1  # noqa
from .span import create_ent_format_augmenter_v1  # noqa
from .span import create_per_replace_augmenter_v1  # noqa
from .token import create_conditional_token_casing_augmenter_v1  # noqa
from .token import create_duplicate_token_augmenter_v1  # noqa
from .token import create_letter_spacing_augmenter_v1  # noqa
from .token import (  # noqa
    create_random_synonym_insertion_augmenter_v1,
    create_spacing_insertion_augmenter_v1,
    create_starting_case_augmenter_v1,
    create_token_insert_augmenter_v1,
    create_token_insert_random_augmenter_v1,
    create_token_replace_augmenter_v1,
    create_token_swap_augmenter_v1,
    create_wordnet_synonym_augmenter_v1,
)
from .util import augmenters, docs, keyboards, load, meta, texts  # noqa
