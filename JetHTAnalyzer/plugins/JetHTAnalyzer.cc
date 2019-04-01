// -*- C++ -*-
//
// Package:    TkAlTools/JetHTAnalyzer
// Class:      JetHTAnalyzer
//
/**\class JetHTAnalyzer JetHTAnalyzer.cc TkAlTools/JetHTAnalyzer/plugins/JetHTAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Marco Musich
//         Created:  Fri, 29 Mar 2019 14:54:59 GMT
//
//


// system include files
#include <algorithm>    // std::sort
#include <memory>
#include <vector>       // std::vector

// CMSSW includes
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "Geometry/Records/interface/GlobalTrackingGeometryRecord.h"
#include "RecoVertex/AdaptiveVertexFit/interface/AdaptiveVertexFitter.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TkAlTools/JetHTAnalyzer/interface/SmartSelectionMonitor.h"

// ROOT includes
#include "TRandom.h"
#include "TTree.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.


using reco::TrackCollection;

class JetHTAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit JetHTAnalyzer(const edm::ParameterSet&);
      ~JetHTAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
      static bool mysorter (reco::Track i, reco::Track j) { return (i.pt () > j.pt()); }

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
  
      edm::InputTag      pvsTag_                        ;
      edm::EDGetTokenT<reco::VertexCollection> pvsToken_;

      edm::InputTag      tracksTag_                        ;
      edm::EDGetTokenT<reco::TrackCollection>  tracksToken_;

      double minVtxNdf_;
      double minVtxWgt_;

      edm::Service<TFileService> outfile_;
      TH1F* h_ntrks ;
      TH1F* h_probePt;
      TH1F* h_probeEta;
      TH1F* h_probePhi;
      TH1F* h_probeDxy;
      TH1F* h_probeDz;
      TH1F* h_probeDxyErr;
      TH1F* h_probeDzErr;   

      SmartSelectionMonitor mon;

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
JetHTAnalyzer::JetHTAnalyzer(const edm::ParameterSet& iConfig) :
  pvsTag_           (iConfig.getParameter<edm::InputTag>("vtxCollection")), 
  pvsToken_         (consumes<reco::VertexCollection>(pvsTag_)), 
  tracksTag_        (iConfig.getParameter<edm::InputTag>("trackCollection")), 
  tracksToken_ (consumes<reco::TrackCollection>(tracksTag_)),
  minVtxNdf_        (iConfig.getUntrackedParameter<double>("minVertexNdf")), 
  minVtxWgt_ (iConfig.getUntrackedParameter<double>("minVertexMeanWeight"))
{
   //now do what ever initialization is needed
}


JetHTAnalyzer::~JetHTAnalyzer()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
JetHTAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  const double cmToum = 10000;

  edm::ESHandle<TransientTrackBuilder>            theB                ;
  edm::ESHandle<GlobalTrackingGeometry>           theTrackingGeometry ;
  iSetup.get<GlobalTrackingGeometryRecord>().get(theTrackingGeometry) ;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder",theB);

  edm::Handle<reco::VertexCollection> vertices; 
  iEvent.getByToken(pvsToken_, vertices);
  const reco::VertexCollection pvtx  = *(vertices.product())  ;    

  edm::Handle<reco::TrackCollection> tracks; 
  iEvent.getByToken(tracksToken_, tracks);

  int counter=0;
  for (reco::VertexCollection::const_iterator pvIt = pvtx.begin(); pvIt!=pvtx.end(); pvIt++){
    reco::Vertex iPV = *pvIt;
    counter++;

    if (iPV.isFake()) continue;
    reco::Vertex::trackRef_iterator trki;

    const math::XYZPoint pos_(iPV.x(),iPV.y(),iPV.z());
    
    // vertex selection as in bs code
    if ( iPV.ndof() < minVtxNdf_ || (iPV.ndof()+3.)/iPV.tracksSize()< 2*minVtxWgt_ )  continue;

    reco::TrackCollection allTracks;
    for (trki  = iPV.tracks_begin(); trki != iPV.tracks_end(); ++trki){
      if (trki->isNonnull()){
        reco::TrackRef trk_now(tracks, (*trki).key());
        allTracks.push_back(*trk_now);
      }
    }
     
    // order with decreasing pt 
    std::sort (allTracks.begin(), allTracks.end(), mysorter);    
    uint ntrks = allTracks.size();
    h_ntrks -> Fill( ntrks );
    
    for (uint tracksIt = 0;  tracksIt < ntrks; tracksIt++){
      auto tk = allTracks.at(tracksIt); 

      double dxyRes  = tk.dxy(pos_)*cmToum;
      double dzRes   = tk.dz(pos_)*cmToum;

      double dxy_err = tk.dxyError()*cmToum;
      double dz_err  = tk.dzError()*cmToum;

      float trackphi = tk.phi();
      float tracketa = tk.eta();
      float trackpt  = tk.pt();

      h_probePt->Fill(trackpt);  
      h_probeEta->Fill(tracketa); 
      h_probePhi->Fill(trackphi); 
      
      h_probeDxy->Fill(dxyRes);   
      h_probeDz->Fill(dzRes);    
      h_probeDxyErr->Fill(dxy_err);
      h_probeDzErr->Fill(dz_err); 

      mon.fillHisto("dxy","all",dxyRes,1.);
      mon.fillHisto("dz","all",dzRes,1.);
      mon.fillHisto("dxyerr","all",dxy_err,1.);
      mon.fillHisto("dzerr","all",dz_err,1.);

      mon.fillProfile("dxyErrVsPt","all",trackpt,dxy_err,1.);
      mon.fillProfile("dzErrVsPt" ,"all",trackpt,dz_err,1.);

      if(std::abs(tracketa)<1.){
	mon.fillHisto("dxy","central",dxyRes,1.);
	mon.fillHisto("dz","central",dzRes,1.);
	mon.fillHisto("dxyerr","central",dxy_err,1.);
	mon.fillHisto("dzerr","central",dz_err,1.);

	mon.fillProfile("dxyErrVsPt","central",trackpt,dxy_err,1.);
	mon.fillProfile("dzErrVsPt" ,"central",trackpt,dz_err,1.);
      }     
      
    }// loop on tracks in vertex
  } // loop on vertices

  mon.fillHisto("nvtx","all",counter,1.);

}


// ------------ method called once each job just before starting event loop  ------------
void
JetHTAnalyzer::beginJob()
{

  h_ntrks    = outfile_->make<TH1F>("h_ntrks" , "n. trks;n. of tracks/vertex;n. vertices", 100, 0, 100 );
  h_probePt  = outfile_->make<TH1F>("h_probePt","p_{T} of probe track;track p_{T} (GeV); tracks",100,0.,500.);   
  h_probeEta = outfile_->make<TH1F>("h_probeEta","#eta of the probe track;track #eta;tracks",54,-2.8,2.8);  
  h_probePhi = outfile_->make<TH1F>("h_probePhi","#phi of probe track;track #phi (rad);tracks",100,-3.15,3.15);  
  
  h_probeDxy    = outfile_->make<TH1F>("h_probeDxy","d_{xy}(PV) of the probe track;track d_{xy}(PV);tracks",200,-100,100 );
  h_probeDz     = outfile_->make<TH1F>("h_probeDz","d_{z}(PV) of the probe track;track d_{z}(PV);tracks",200,-100,100 );    
  h_probeDxyErr = outfile_->make<TH1F>("h_probeDxyErr","error on d_{xy}(PV) of the probe track;track error on d_{xy}(PV);tracks",100,0.,100 );	   
  h_probeDzErr  = outfile_->make<TH1F>("h_probeDzErr","error on d_{z}(PV)  of the probe track;track erro on d_{z}(PV);tracks",100,0.,100 );	  

  mon.addHistogram( new TH1F( "nvtx",";Vertices;Events",50,0,50) );
  mon.addHistogram( new TH1F( "dxy",";d_{xy};tracks",100,-100,100) );
  mon.addHistogram( new TH1F( "dz",";d_{xy};tracks",100,-100,100) );
  mon.addHistogram( new TH1F( "dxyerr",";d_{xy} error;tracks",100,0.,200) );
  mon.addHistogram( new TH1F( "dxyerr",";d_{xy} error;tracks",100,0.,200) );
  mon.addHistogram( new TProfile( "dxyErrVsPt",";track p_{T};d_{xy} error",100,0.,200,0.,100.));
  mon.addHistogram( new TProfile( "dzErrVsPt" ,";track p_{T};d_{z} error" ,100,0.,200,0.,100.));
    
}

// ------------ method called once each job just after ending the event loop  ------------
void
JetHTAnalyzer::endJob()
{
  mon.Write();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
JetHTAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetHTAnalyzer);