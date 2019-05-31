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

3. To easily see the plots that are produced, compile them into single pdf file using prepareSlides.sh script:
  ```
  ./prepareSlides.sh iovListForSlides.txt jetHt_plotCollection.tex
  ```

4. Examine the results in the produced pdf file
