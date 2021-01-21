#include "JetHtPlotConfiguration.h"

using namespace std;

int main(int argc, char **argv){

  JetHtPlotConfiguration *myConf = new JetHtPlotConfiguration();

  myConf->ReadJsonFile("jetHtPlotConfiguration.json");

  cout << endl;
  cout << "Blue: " << kBlue << endl;
  cout << "Red: " << kRed << endl;
  cout << "Green: " << kGreen+2 << endl;
  cout << endl;

  myConf->PrintConfiguration();

}
