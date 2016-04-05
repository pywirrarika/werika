# werika
This is a language recognition system for Wixarika(huichol) indigenous language of Mexico. It can extract sentences with a minimum of three words inside an unknown text sorces. In theory you may use this script also for other languages.

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

Thanks to Prof. Ivan Vladmimir Meza, and Prof. Carlos Barron Romer for their invaluable help with this work.
