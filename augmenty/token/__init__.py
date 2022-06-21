from .casing import create_conditional_token_casing_augmenter_v1  # noqa
from .casing import create_starting_case_augmenter_v1  # noqa
from .insert import create_duplicate_token_augmenter_v1  # noqa
from .insert import (  # noqa
    create_random_synonym_insertion_augmenter_v1,
    create_token_insert_augmenter_v1,
    create_token_insert_random_augmenter_v1,
)
from .replace import create_token_replace_augmenter_v1  # noqa
from .replace import create_wordnet_synonym_augmenter_v1  # noqa
from .spacing import create_letter_spacing_augmenter_v1  # noqa
from .spacing import create_spacing_insertion_augmenter_v1  # noqa
from .swap import create_token_swap_augmenter_v1  # noqa
