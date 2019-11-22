# Plotting macros

How to plot the figures from root files produced by the analysis done with TkAlTools:

1. Edit the configuration part in jetHtPlotter.C
  - Choose which histograms you want to draw
  - Choose how many IOV:s are plotted in the same figure for profiles
  - Choose if you want to save the figures or not
  - Choose if you want to make an IOV list for the prepareSlides.sh script (should be true if you do not have the list already)

2. Run jetHtPlotter.C. If many histograms and figure saving are selected, I suggest to run in batch mode:
  ```
  root -l -b -q 'jetHtPlotter.C("inputFileName.root")'
  ```

You can compare results from different files by drawing the results to the same figure. For this you need to give more than one file as an argument to the macro. Up to four files at a time can be compared in this manner:
  ```
  root -l -b -q 'jetHtPlotter.C("inputFile1.root", "inputFile2.root", "inputFile3.root", "inputFile4.root")'
  ```

When comparing several files, you can specify the comment put into the legend of the figures for each file using the variable legendComment.

3. To easily see the plots that are produced, compile them into single pdf file using prepareSlides.sh script:
  ```
  ./prepareSlides.sh iovListForSlides.txt jetHt_plotCollection.tex
  ```

4. Examine the results in the produced pdf file
