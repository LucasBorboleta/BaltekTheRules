# Contributing to baltek-the-rules 

👍🎉 Thanks for taking the time to contribute! 🎉👍 


## What languages can you use

In this project, you have to use  English for exchanging, coding and documenting. 

Esperanto, French and Portuguese have been already used only for translating the rules.

All other languages are welcome for translating the rules.

## What can you contribute

* You can start a translation of the rules in a new language.
* You can correct an existing translation.
* You can propose clarification on the rules.
* You can fix coding errors in files (HTML, CSS, ...).
* You can correct the wording in the documentation files.
* You can propose evolution of the rules if the following principles stay satisfied:
  * game easily made by hand,
  * defined by a few rules,
  * without randomizing device.

## How do you exchange

You can exchange by:

* Reporting error or proposing enhancement using the [GitHub](https://github.com) ticketing solution at [baltek-the-rules/issues](https://github.com/LucasBorboleta/baltek-the-rules/issues).
* Proposing code using the [GitHub](https://github.com) pull-request solution at [baltek-the-rules/pulls](https://github.com/LucasBorboleta/baltek-the-rules/pulls).

## How do you get started

* Read the introductory [README](../README.md) document.
* Play the rules, either manually or using [baltek-the-program](https://github.com/LucasBorboleta/baltek-the-program).
* Create a  [GitHub](https://github.com)  account. This is the prerequisite for issuing a ticket.
* If you intent to propose code, then:
  * Learn how to use  [GitHub](https://github.com) in some sandbox project.
  * Read all sections of this document about files, testing...
* Read the [CODE-OF-CONDUCT](./CODE-OF-CONDUCT.md) document about expected behavior of contributors. Most probably, a translation in your native language can be found at https://www.contributor-covenant.org.


## How do you find and store files

Here is the organization of the files:

* The [README](../README.md) file is stored at the root of the project. All other documentation files ([LICENSE](./LICENSE.md), [CONTRIBUTING](./CONTRIBUTING.md)...) are stored in the [docs](./.) folder, itself located at the root of the project. These files are named with capitalized letters leading to words joined with `-` but not with `_`. Their extensions are either `.txt` or `.md`.
* The main files are grouped and stored as packages in the [packages](../pacakges) folder. The present project is the [baltek-the-rules](../pacakges/baltek-the-rules) package. The other packages correspond to imported projects.
* Beneath each package root, the following subfolders group the files according to their types: `html`, `css`, `js`, `pictures`. Going deeper, sub-subfolders might be created if they bring added value.
* Links between files beneath the [packages](../pacakges) folder are always expressed using relative paths.
* At the root of the project, the [index.html](../index.html) file launches the [baltek-the-rules](../pacakges/baltek-the-rules) package, thanks to a minimal amount of code.
* The [tools](../tools) folder provides Python scripts for automation:
  * [update-files.py ](../tools/update-files.py)walks the project file and insert or update the copyright and license text. Some files and folders are excluded from this process. The updated files must provide special tagged lines matching the `license_begin_rule` and `license_end_rule`  (see the script). Also this script duplicates the [LICENSE](../docs/LICENSE.md) and [CONTRIBUTORS](../docs/CONTRIBUTORS.md) files at the root of the the [baltek-the-rules](../pacakges/baltek-the-rules) package.

## How do you test

New and modified HTML files have to be tested manually as follows:

* The [W3C HTML validator](https://validator.w3.org) checks the files without any error.
* All hyperlinks are checked with success. 
* The files are  readable using at least two browsers amongst Chrome, Firefox, Internet Explorer, Opera.
* The files printed as PDF are readable.

## How do you register contributors

The [CONTRIBUTORS.md](./CONTRIBUTORS.md) file registers the Baltekians who are the people have contributed in one of the following ways to the project:

* People who reported issues, then being treated.
* People who proposed code, then being integrated.
* People outside GitHub who get known for their feedbacks as game testers or linguistic correctors.

Developer creating or merging a pull-request, or treating an issue, is responsible for updating the [CONTRIBUTORS.md](./CONTRIBUTORS.md) file with the names of the involved Baltekians.

