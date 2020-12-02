// Include a drawing helper class
#include "JDrawer.h"

/*
 *  Draw a histogram to canvas
 *
 *  Arguments:
 *    TH1D *histogram[2] = Input histogram and comparison histogram
 *    const char *saveName = Name given for saved figures
 *    bool saveFigures = True: Save figures to file, False: Do not save figures
 *    TString comment[2] = Text written to legend
 *    int legendPosition = Position index of legend: 0 = Right top, 1 = Middle bottom
 *    bool normalize = Normalize the distributions to one so that shapes can be compared
 *    bool logScale = Use logarithmic scale for y-axis
 */
void drawSingleHistogram(TH1D *histogram[4], const char *saveName, bool saveFigures, TString comment[4], int legendPosition, bool normalize, bool logScale){
  JDrawer *drawer = new JDrawer();
  drawer->SetLogY(logScale);
  double legendX1 = 0.6; double legendY1 = 0.75; double legendX2 = 0.9; double legendY2 = 0.9;
  if(legendPosition == 1){
    legendX1 = 0.35; legendY1 = 0.2; legendX2 = 0.65; legendY2 = 0.35;
  }
  TLegend *legend = new TLegend(legendX1,legendY1,legendX2,legendY2);
  legend->SetFillStyle(0);legend->SetBorderSize(0);legend->SetTextSize(0.05);legend->SetTextFont(62);
  histogram[0]->SetLineColor(kBlack);
  if(normalize) histogram[0]->Scale(1.0/histogram[0]->Integral());
  legend->AddEntry(histogram[0],comment[0],"l");
  drawer->DrawHistogram(histogram[0]);
  int lineColors[] = {kRed, kBlue, kMagenta};
  for(int i = 1; i < 4; i++){
    if(histogram[i]){
      histogram[i]->SetLineColor(lineColors[i-1]);
      if(normalize) histogram[i]->Scale(1.0/histogram[i]->Integral());
      histogram[i]->Draw("Same");
      legend->AddEntry(histogram[i],comment[i],"l");
    }
  }
  legend->Draw();
  if(saveFigures) gPad->GetCanvas()->SaveAs(Form("figures/%s.pdf",saveName));
}

/*
 *  Construct vectors of ptHet files and the ptHat value in each of those files
 *
 *  Arguments:
 *   const char* inputFile = File containing the list of ptHat separated files and ptHat bin in each file
 *
 *  return:
 *   Tuple containing list of runs, luminosities, and histogram names within the validation files
 */
std::tuple<std::vector<std::string>, std::vector<int>> getPtHatFilesAndValues(const char* inputFile){
  
  // Create vectors for ptHat files and values
  std::vector<std::string> ptHatFileList;
  std::vector<int> ptHatList;
  
  // Helper variables to read the file
  std::string lineInFile;
  
  // Open the input file for reading
  std::ifstream ptHatFile(inputFile);
  
  // Go through the file line by line. Each line has one file and information about the ptHat in the file.
  while(std::getline(ptHatFile, lineInFile))
  {
    
    auto stringStream = std::istringstream{lineInFile};
    auto wordString = std::string{};
    
    // Find the file name and ptHat in that file
    stringStream >> wordString;
    ptHatFileList.push_back(wordString);
    stringStream >> wordString;
    ptHatList.push_back(std::stoi(wordString));
  }
  
  // After all the vectors are filled, return them
  return std::make_tuple(ptHatFileList, ptHatList);
  
}

/*
 * Get a selected histogram combining different pThat bins
 */
TH1* getPtHatCombinedHistogram(std::vector<std::string> ptHatFiles, std::vector<int> ptHatValues, const char* histogramName){
  
  // Weight for bins:       30to50     50to80      80to120    120to170    170to300    300to470    470to600
  double ptHatWeights[] = {138800000, 19110000,    2735000,    466200,     117200,      7763,      641.0,
  //                       600to800   800to1000  1000to1400  1400to1800  1800to2400  2400to3200  3200toInf
                            185.7,      32.02,      9.375 ,    0.8384,     0.1133,    0.006746,  0.0001623};
  const int nPtHat = 14;
  int ptHatBoundaries[] = {30, 50, 80, 120, 170, 300, 470, 600, 800, 1000, 1400, 1800, 2400, 3200};
  
  TFile *openFile = TFile::Open(ptHatFiles.at(0).data());
  TH1* combinedHistogram = (TH1*) openFile->Get(histogramName)->Clone(Form("%sClone",histogramName));
  TH1* currentHistogram;
  combinedHistogram->Reset("ICES");
  int ptHatIndex = -1;
  
  for(int iFile = 0; iFile < ptHatFiles.size(); iFile++){
    
    ptHatIndex = -1;
    for(int iPtHat = 0; iPtHat < nPtHat; iPtHat++){
      if(ptHatValues.at(iFile) == ptHatBoundaries[iPtHat]){
        ptHatIndex = iPtHat;
        break;
      }
    }
    
    if(ptHatIndex < 0){
      cout << "Could not find pT hat boundary " << ptHatValues.at(iFile) << " for file " << ptHatFiles.at(iFile) << endl;
      cout << "Please check your input! It needs to be in the form <fileName> <ptHatBoundary>" << endl;
      return NULL;
    }
    
    openFile = TFile::Open(ptHatFiles.at(iFile).data());
    currentHistogram = (TH1*) openFile->Get(histogramName);
    combinedHistogram->Add(currentHistogram,ptHatWeights[ptHatIndex]);
    
  }
  
  return combinedHistogram;
  
}

/*
 *  Construct vectors of runs, luminosities, and histogram names within the validation files from an input file
 *  containing a list of runs and luminosities attached to each one
 *
 *  Arguments:
 *   const char* inputFile = File containing the run and luminosity lists
 *
 *  return:
 *   Tuple containing list of runs, luminosities, and histogram names within the validation files
 */
std::tuple<std::vector<int>, std::vector<double>, std::vector<TString>> getRunAndLumiLists(const char* inputFile){
  
  // Create vectors for each list
  std::vector<int> iovVector;
  std::vector<double> lumiPerIov;
  std::vector<TString> iovNames;
  
  // Helper variables to read the file
  std::string lineInFile;
  int thisIov;
  double thisLumi;
  
  // Load the iovList
  std::ifstream iovList(inputFile);
  
  // Go through the file line by line. Each line has an IOV boundary and luminosity for this IOV.
  while(std::getline(iovList, lineInFile))
  {
    
    // Read the iov and luminosity from the file
    std::istringstream lineStream(lineInFile);
    lineStream >> thisIov;
    lineStream >> thisLumi;
    
    // Push the extracted numbers to vectors
    iovVector.push_back(thisIov);
    lumiPerIov.push_back(thisLumi);
  }

  // Create names for the different IOV:s
  for(std::vector<int>::size_type i = 1; i < iovVector.size(); i++){
    iovNames.push_back(Form("iov%d-%d",iovVector.at(i-1),iovVector.at(i)-1));
  }
  
  // Add the iov integrated histograms after the histograms per IOV
  iovNames.push_back("all");
  iovNames.push_back("central");
  
  // After all the vectors are filled, return them
  return std::make_tuple(iovVector, lumiPerIov, iovNames);
  
}

/*
 *  Scale the x-axis of a given graph by integrated luminosity. The error on x-axis represents the luminosity of each run.
 *
 *  Arguments:
 *   TGraphErrors *runGraph = Graph containing dxy or dz error trends as a function of run index
 *   std::vector<double> lumiPerIov = Vector showing luminosities for each run. Indices must match with the graph
 *   bool skipMissingRuns = If there is no data for a run in the runlist, do not assign luminosity for it
 *
 *  Return: std::vector<double> New luminosity list where skipped runs are set to zero
 *
 */
std::vector<double> scaleGraphByLuminosity(TGraphErrors *runGraph, std::vector<double> lumiPerIov, bool skipMissingRuns) {
  
  // Read the number of runs from the graph by run number
  int nRuns = runGraph->GetN();
  
  // Helper variables
  std::vector<double> xAxisValues, yAxisValues, xAxisErrors, yAxisErrors;

  int iRun = 0;
  int offset = 0;
  double lumiFactor = 1000;  // Scale factor value to have luminosity expressed in fb^-1
  
  double runIndex, yValue;
  double xValue = 0;
  double epsilon = 1e-5;
  
  std::vector<double> lumiPerIovWithSkips;
  
  // Loop over all runs, remove zeros and for runs with content, replace x-axis index by luminosity
  while (iRun < nRuns) {
    runGraph->GetPoint(iRun, runIndex, yValue);

    if (lumiPerIov.at(iRun+offset) == 0 || (yValue < epsilon && skipMissingRuns)) {
      nRuns--;
      runGraph->RemovePoint(iRun);
      offset++;
      
      // Fill vector where lumi for skipped runs is set to zero
      lumiPerIovWithSkips.push_back(0);
    } else {
      
      xValue += lumiPerIov.at(iRun+offset) / lumiFactor;
      xAxisValues.push_back(xValue - (lumiPerIov.at(iRun+offset) / (lumiFactor * 2)));
      xAxisErrors.push_back(lumiPerIov.at(iRun+offset) / (lumiFactor * 2));
      yAxisValues.push_back(yValue);
      yAxisErrors.push_back(runGraph->GetErrorY(iRun));
      
      // Fill vector where lumi for skipped runs is set to zero
      lumiPerIovWithSkips.push_back(lumiPerIov.at(iRun+offset));
      
      iRun++;
    }
  } // Loop over all runs in original histogram
  
  // Delete remaining old content and replace it with new one calculated from luminosities
  runGraph->GetHistogram()->Delete();
  runGraph->SetHistogram(nullptr);
  for (size_t iRun = 0; iRun < nRuns; iRun++) {
    runGraph->SetPoint(iRun, xAxisValues.at(iRun), yAxisValues.at(iRun));
    runGraph->SetPointError(iRun, xAxisErrors.at(iRun), yAxisErrors.at(iRun));
  }
  
  return lumiPerIovWithSkips;
}

/*
 * Get the total luminosity upto a given run
 *
 *  std::vector<double> lumiPerIov = Vector containing luminosity information
 *  std::vector<int> iovVector = Vector containing run information
 *  in runNumber = Run upto which the luminosity is calculated
 */
double getLuminosityBeforeRun(std::vector<double> lumiPerIov, std::vector<int> iovVector, int runNumber) {

  double lumiFactor = 1000;  // Scale factor value to have luminosity expressed in fb^-1
  
  int nRuns = lumiPerIov.size();
  double luminosityBefore = 0;
  
  for(int iRun = 0; iRun < nRuns; iRun++){
    
    if(runNumber <= iovVector.at(iRun)) return luminosityBefore;
    
    luminosityBefore += lumiPerIov.at(iRun) / lumiFactor;
    
  }
  
  return luminosityBefore;
  
}

/*
 * Macro for plotting figures for the study of jet HT sample
 */
void jetHtPlotter(TString inputFileName = "data/jetHtAnalysis_partMissing.root", TString comparisonFileName = "", TString comparisonFileName2 = "", TString comparisonFileName3 = ""){

  // ======================================================
  // ================== Configuration =====================
  // ======================================================
  
  enum enumHistogramType{kDz, kDzError, kDxy, kDxyError, knHistogramTypes};
  TString histogramName[knHistogramTypes] = {"dz","dzerr","dxy","dxyerr"};
  TString histogramXaxis[knHistogramTypes] = {"d_{z} (#mum)","#sigma(d_{z}) (#mum)","d_{xy} (#mum)","#sigma(d_{xy}) (#mum)"};
  enum enumProfileType{kDzErrorVsPt, kDzErrorVsPhi, kDzErrorVsEta, kDxyErrorVsPt, kDxyErrorVsPhi, kDxyErrorVsEta, kDzErrorVsPtWide, kDxyErrorVsPtWide, knProfileTypes};
  enum enumTrendType{kDzErrorTrend, kDxyErrorTrend, knTrendTypes};
  TString profileName[knProfileTypes] = {"dzErrVsPt", "dzErrVsPhi", "dzErrVsEta", "dxyErrVsPt", "dxyErrVsPhi", "dxyErrVsEta", "dzErrVsPtWide", "dxyErrVsPtWide"};
  TString profileXaxis[knProfileTypes] = {"p_{T} (GeV)","#varphi","#eta","p_{T} (GeV)","#varphi","#eta", "p_{T} bin", "p_{T} bin"};
  TString profileYaxis[knProfileTypes] = {"d_{z}","d_{z}","d_{z}","d_{xy}","d_{xy}","d_{xy}","d_{z}","d_{xy}"};
  TString trendName[] = {"dzErr","dxyErr"};
  bool drawHistogram[knHistogramTypes];
  bool drawProfile[knProfileTypes];
  bool drawTrend[knTrendTypes];
  
  bool drawTrackQA = false;             // Draw track and vertex QA figures
  drawHistogram[kDz] = false;           // Draw the dz histograms
  drawHistogram[kDzError] = false;      // Draw the dz error histograms
  drawProfile[kDzErrorVsPt] = true;    // Draw mean dz error as a function of pT
  drawProfile[kDzErrorVsPhi] = true;   // Draw mean dz error as a function of phi
  drawProfile[kDzErrorVsEta] = true;   // Draw mean dz error as a function of eta
  drawProfile[kDzErrorVsPtWide] = false;   // Draw mean dz error in wide pT bins
  drawHistogram[kDxy] = false;          // Draw the dxy histograms
  drawHistogram[kDxyError] = false;     // Draw the dxy error histograms
  drawProfile[kDxyErrorVsPt] = true;   // Draw the dxy error as a function of pT
  drawProfile[kDxyErrorVsPhi] = true;  // Draw the dxy error as a function of phi
  drawProfile[kDxyErrorVsEta] = true;  // Draw the dxy error as a function of eta
  drawProfile[kDxyErrorVsPtWide] = false;   // Draw mean dxy error in wide pT bins
  drawTrend[kDzErrorTrend] = true;     // Draw the trend plots for dz errors
  drawTrend[kDxyErrorTrend] = true;    // Draw the trend plots for dxy errors
  
  bool drawProfilesForEachIOV = false;  // True = Draw profile plots for every IOV. False = only draw average over all runs
  bool useLuminosityForTrends = true;  // True = Draw trends as a function of luminosity. False = Draw trends as a function of run index
  bool skipRunsWithNoData = false;      // True = Do not draw empty space if run in list is missing data. False = Draw empty space
  
  int colors[] = {kRed,kGreen+3,kMagenta,kCyan,kViolet+3,kOrange,kPink-7,kSpring+3,kAzure-7};
  int nIovInOnePlot = 1;  // Define how many iov:s are drawn to the same plot
  
  double profileZoomLow[knProfileTypes] = {28,45,30,7,40,20,25,20};
  double profileZoomHigh[knProfileTypes] = {60,80,95,40,70,90,90,80};
  double trendZoomLow[knTrendTypes] = {20,10};
  double trendZoomHigh[knTrendTypes] = {95,90};
  
  const int nWidePtBins = 6;
  int widePtBinBorders[nWidePtBins] = {3,5,10,20,50,100};
  
  bool normalizeQAplots = true;
  bool saveFigures = false;
  const char *saveComment = "_dataMCComparison2017_lowPtHat";
  
  int compareFiles = 1;
  if(!comparisonFileName.EqualTo("")) compareFiles++;
  if(!comparisonFileName2.EqualTo("")) compareFiles++;
  if(!comparisonFileName3.EqualTo("")) compareFiles++;
  
  // Prepare an IOV list that can be used with the slide generation script
  bool makeIovListForSlides = false;
  const char *iovListForSlides = "iovListForSlides.txt";
  
  // Helper variable to ensure that each IOV is added exactly once to the list
  int profileIndexForIovList = 0;
  for(int iProfileType = 0; iProfileType < knProfileTypes; iProfileType++){
    if(drawProfile[iProfileType]){
      profileIndexForIovList = iProfileType;
      break;
    }
  }
  
  // Text written to the legend for each file
  TString legendComment[4];
  legendComment[0] = "Prompt";
  legendComment[1] = "ReReco";
  legendComment[2] = "UltraLegacy";
  legendComment[3] = "120 < #hat{p}_{T} < 170 GeV";
  
  
  const bool displayIOVinComment = false; // False: The comment is fully given by legend comment. True: IOV/all/central added to comment
  
  TString plotTitle = " ";  // Title given to the plot
  
  // Year boundary runs
  bool drawYearLines = true;         // Draw lines between data taking years
  const int firstRun2016 = 266150;   // First run of 2016
  const int firstRun2017 = 290543;   // First run of 2017
  const int firstRun2018 = 314881;   // First run of 2018
  
  // ======================================================
  // ================ Configuration done ==================
  // ======================================================
  
  // ===============================================================
  //   Read different ptHat files for combining those with weights
  // ===============================================================
  
//  // Name of the file containing the ptHat file names
//  const char *ptHatFileName = "ptHatFiles.txt";
//
//  // List for all the different ptHat files to be combined
//  std::vector<std::string> ptHatFileList;
//  std::vector<int> ptHatList;
//
//  std::tie(ptHatFileList, ptHatList) = getPtHatFilesAndValues(ptHatFileName);
  
  // ===============================================
  //        Read the run and luminosity list
  // ===============================================
  
  // Luminosity per run file
  const char* iovAndLumiFile = "lumiPerRun_Run2.txt";
  
  // Create a vector for a new iovList
  std::vector<int> iovVector;
  std::vector<double> lumiPerIov;
  std::vector<double> lumiPerIovWithSkips;
  std::vector<TString> iovNames;
  
  std::tie(iovVector, lumiPerIov, iovNames) = getRunAndLumiLists(iovAndLumiFile);
  
  // ===============================================
  //                IOV list for slides
  // ===============================================
  
  // If we are preparing an iov list for slides, make a file for that
  std::ofstream iovFileForSlides;
  if(makeIovListForSlides) iovFileForSlides.open(iovListForSlides);
  
  // ===============================================
  //   Create histograms and read them from a file
  // ===============================================
  
  // Open the input files
  TFile *inputFile[4];
  inputFile[0] = TFile::Open(inputFileName);
  if(compareFiles > 1) inputFile[1] = TFile::Open(comparisonFileName);
  if(compareFiles > 2) inputFile[2] = TFile::Open(comparisonFileName2);
  if(compareFiles > 3) inputFile[3] = TFile::Open(comparisonFileName3);
  
  // Define the histograms that will be read from the file
  const int nIov = iovNames.size();
  TH1D *hVertex[4];
  TH1D *hTracksPerVertex[4];
  TH1D *hTrackPt[4];
  TH1D *hTrackEta[4];
  TH1D *hTrackPhi[4];
  TH1D *jetHtHistograms[4][knHistogramTypes][nIov];
  TProfile *jetHtProfiles[4][knProfileTypes][nIov];
  TGraphErrors *gBigTrend[4][knTrendTypes][nWidePtBins];
  int legendSplitter = 0;
  
  // Initialize everything to NULL
  for(int iFile = 0; iFile < 4; iFile++){
    hVertex[iFile] = NULL;
    hTracksPerVertex[iFile] = NULL;
    hTrackPt[iFile] = NULL;
    hTrackEta[iFile] = NULL;
    hTrackPhi[iFile] = NULL;
    for(int iIov = 0; iIov < nIov; iIov++){
      for(int iHistogramType = 0; iHistogramType < knHistogramTypes; iHistogramType++){
        jetHtHistograms[iFile][iHistogramType][iIov] = NULL;
      } // histogram type loop
      for(int iProfileType = 0; iProfileType < knProfileTypes; iProfileType++){
        jetHtProfiles[iFile][iProfileType][iIov] = NULL;
      } // profile type loop
    } // iov loop for reading histograms from file
    for(int iTrend = 0; iTrend < knTrendTypes; iTrend++){
      for(int iWidePt = 0; iWidePt < nWidePtBins; iWidePt++){
        gBigTrend[iFile][iTrend][iWidePt] = NULL;
      } // Trend loop
    } // Wide pT bin loop
  } // file loop
  
  // Read the histograms from the file
  for(int iFile = 0; iFile < compareFiles; iFile++){
    hVertex[iFile] = (TH1D*) inputFile[iFile]->Get("jetHTAnalyzer/all_nvtx");
    hTracksPerVertex[iFile] = (TH1D*) inputFile[iFile]->Get("jetHTAnalyzer/h_ntrks");
    hTrackPt[iFile] = (TH1D*) inputFile[iFile]->Get("jetHTAnalyzer/h_probePt");
    hTrackEta[iFile] = (TH1D*) inputFile[iFile]->Get("jetHTAnalyzer/h_probeEta");
    hTrackPhi[iFile] = (TH1D*) inputFile[iFile]->Get("jetHTAnalyzer/h_probePhi");
    for(int iIov = 0; iIov < nIov; iIov++){
      for(int iHistogramType = 0; iHistogramType < knHistogramTypes; iHistogramType++){
        if(drawHistogram[iHistogramType]){
          jetHtHistograms[iFile][iHistogramType][iIov] = (TH1D*) inputFile[iFile]->Get(Form("jetHTAnalyzer/%s_%s",iovNames.at(iIov).Data(),histogramName[iHistogramType].Data()));
        } // if for drawing histogram
      } // histogram type loop
      for(int iProfileType = 0; iProfileType < knProfileTypes; iProfileType++){
        if(drawProfile[iProfileType] || (drawTrend[kDzErrorTrend] && iProfileType == kDzErrorVsPtWide) || (drawTrend[kDxyErrorTrend] && iProfileType == kDxyErrorVsPtWide)){
          jetHtProfiles[iFile][iProfileType][iIov] = (TProfile*) inputFile[iFile]->Get(Form("jetHTAnalyzer/%s_%s",iovNames.at(iIov).Data(),profileName[iProfileType].Data()));
        } // if for drawing profile
      } // profile type loop
    } // iov loop for reading histograms from file
  } // Loop over files
  
  // Collect the information for the trend graphs
  // TODO: Integrated luminosity for x-axis. The width of the bin should correspond to the luminosity recorded in that run
  const int nRuns = iovVector.size()-1;
  double yValueDz[nRuns];
  double yErrorDz[nRuns];
  double yValueDxy[nRuns];
  double yErrorDxy[nRuns];
  double xValue[nRuns];
  double xError[nRuns];
  TString commentEntry = "";
  if(drawTrend[kDzErrorTrend] || drawTrend[kDxyErrorTrend]){
    for(int iFile = 0; iFile < compareFiles; iFile++){
      for(int iWidePt = 0; iWidePt < nWidePtBins; iWidePt++){
        for(int iRun = 0; iRun < nRuns; iRun++){
          xValue[iRun] = iRun;
          xError[iRun] = 0;
          if(jetHtProfiles[iFile][kDzErrorVsPtWide][iRun] == NULL){
            yValueDz[iRun] = 0;
            yErrorDz[iRun] = 0;
          } else {
            yValueDz[iRun] = jetHtProfiles[iFile][kDzErrorVsPtWide][iRun]->GetBinContent(iWidePt+1);
            yErrorDz[iRun] = jetHtProfiles[iFile][kDzErrorVsPtWide][iRun]->GetBinError(iWidePt+1);
          }
          if(jetHtProfiles[iFile][kDxyErrorVsPtWide][iRun] == NULL){
            yValueDxy[iRun] = 0;
            yErrorDxy[iRun] = 0;
          } else {
            yValueDxy[iRun] = jetHtProfiles[iFile][kDxyErrorVsPtWide][iRun]->GetBinContent(iWidePt+1);
            yErrorDxy[iRun] = jetHtProfiles[iFile][kDxyErrorVsPtWide][iRun]->GetBinError(iWidePt+1);
          }
        } // Run loop
        
        gBigTrend[iFile][kDzErrorTrend][iWidePt] = new TGraphErrors(nRuns, xValue, yValueDz, xError, yErrorDz);
        gBigTrend[iFile][kDxyErrorTrend][iWidePt] = new TGraphErrors(nRuns, xValue, yValueDxy, xError, yErrorDxy);
        
        // Change x-axis to processed luminosity
        if(useLuminosityForTrends){
          lumiPerIovWithSkips = scaleGraphByLuminosity(gBigTrend[iFile][kDzErrorTrend][iWidePt], lumiPerIov, skipRunsWithNoData);
          scaleGraphByLuminosity(gBigTrend[iFile][kDxyErrorTrend][iWidePt], lumiPerIov, skipRunsWithNoData);
        }
        
        
      } // Wide pT bin loop
    } // File loop
  } // If for drawing trends
  
  // ===============================================
  //                  Draw the plots
  // ===============================================
  
  JDrawer *drawer = new JDrawer();
  TLegend *legend[2];
  bool noIovFound = true;
  
  // Draw track and vertex histograms
  if(drawTrackQA){
    drawSingleHistogram(hVertex,Form("vertex%s",saveComment),saveFigures,legendComment,0,normalizeQAplots,false);
    drawSingleHistogram(hTracksPerVertex,Form("tracksPerVertex%s",saveComment),saveFigures,legendComment,0,normalizeQAplots,false);
    drawSingleHistogram(hTrackPt,Form("trackPt%s",saveComment),saveFigures,legendComment,0,normalizeQAplots,true);
    drawSingleHistogram(hTrackEta,Form("trackEta%s",saveComment),saveFigures,legendComment,1,normalizeQAplots,false);
    drawSingleHistogram(hTrackPhi,Form("trackPhi%s",saveComment),saveFigures,legendComment,1,normalizeQAplots,false);
  }
  
  // Draw dz and dxy histograms
  for(int iIov= 0; iIov < nIov; iIov++){
    for(int iHistogramType = 0; iHistogramType < knHistogramTypes; iHistogramType++){
      if(drawHistogram[iHistogramType]){
        
        legend[0] = new TLegend(0.7,0.85-0.05*compareFiles,0.95,0.9);
        legend[0]->SetFillStyle(0);legend[0]->SetBorderSize(0);
        legend[0]->SetTextSize(0.05);legend[0]->SetTextFont(62);
        
        if(jetHtHistograms[0][iHistogramType][iIov] != NULL){
          drawer->DrawHistogram(jetHtHistograms[0][iHistogramType][iIov], histogramXaxis[iHistogramType], "tracks", iovNames.at(iIov).Data());
          legend[0]->AddEntry(jetHtHistograms[0][iHistogramType][iIov],legendComment[0],"l");
          
          for(int iFile = 1; iFile < compareFiles; iFile++){
            if(jetHtHistograms[iFile][iHistogramType][iIov] != NULL){
              jetHtHistograms[iFile][iHistogramType][iIov]->SetLineColor(colors[iFile-1]);
              jetHtHistograms[iFile][iHistogramType][iIov]->Draw("same");
              legend[0]->AddEntry(jetHtHistograms[iFile][iHistogramType][iIov],legendComment[iFile],"l");
            }
          }
          
          legend[0]->Draw();
          
          // Save the figures
          if(saveFigures){
            gPad->GetCanvas()->SaveAs(Form("figures/%s%s_%s.pdf", histogramName[iHistogramType].Data(), saveComment, iovNames.at(iIov).Data()));
          }
          
        } else {
          cout << "No histogram found for: " << Form("%s_%s",iovNames.at(iIov).Data(),histogramName[iHistogramType].Data()) << endl;
        }
      } // if for drawing histogram
    } // histogram type loop
  }
  
  // Draw dz and dxy profiles
  for(int iProfileType = 0; iProfileType < knProfileTypes; iProfileType++){
    if(drawProfile[iProfileType]){
      
      // Set the style for IOV integrated histograms
      jetHtProfiles[0][iProfileType][nIov-2]->SetLineColor(kBlue);
      jetHtProfiles[0][iProfileType][nIov-2]->SetLineWidth(2);
      jetHtProfiles[0][iProfileType][nIov-2]->GetYaxis()->SetRangeUser(profileZoomLow[iProfileType], profileZoomHigh[iProfileType]);
      
      for(int iFile = 1; iFile < compareFiles; iFile++){
        jetHtProfiles[iFile][iProfileType][nIov-2]->SetLineColor(colors[iFile-1]);
        if(compareFiles == 2) jetHtProfiles[iFile][iProfileType][nIov-2]->SetLineColor(kCyan);  // Preserve coloring scheme for 2 file comparison
        jetHtProfiles[iFile][iProfileType][nIov-2]->SetLineWidth(2);
      }
      
      // NOTE: IOV drawing only works for one or two files! Using more files will not give good results!!!
      if(drawProfilesForEachIOV){
        for(int iIov= 0; iIov < nIov-2; iIov = iIov + nIovInOnePlot){
          
          noIovFound = true;
          
          // Set up the IOV:s to be drawn to the current plot
          for(int iSamePlot = 0; iSamePlot < nIovInOnePlot; iSamePlot++){
            if(iIov + iSamePlot >= nIov - 2) break; // Do not draw again all or central references
            if(jetHtProfiles[0][iProfileType][iIov+iSamePlot] != NULL){
              jetHtProfiles[0][iProfileType][iIov+iSamePlot]->SetLineColor(colors[iSamePlot]);
              jetHtProfiles[0][iProfileType][iIov+iSamePlot]->SetLineWidth(2);
              noIovFound = false;
            } else {
              cout << "No histogram found for: " << Form("%s_%s",iovNames.at(iIov).Data(),profileName[iProfileType].Data()) << endl;
            }
            
            if(jetHtProfiles[1][iProfileType][iIov+iSamePlot] != NULL){
              jetHtProfiles[1][iProfileType][iIov+iSamePlot]->SetLineColor(colors[iSamePlot+nIovInOnePlot]);
              jetHtProfiles[1][iProfileType][iIov+iSamePlot]->SetLineWidth(2);
            }
          }
          
          if(noIovFound) continue;
          
          // First, draw the reference over all runs to the plot
          drawer->DrawHistogram(jetHtProfiles[0][iProfileType][nIov-2], profileXaxis[iProfileType], Form("#LT#sigma(%s)#GT (#mum)",profileYaxis[iProfileType].Data()));
          
          // Define a new legend for the plot
          for(int iFile = 0; iFile < compareFiles; iFile++){
            legend[iFile] = new TLegend(0.56-0.37*iFile,0.8-0.05*nIovInOnePlot,0.86-0.37*iFile,0.9);
            legend[iFile]->SetFillStyle(0); legend[iFile]->SetBorderSize(0);
            legend[iFile]->SetTextSize(0.05); legend[iFile]->SetTextFont(62);
          }
          legend[0]->AddEntry(jetHtProfiles[0][iProfileType][nIov-2],Form("All (%s)",legendComment[0].Data()),"l");
          
          if(jetHtProfiles[1][iProfileType][nIov-2] != NULL){
            jetHtProfiles[1][iProfileType][nIov-2]->Draw("same");
            legend[1]->AddEntry(jetHtProfiles[1][iProfileType][nIov-2],Form("All (%s)",legendComment[1].Data()),"l");
          }
          
          // Draw defined number of different IOVs to the plot
          for(int iFile = 0; iFile < compareFiles; iFile++){
            for(int iSamePlot = 0; iSamePlot < nIovInOnePlot; iSamePlot++){
              if(iIov + iSamePlot >= nIov - 2) break; // Do not draw again all or central references
              if(jetHtProfiles[iFile][iProfileType][iIov+iSamePlot] != NULL){
                jetHtProfiles[iFile][iProfileType][iIov+iSamePlot]->Draw("same");
                legend[iFile]->AddEntry(jetHtProfiles[iFile][iProfileType][iIov+iSamePlot],iovNames.at(iIov+iSamePlot),"l");
              }
            }
            legend[iFile]->Draw();
          }
          
          
          
          // Save the figures
          if(saveFigures){
            gPad->GetCanvas()->SaveAs(Form("figures/%s%s_iov%d-%d.pdf", profileName[iProfileType].Data(), saveComment, iovVector.at(iIov),iovVector.at(std::min(iIov+nIovInOnePlot,nIov-2))-1));
          }
          
          // Add the current IOV to the IOV list to be used with the slide generation script
          if(makeIovListForSlides && (iProfileType == profileIndexForIovList)){
            iovFileForSlides << Form("%d-%d",iovVector.at(iIov),iovVector.at(std::min(iIov+nIovInOnePlot,nIov-2))-1) << "\n";
          }
          
        } // iov loop for drawing
      } // if for drawing profiles for each IOV
      
      
      // After all IOV:s, draw summary with all and central curves
      drawer->DrawHistogram(jetHtProfiles[0][iProfileType][nIov-2], profileXaxis[iProfileType], Form("#LT#sigma(%s)#GT (#mum)",profileYaxis[iProfileType].Data()), plotTitle);
      
      // Add a reference to all runs in central eta range, except for plots as a function of eta
      // Only draw central histogram is comparing only 2 files
      if(jetHtProfiles[0][iProfileType][nIov-1] != NULL && compareFiles < 3){
        jetHtProfiles[0][iProfileType][nIov-1]->SetLineColor(kRed);
        jetHtProfiles[0][iProfileType][nIov-1]->SetLineWidth(2);
        jetHtProfiles[0][iProfileType][nIov-1]->Draw("same");
      }
      
      
      for(int iFile = 1; iFile < compareFiles; iFile++){
        
        // Add all and central also from the comparison file
        if(jetHtProfiles[iFile][iProfileType][nIov-2] != NULL){
          jetHtProfiles[iFile][iProfileType][nIov-2]->Draw("same");
          if(jetHtProfiles[iFile][iProfileType][nIov-1] != NULL && compareFiles < 3){ // Only add central if comparing just two files
            jetHtProfiles[iFile][iProfileType][nIov-1]->SetLineColor(kMagenta);
            jetHtProfiles[iFile][iProfileType][nIov-1]->SetLineWidth(2);
            jetHtProfiles[iFile][iProfileType][nIov-1]->Draw("same");
          }
        }
      }
      
      // Define legends for the plots
      legendSplitter = 2;
      if(compareFiles < legendSplitter) legendSplitter = compareFiles;
      for(int iFile = 0; iFile < legendSplitter; iFile++){
        if(legendSplitter < 2){
          legend[iFile] = new TLegend(0.56,0.75,0.86,0.9);
        } else {
          legend[iFile] = new TLegend(0.19+0.37*iFile,0.75,0.49+0.37*iFile,0.9);
        }
        legend[iFile]->SetFillStyle(0); legend[iFile]->SetBorderSize(0);
        legend[iFile]->SetTextSize(0.05); legend[iFile]->SetTextFont(62);
        if(displayIOVinComment){
          commentEntry = Form("All (%s)",legendComment[iFile].Data());
        } else {
          commentEntry = legendComment[iFile];
        }
        legend[iFile]->AddEntry(jetHtProfiles[iFile][iProfileType][nIov-2],commentEntry.Data(),"l");
        if(jetHtProfiles[iFile][iProfileType][nIov-1] != NULL && compareFiles < 3) legend[iFile]->AddEntry(jetHtProfiles[iFile][iProfileType][nIov-1],Form("Central (%s)",legendComment[iFile].Data()),"l");
      }
      
      if(compareFiles > 2){
        for(int iFile = 2; iFile < compareFiles; iFile++){
          if(displayIOVinComment){
            commentEntry = Form("All (%s)",legendComment[iFile].Data());
          } else {
            commentEntry = legendComment[iFile];
          }
          legend[iFile-2]->AddEntry(jetHtProfiles[iFile][iProfileType][nIov-2],commentEntry.Data(),"l");
        }
      }
      
      for(int iFile = 0; iFile < legendSplitter; iFile++){
        legend[iFile]->Draw();
      }
      
      // Save the figures
      if(saveFigures){
        gPad->GetCanvas()->SaveAs(Form("figures/%s%s_allIovs.pdf", profileName[iProfileType].Data(),saveComment));
      }
    } // if for drawing profile
  } // profile type loop
  
  // Close the output file
  if(makeIovListForSlides) iovFileForSlides.close();
  
  // Trend plots
  TLegend *trendLegend;
  drawer->SetCanvasSize(1000,400);
  double trendColors[] = {kBlue, kRed, kGreen+2, kBlack};
  double lumiX;
  TLine *lumiLine2017;
  TLine *lumiLine2018;
  
  TString xTitle = "Run index";
  if(useLuminosityForTrends) xTitle = "Delivered luminosity  (1/fb)";
  
  for(int iTrend = 0; iTrend < knTrendTypes; iTrend++){
    if(!drawTrend[iTrend]) continue;
    for(int iWidePt = 0; iWidePt < nWidePtBins; iWidePt++){
      
      trendLegend = new TLegend(0.65,0.6,0.9,0.9);
      trendLegend->SetFillStyle(0); trendLegend->SetBorderSize(0);
      trendLegend->SetTextSize(0.05); trendLegend->SetTextFont(62);
      trendLegend->SetHeader(Form("%s error trend for p_{T} > %d GeV", profileYaxis[iTrend+6].Data(), widePtBinBorders[iWidePt]));
      
      for(int iFile = 0; iFile < compareFiles; iFile++){
        gBigTrend[iFile][iTrend][iWidePt]->SetMarkerColor(trendColors[iFile]);
        gBigTrend[iFile][iTrend][iWidePt]->SetMarkerStyle(kFullCircle);
        
        if(iFile == 0){
          drawer->DrawGraphCustomAxes(gBigTrend[iFile][iTrend][iWidePt], 0, nRuns, trendZoomLow[iTrend], trendZoomHigh[iTrend], xTitle, Form("#LT #sigma(%s) #GT", profileYaxis[iTrend+6].Data()), " ", "ap");
        } else {
          gBigTrend[iFile][iTrend][iWidePt]->Draw("p,same");
        }
        
        trendLegend->AddEntry(gBigTrend[iFile][iTrend][iWidePt], legendComment[iFile].Data(), "p");
        
      } // File loop
      
      trendLegend->Draw();
      
      // Draw lines for different data taking year
      if(drawYearLines){
        lumiX = getLuminosityBeforeRun(lumiPerIovWithSkips, iovVector, firstRun2017);
        lumiLine2017 = new TLine(lumiX, trendZoomLow[iTrend], lumiX, trendZoomHigh[iTrend]);
        lumiLine2017->Draw();
        
        lumiX = getLuminosityBeforeRun(lumiPerIovWithSkips, iovVector, firstRun2018);
        lumiLine2018 = new TLine(lumiX, trendZoomLow[iTrend], lumiX, trendZoomHigh[iTrend]);
        lumiLine2018->Draw();
      }
      
      // Save the figures
      if(saveFigures){
        gPad->GetCanvas()->SaveAs(Form("figures/%sTrendPtOver%d%s.pdf", trendName[iTrend].Data(), widePtBinBorders[iWidePt], saveComment));
      }
      
    } // Wide pT loop
  } // Trend type loop
  
}
