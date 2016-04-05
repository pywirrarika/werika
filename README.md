# werika
This is a language recognition system for Wixarika(huichol) indigenous language. It can extract sentences with a minimum of three words inside an unknown text sorces. In theory you may be used also for other languages.

## Usage

**Identification**
This script extracts compleate sentences of wixarika from a text file. The file can be written in many languages, and the sentences in wixarika dont't need to be larger than 3 words to be classified. 
python3 idtexto.py [filename.txt]

**Training**

To train the language model the corpus must be stored as nuevo.txt
pyhton3 wixanlp.py
You can also create a index of words that can be confused with wixarika. 
python3 confgen [filename2.txt]

## Licence

GPL v3+

## Thanks

Thanks to Phd. Ivan Vladmimir Meza, and Phd. Carlos Barron Romer for all the help given to me to create this simple script. 
