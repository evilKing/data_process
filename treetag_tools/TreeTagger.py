import pprint
import treetaggerwrapper


tagger = treetaggerwrapper.TreeTagger(TAGLANG = 'en', TAGDIR = '/Users/hulk/software/tree-tagger/')

tags = tagger.tag_text("Candidates Overview and Analysis")

for tag in tags:
    print(tag.split()[2])

# tags2 = treetaggerwrapper.make_tags(tags)
# pprint.pprint(tags2)



