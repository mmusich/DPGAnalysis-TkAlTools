#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage of the script:"
  echo "$0 <iovList> <outputFile>"
  echo "<iovList> = List containing used IOV:s"
  echo "<outputFile> = Name given to the output file"
  exit
fi

IOVLIST="$1"
LATEXFILE="$2"

# Create a template for the presentation in which the figures can be shown in a nice way
printf "\\\\documentclass{beamer}\n" > $LATEXFILE
printf "\\\\usepackage[T1]{fontenc}\n" >> $LATEXFILE
printf "\\\\usepackage[utf8]{inputenc}\n" >> $LATEXFILE
printf "\\\\usepackage[english]{babel}\n" >> $LATEXFILE
printf "\\\\usepackage{amssymb}\n" >> $LATEXFILE
printf "\\\\usepackage[amssymb]{SIunits}\n" >> $LATEXFILE
printf "\n" >> $LATEXFILE
printf "\setbeamertemplate{navigation symbols}{} %%remove navigation symbols\n" >> $LATEXFILE
printf "\n" >> $LATEXFILE
printf "\\\\usetheme{Madrid}\n" >> $LATEXFILE
printf "\\\\author{Jussi Viinikainen}\n" >> $LATEXFILE
printf "\\\\title[JetHT plots]{JetHT plot collection}\n" >> $LATEXFILE
printf "\n" >> $LATEXFILE
printf "\\\\begin{document}\n" >> $LATEXFILE
printf "\n" >> $LATEXFILE
printf "\\\\begin{frame}\n" >> $LATEXFILE
printf "\\\\frametitle{IOV integrated \$d_{z}\$ and \$d_{xy}\$ error trends}\n" >> $LATEXFILE
printf "  \\\\begin{columns}[c,onlytextwidth]\n" >> $LATEXFILE
printf "    \\\\begin{column}{0.48\\\\textwidth}\n" >> $LATEXFILE
printf "      \\\\begin{center}\n" >> $LATEXFILE
printf "        \\\\includegraphics[width=13em]{figures/dxyErrVsPt_allIovs}\n" >> $LATEXFILE
printf "      \\\\end{center}\n" >> $LATEXFILE
printf "      \\\\begin{center}\n" >> $LATEXFILE
printf "        \\\\includegraphics[width=13em]{figures/dxyErrVsPhi_allIovs}\n" >> $LATEXFILE
printf "      \\\\end{center}\n" >> $LATEXFILE
printf "    \\\\end{column}\n" >> $LATEXFILE
printf "    \\\\begin{column}{0.48\\\\textwidth}\n" >> $LATEXFILE
printf "      \\\\begin{center}\n" >> $LATEXFILE
printf "        \\\\includegraphics[width=13em]{figures/dzErrVsPt_allIovs}\n" >> $LATEXFILE
printf "      \\\\end{center}\n" >> $LATEXFILE
printf "      \\\\begin{center}\n" >> $LATEXFILE
printf "        \\\\includegraphics[width=13em]{figures/dzErrVsPhi_allIovs}\n" >> $LATEXFILE
printf "      \\\\end{center}\n" >> $LATEXFILE
printf "    \\\\end{column}\n" >> $LATEXFILE
printf "  \\\\end{columns}\n" >> $LATEXFILE
printf "\\\\end{frame}\n" >> $LATEXFILE
printf "\n" >> $LATEXFILE
while read line 
do
  printf "\\\\begin{frame}\n" >> $LATEXFILE
  printf "\\\\frametitle{\$d_{z}\$ and \$d_{xy}\$ error trends for IOV ${line}}\n" >> $LATEXFILE
  printf "  \\\\begin{columns}[c,onlytextwidth]\n" >> $LATEXFILE
  printf "    \\\\begin{column}{0.48\\\\textwidth}\n" >> $LATEXFILE
  printf "      \\\\begin{center}\n" >> $LATEXFILE
  printf "        \\\\includegraphics[width=13em]{figures/dxyErrVsPt_iov${line}}\n" >> $LATEXFILE
  printf "      \\\\end{center}\n" >> $LATEXFILE
  printf "      \\\\begin{center}\n" >> $LATEXFILE
  printf "        \\\\includegraphics[width=13em]{figures/dxyErrVsPhi_iov${line}}\n" >> $LATEXFILE
  printf "      \\\\end{center}\n" >> $LATEXFILE
  printf "    \\\\end{column}\n" >> $LATEXFILE
  printf "    \\\\begin{column}{0.48\\\\textwidth}\n" >> $LATEXFILE
  printf "      \\\\begin{center}\n" >> $LATEXFILE
  printf "        \\\\includegraphics[width=13em]{figures/dzErrVsPt_iov${line}}\n" >> $LATEXFILE
  printf "      \\\\end{center}\n" >> $LATEXFILE
  printf "      \\\\begin{center}\n" >> $LATEXFILE
  printf "        \\\\includegraphics[width=13em]{figures/dzErrVsPhi_iov${line}}\n" >> $LATEXFILE
  printf "      \\\\end{center}\n" >> $LATEXFILE
  printf "    \\\\end{column}\n" >> $LATEXFILE
  printf "  \\\\end{columns}\n" >> $LATEXFILE
  printf "\\\\end{frame}\n" >> $LATEXFILE
  printf "\n" >> $LATEXFILE
done < $IOVLIST
printf "\\\\end{document}" >> $LATEXFILE

# Compile the slides to pdf
pdflatex "$LATEXFILE"
pdflatex "$LATEXFILE"
pdflatex "$LATEXFILE"
