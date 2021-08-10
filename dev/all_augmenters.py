import sys

sys.path.append(".")
sys.path.append("..")

from wasabi import MarkdownRenderer

import augmenty

md = MarkdownRenderer()
meta = augmenty.meta()


table_list = []
for aug, f in sorted(augmenty.augmenters().items()):

    about = meta[aug]

    # description:
    if "description" in about:
        desc = about["description"]
    else:
        desc = f.__doc__.split("\n")[0]

    # respects
    respects = ", ".join(about["respects"])

    # references
    aug_refs_strings = []
    if "references" in about:
        refs = about["references"]
        for ref in refs:
            r = refs[ref]
            if not isinstance(r, list):
                r = [r]
            for ref_dict in r:
                ref = f"{ref}: "
                ref += md.link(
                    f"{ref_dict['authors']} ({ref_dict['year']})", ref_dict["link"]
                )
                aug_refs_strings.append(ref)

    # Augmenter name, description, respects, references
    table_list.append((aug, desc, respects, ", ".join(aug_refs_strings)))


md.add(md.title(1, "Overview of Augmenters"))
md.add(
    "The following tables list all the available augmenters in augmenty, along with a short description.\
It also list all of the labels which the augmenters respects. For instance if you wish to train an named\
entity recognition pipeline you should not use augmenters which does not respect entity labels. Lastly \
the package includes a list of references to any data or packages used as well as references to example application of the augmenter in practice."
)

table = md.table(
    table_list,
    ["Augmenter name", "Description", "Respects", "References"],
    aligns=("c", "l", "l", "l"),
)
md.add(table)


with open("../docs/augmenters.md", "w") as f:
    f.write(md.text)
