# nvdb

A Python script to extract the plain-text data from the NVdB PDF file.

* Version: 1.0.0
* Date: 2017-01-08
* Author: [Alberto Pettarin](http://www.albertopettarin.it/) ([contact](http://www.albertopettarin.it/contact.html))
* License: Public Domain / CC BY 4.0 / AGPLv3 (see below)

This project is dedicated to the memory of
[Professor Tullio De Mauro](https://it.wikipedia.org/wiki/Tullio_De_Mauro).


## The NVdB

The _Nuovo vocabolario di base della lingua italiana_ (NVdB, 2016-11-23),
curated by **Isabella Chiari** and **Tullio De Mauro**
with the help of **Francesca Ferrucci**,
contains the roughly 7,000 most common
(or perceived as such by native speakers)
Italian words.

See
[the Web page](http://www.internazionale.it/opinione/tullio-de-mauro/2016/12/23/il-nuovo-vocabolario-di-base-della-lingua-italiana)
for details, or consult the
[markdown version available in this repository](article.md).

For archival purposes,
a copy of the PDF file is also stored in this repository,
as [20170108.nvdb.pdf](20170108.nvdb.pdf).
This PDF file was retrieved from the URL
``https://dl.dropboxusercontent.com/u/236058/nuovovocabolariodibase.pdf``
(contained in the page linked above) on 2017-01-08.


## Processed Files

This repository contains the following processed files:

1. [``raw.txt``](raw.txt), which is the raw text
   extracted from the NVdB PDF file:

    ```plain
Internazionale | url
Dizionario
Il Nuovo vocabolario di base
della lingua italiana

A cura di Tullio De Mauro
23 novembre 2016

A

1a s.f. e m.inv., 2a prep., abbagliante p.pres., agg., s.m., abbaiare v.intr. e tr., abbandonare v.tr., abbandonato p.pass., agg., s.m.,
abbandono s.m., abbassare v.tr., abbasso avv., inter., abbastanza avv., abbattere v.tr., abbeverare v.tr., abbigliamento s.m.,
abbinare v.tr., abbonamento s.m., 1abbonare v.tr., abbondante p.pres., agg., abbondare v.intr., abbottonare v.tr., 1abbracciare
v.tr., abbraccio s.m., abbreviare v.tr., abbronzare v.tr., abete s.m., abile agg., abilità s.f.inv., abisso s.m., abitante p.pres., agg.,
s.m., abitare v.intr. e tr., s.m., abitazione s.f., abito s.m., abituale agg., abituare v.tr., abitudine s.f., abolire v.tr., abortire v.in-
tr., aborto s.m., abruzzese agg., s.m. e f., abusare v.intr., abuso s.m., acca s.f. e m.inv., accademia s.f., accademico agg., s.m.,
accadere v.intr., accampamento s.m., accanto avv., accappatoio s.m., accarezzare v.tr., accattone s.m., accavallare v.tr., acceca-
re v.tr., v.intr., accedere v.intr., accelerare v.tr. e intr., acceleratore agg., s.m., accelerazione s.f., accendere v.tr., accendino s.m.,
accennare v.tr. e intr., accenno s.m., accentare v.tr., accertamento s.m., accertare v.tr., acceso p.pass., agg., accesso s.m., acces-
sorio agg., s.m., accetta s.f., accettabile agg., accettare v.tr., acchiappare v.tr., acciacco s.m., acciaio s.m., accidente s.m., acciuga
...
    ```

2. [``nvdb.full.txt``](nvdb.full.txt),
   containing the full info, one word per line:

    ```plain
    a s.f. e m.inv.
    a prep.
    abbagliante p.pres., agg., s.m.
    abbaiare v.intr. e tr.
    abbandonare v.tr.
    abbandonato p.pass., agg., s.m.
    abbandono s.m.
    abbassare v.tr.
    abbasso avv., inter.
    abbastanza avv.
    ...
    ```

3. [``nvdb.words.txt``](nvdb.words.txt),
   containing just the words, one word per line:

    ```plain
    a
    abbagliante
    abbaiare
    abbandonare
    abbandonato
    abbandono
    abbassare
    abbasso
    abbastanza
    abbattere
    ...
    ```

4. [``nvdb.split.txt``](nvdb.split.txt),
   containing the full info, one word per line,
   with word and grammar info separated by a tab character:

    ```plain
    a       s.f. e m.inv.
    a       prep.
    abbagliante     p.pres., agg., s.m.
    abbaiare        v.intr. e tr.
    abbandonare     v.tr.
    abbandonato     p.pass., agg., s.m.
    abbandono       s.m.
    abbassare       v.tr.
    abbasso avv., inter.
    abbastanza      avv.
    ...
    ```

5. [``nvdb.split.justified.txt``](nvdb.split.justified.txt)
   similar to ``nvdb.split.txt``,
   but with space-based left justification instead of tabs:

    ```plain
    a                  s.f. e m.inv.
    a                  prep.
    abbagliante        p.pres., agg., s.m.
    abbaiare           v.intr. e tr.
    abbandonare        v.tr.
    abbandonato        p.pass., agg., s.m.
    abbandono          s.m.
    abbassare          v.tr.
    abbasso            avv., inter.
    abbastanza         avv.
    ...
    ```

The following commands were used to obtain the files:

```bash
$ wget https://dl.dropboxusercontent.com/u/236058/nuovovocabolariodibase.pdf
$ pdftotext nuovovocabolariodibase.pdf > raw.txt
$ python cleanraw.py raw.txt nvdb.full.txt
$ python cleanraw.py raw.txt nvdb.words.txt -w
$ python cleanraw.py raw.txt nvdb.split.txt -s
$ python cleanraw.py raw.txt nvdb.split.justified.txt --split-justify
```


## License

This document is released under the CC BY 4.0 License.

The processed files are released in the public domain.

``cleanraw.py`` is released under the AGPLv3 License.

All materials should be used for research and/or personal purposes only,
and according to the Terms of Service of the NVdB.
