(TeX-add-style-hook
 "diss-full"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("HSEUniversity" "PI" "VKR")))
   (TeX-run-style-hooks
    "latex2e"
    "HSEUniversity"
    "HSEUniversity10")
   (LaTeX-add-labels
    "tbl:example-table"
    "eq:formula-1"
    "eq:formula-2"
    "fig:example-figure")
   (LaTeX-add-bibliographies
    "library.bib"))
 :latex)

