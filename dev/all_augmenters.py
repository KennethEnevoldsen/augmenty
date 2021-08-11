import sys

sys.path.append(".")
sys.path.append("..")

from wasabi import MarkdownRenderer

import augmenty

md = MarkdownRenderer()
meta = augmenty.meta()
respects = ["token labels", "dependency parsing", "entity labels", "document labels"]
use = ["evaluation", "training"]

table_list = []

for aug, f in sorted(augmenty.augmenters().items()):

    about = meta[aug]

    # description:
    if "description" in about:
        desc = about["description"]
    else:
        desc = f.__doc__.split("\n\n")[0]
        desc = " ".join(desc.split("\n"))

    # respects
    respects_ = ["✅" if r in about["respects"] else "❌" for r in respects]

    # respects
    use_ = ["✅" if r in about["use"] else "" for r in use]

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
    table_list.append(
        (md.bold(aug), desc, *respects_, *use_, ", ".join(aug_refs_strings))
    )


md.add(md.title(1, "Overview of Augmenters"))
md.add(
    "The following tables list all the available augmenters in augmenty, along with a short description. \
It also contains list all of the labels which the augmenters respects. For instance, if you wish to train a named \
entity recognition pipeline you should not use augmenters which do not respect entity labels. \
Similarly, a hint is also given to whether the augmenter is recommended for training or evaluation. Lastly, \
the package includes a list of references to any data or packages used as well as references to example application of the augmenter in practice."
)

table = md.table(
    table_list,
    [
        "Augmenter name",
        "Description",
        "Token",
        "Dependency parsing",
        "Entity",
        "Document",
        "Training",
        "Evaluation",
        "References",
    ],
    aligns=("c", "l", "l", "l", "l", "l", "l", "l", "l"),
)
md.add(table)


with open("../docs/augmenters_overview.md", "w") as f:
    f.write(md.text)
