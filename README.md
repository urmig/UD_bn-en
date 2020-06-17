# Summary


This program crawls Bengali-English tweets and provides for Language, POS, Dependency tags for the normalised text in accordance with the Universal Dependencies.

	Install [Tweepy](https://github.com/tweepy/tweepy)

	Get your Twitter app keys from https://apps.twitter.com/ and put the keys in the ``crawl_tweets.py`` script.


# Crawl Tweets

	python crawl_tweets.py --t DATA/<dev/test/train>_twids.txt  --a DATA/<dev/test/train>_annot.json --o <dev/test/train>_output.conllu# Requirements


# Acknowledgments

Any publication reporting the work done using this data should cite the following papers:

	Ghosh, Urmi, Dipti Misra Sharma, and Simran Khanuja. "Dependency Parser for Bengali-English Code-Mixed Data enhanced with a Synthetic Treebank." Proceedings of the 18th International Workshop on Treebanks and Linguistic Theories (TLT, SyntaxFest 2019). 2019.

@inproceedings{ghosh-etal-2019-dependency,
    title = "Dependency Parser for {B}engali-{E}nglish Code-Mixed Data enhanced with a Synthetic Treebank",
    author = "Ghosh, Urmi  and
      Sharma, Dipti  and
      Khanuja, Simran",
    booktitle = "Proceedings of the 18th International Workshop on Treebanks and Linguistic Theories (TLT, SyntaxFest 2019)",
    month = aug,
    year = "2019",
    address = "Paris, France",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-7810",
    doi = "10.18653/v1/W19-7810",
    pages = "91--99",
}
