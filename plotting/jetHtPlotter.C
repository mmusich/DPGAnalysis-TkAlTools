// Include a drawing helper class
#include "JDrawer.h"

/*
 * Macro for plotting figures for the study of jet HT sample
 */
void jetHtPlotter(TString inputFileName = "jetHtAnalysis_partMissing.root"){

  // ======================================================
  // ================== Configuration =====================
  // ======================================================
  
  enum enumHistogramType{kDz, kDzError, kDxy, kDxyError, knHistogramTypes};
  TString histogramName[knHistogramTypes] = {"dz","dzerr","dxy","dxyerr"};
  enum enumProfileType{kDzErrorVsPt, kDzErrorVsPhi, kDxyErrorVsPt, kDxyErrorVsPhi, knProfileTypes};
  TString profileName[knProfileTypes] = {"dzErrVsPt","dzErrVsPhi","dxyErrVsPt","dxyErrVsPhi"};
  TString profileXaxis[knProfileTypes] = {"p_{T}","#phi","p_{T}","#phi"};
  TString profileYaxis[knProfileTypes] = {"d_{z}","d_{z}","d_{xy}","d_{xy}"};
  bool drawHistogram[knHistogramTypes];
  bool drawProfile[knProfileTypes];
  
  bool drawTrackQA = false;             // Draw track and vertex QA figures
  drawHistogram[kDz] = false;           // Draw the dz histograms
  drawHistogram[kDzError] = false;      // Draw the dz error histograms
  drawProfile[kDzErrorVsPt] = false;    // Draw mean dz error as a function of pT
  drawProfile[kDzErrorVsPhi] = false;   // Draw mean dz error as a function of phi
  drawHistogram[kDxy] = false;          // Draw the dxy histograms
  drawHistogram[kDxyError] = false;     // Draw the dxy error histograms
  drawProfile[kDxyErrorVsPt] = true;   // Draw the dxy error as a function of pT
  drawProfile[kDxyErrorVsPhi] = false;  // Draw the dxy error as a function of phi
  
  int colors[] = {kMagenta,kCyan,kGreen+3,kOrange,kViolet+3,kPink-7,kSpring+3,kAzure-7};
  int nIovInOnePlot = 1;  // Define how many iov:s are drawn to the same plot
  
  double profileZoomLow[knProfileTypes] = {0,30,0,30};
  double profileZoomHigh[knProfileTypes] = {80,80,80,80};
  
  bool saveFigures = false;
  
  // Prepare an IOV list that can be used with the slide generation script
  bool makeIovListForSlides = true;
  const char *iovListForSlides = "iovListForSlides.txt";
  
  // Helper variable to ensure that each IOV is added exactly once to the list
  int profileIndexForIovList = 0;
  for(int iProfileType = 0; iProfileType < knProfileTypes; iProfileType++){
    if(drawProfile[iProfileType]){
      profileIndexForIovList = iProfileType;
      break;
    }
  }
  
  // ======================================================
  // ================ Configuration done ==================
  // ======================================================
  
  // Open the input file
  TFile *inputFile = TFile::Open(inputFileName);
  
  // Strings for reading a line from the file
  std::string lineInFile;
  
  // Load the iovList
  std::ifstream iovList("iovList.txt");
  
  // Create a vector for a new iovList
  std::vector<int> iovVector;
  std::vector<TString> iovNames;
  
  // Go through the file line by line. Each line has an iov boundary.
  while(std::getline(iovList, lineInFile))
  {
    // Convert string to integer and put it to vector
    iovVector.push_back(std::stoi(lineInFile));
  }

  // Create names for the different iov:s
  for(std::vector<int>::size_type i = 1; i < iovVector.size(); i++){
    iovNames.push_back(Form("iov%d-%d",iovVector.at(i-1),iovVector.at(i)-1));
  }
  
  // Add the iov integrated histograms after the histograms per IOV
  iovNames.push_back("all");
  iovNames.push_back("central");
  
  // If we are preparing an iov list for slides, make a file for that
  std::ofstream iovFileForSlides;
  if(makeIovListForSlides) iovFileForSlides.open(iovListForSlides);
  
  // Define the histograms that will be read from the file
  const int nIov = iovNames.size();
  TH1D *hVertex;
  TH1D *hTracksPerVertex;
  TH1D *hTrackPt;
  TH1D *hTrackEta;
  TH1D *hTrackPhi;
  TH1D *jetHtHistograms[knHistogramTypes][nIov];
  TProfile *jetHtProfiles[knProfileTypes][nIov];
  
  // Read the histograms from the file
  hVertex = (TH1D*) inputFile->Get("jetHTAnalyzer/all_nvtx");
  hTracksPerVertex = (TH1D*) inputFile->Get("jetHTAnalyzer/h_ntrks");
  hTrackPt = (TH1D*) inputFile->Get("jetHTAnalyzer/h_probePt");
  hTrackEta = (TH1D*) inputFile->Get("jetHTAnalyzer/h_probeEta");
  hTrackPhi = (TH1D*) inputFile->Get("jetHTAnalyzer/h_probePhi");
  for(int iIov = 0; iIov < nIov; iIov++){
    for(int iHistogramType = 0; iHistogramType < knHistogramTypes; iHistogramType++){
      if(drawHistogram[iHistogramType]){
        jetHtHistograms[iHistogramType][iIov] = (TH1D*) inputFile->Get(Form("jetHTAnalyzer/%s_%s",iovNames.at(iIov).Data(),histogramName[iHistogramType].Data()));
      } // if for drawing histogram
    } // histogram type loop
    for(int iProfileType = 0; iProfileType < knProfileTypes; iProfileType++){
      if(drawProfile[iProfileType]){
        jetHtProfiles[iProfileType][iIov] = (TProfile*) inputFile->Get(Form("jetHTAnalyzer/%s_%s",iovNames.at(iIov).Data(),profileName[iProfileType].Data()));
      } // if for drawing profile
    } // profile type loop
  } // iov loop for reading histograms from file
  
  JDrawer *drawer = new JDrawer();
  TLegend *legend;
  bool noIovFound = true;
  
  // Draw track and vertex histograms
  if(drawTrackQA){
    drawer->DrawHistogram(hVertex);
    if(saveFigures) gPad->GetCanvas()->SaveAs("figures/vertex.pdf");
    drawer->DrawHistogram(hTracksPerVertex);
    if(saveFigures) gPad->GetCanvas()->SaveAs("figures/tracksPerVertex.pdf");
    drawer->DrawHistogram(hTrackPt);
    if(saveFigures) gPad->GetCanvas()->SaveAs("figures/trackPt.pdf");
    drawer->DrawHistogram(hTrackEta);
    if(saveFigures) gPad->GetCanvas()->SaveAs("figures/trackEta.pdf");
    drawer->DrawHistogram(hTrackPhi);
    if(saveFigures) gPad->GetCanvas()->SaveAs("figures/trackPhi.pdf");
  }
  
  // Draw dz and dxy histograms
  for(int iIov= 0; iIov < nIov; iIov++){
    for(int iHistogramType = 0; iHistogramType < knHistogramTypes; iHistogramType++){
      if(drawHistogram[iHistogramType]){
        if(jetHtHistograms[iHistogramType][iIov] != NULL){
          drawer->DrawHistogram(jetHtHistograms[iHistogramType][iIov], histogramName[iHistogramType], "tracks", iovNames.at(iIov).Data());
          
          // Save the figures
          if(saveFigures){
            gPad->GetCanvas()->SaveAs(Form("figures/%s_%s.pdf", histogramName[iHistogramType].Data(), iovNames.at(iIov).Data()));
          }
          
        } else {
          cout << "No histogram found for: " << Form("%s_%s",iovNames.at(iIov).Data(),histogramName[iHistogramType].Data()) << endl;
        }
      } // if for drawing histogram
    } // histogram type loop
  }
  
  // Draw dz and dxy profiles
  for(int iIov= 0; iIov < nIov-2; iIov = iIov + nIovInOnePlot){
    for(int iProfileType = 0; iProfileType < knProfileTypes; iProfileType++){
      if(drawProfile[iProfileType]){
        
        noIovFound = true;
        
        // Set up the IOV:s to be drawn to the current ploe
        for(int iSamePlot = 0; iSamePlot < nIovInOnePlot; iSamePlot++){
          if(iIov + iSamePlot >= nIov - 2) break; // Do not draw again all or central references
          if(jetHtProfiles[iProfileType][iIov+iSamePlot] != NULL){
            jetHtProfiles[iProfileType][iIov+iSamePlot]->SetLineColor(colors[iSamePlot]);
            jetHtProfiles[iProfileType][iIov+iSamePlot]->SetLineWidth(2);
            noIovFound = false;
          } else {
            cout << "No histogram found for: " << Form("%s_%s",iovNames.at(iIov).Data(),profileName[iProfileType].Data()) << endl;
          }
        }
        
        if(noIovFound) continue;
        
        // First, draw the reference over all runs to the plot
        jetHtProfiles[iProfileType][nIov-2]->SetLineColor(kBlue);
        jetHtProfiles[iProfileType][nIov-2]->SetLineWidth(2);
        jetHtProfiles[iProfileType][nIov-2]->GetYaxis()->SetRangeUser(profileZoomLow[iProfileType],profileZoomHigh[iProfileType]);
        drawer->DrawHistogram(jetHtProfiles[iProfileType][nIov-2], profileXaxis[iProfileType], Form("#LT#sigma(%s)#GT",profileYaxis[iProfileType].Data()));
        
        // Add a reference to all runs in central eta range
        jetHtProfiles[iProfileType][nIov-1]->SetLineColor(kRed);
        jetHtProfiles[iProfileType][nIov-1]->SetLineWidth(2);
        jetHtProfiles[iProfileType][nIov-1]->Draw("same");
        
        // Define a new legend for the plot
        legend = new TLegend(0.5,0.75-0.05*nIovInOnePlot,0.9,0.9);
        legend->SetFillStyle(0);legend->SetBorderSize(0);legend->SetTextSize(0.05);legend->SetTextFont(62);
        legend->AddEntry(jetHtProfiles[iProfileType][nIov-2],"All","l");
        legend->AddEntry(jetHtProfiles[iProfileType][nIov-1],"Central","l");
        
        // Draw defined number of different IOVs to the plot
        for(int iSamePlot = 0; iSamePlot < nIovInOnePlot; iSamePlot++){
          if(iIov + iSamePlot >= nIov - 2) break; // Do not draw again all or central references
          if(jetHtProfiles[iProfileType][iIov+iSamePlot] != NULL){
            jetHtProfiles[iProfileType][iIov+iSamePlot]->Draw("same");
            legend->AddEntry(jetHtProfiles[iProfileType][iIov+iSamePlot],iovNames.at(iIov+iSamePlot),"pl");
          }
        }
        
        legend->Draw();
        
        // Save the figures
        if(saveFigures){
          gPad->GetCanvas()->SaveAs(Form("figures/%s_iov%d-%d.pdf", profileName[iProfileType].Data(), iovVector.at(iIov),iovVector.at(std::min(iIov+nIovInOnePlot,nIov-2))-1));
        }
        
        // Add the current IOV to the IOV list to be used with the slide generation script
        if(makeIovListForSlides && (iProfileType == profileIndexForIovList)){
          iovFileForSlides << Form("%d-%d",iovVector.at(iIov),iovVector.at(std::min(iIov+nIovInOnePlot,nIov-2))-1) << "\n";
        }
        
      } // if for drawing profile
    } // profile type loop
  } // iov loop for drawing
  
  // Close the output file
  if(makeIovListForSlides) iovFileForSlides.close();
  
}
