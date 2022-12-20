(TeX-add-style-hook
 "rapport"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "a4paper" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("babel" "francais") ("graphicx" "pdftex") ("adjustbox" "export") ("fontenc" "T1")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art12"
    "inputenc"
    "babel"
    "graphicx"
    "amsmath"
    "amssymb"
    "algorithm"
    "algpseudocode"
    "tikz"
    "subcaption"
    "adjustbox"
    "fontenc"
    "hyperref")
   (TeX-add-symbols
    "HRule")
   (LaTeX-add-labels
    "fig:x example graph")
   (LaTeX-add-bibitems
    "contetomita"))
 :latex)

