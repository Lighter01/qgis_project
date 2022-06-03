/***************************************************************************
                           dummy.cpp

  Sample service implementation
  -----------------------------
  begin                : 2016-12-13
  copyright            : (C) 2016 by David Marteau
  email                : david dot marteau at 3liz dot com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#include "qgsmodule.h"
#include "ctsmath.h"
#include "ctsinit.h"
#include "ctstypes.h"
#include "ctscore.h"

//#include "std.h"
//#include <string.h>е
#include <vector>
#include <string>
//#include <cmath>
#include <algorithm>

#include <fstream>
#include <sstream>

#include <iostream>
#include <iomanip>

# define M_PI           3.14159265358979323846
// Service

    static std::ifstream AIR("//home//parallels//dev//cpp//TLKTestRepo//src//server//services//DummyService//airport_country.csv");
    static std::ifstream CAPITAL("//home//parallels//dev//cpp//TLKTestRepo//src//server//services//DummyService//country-capitals.csv");

    std::vector<Airports> airports;
    std::vector<City> capitals;



///////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////
enum RequestType {
    REQ_UNSET,
    REQ_GETTRACK,
    REQ_GETBOTHPATH,
    REQ_GETAIRPATH,
    REQ_GETGROUNDPATH,
};

class SampleService: public QgsService
{
  public:
    QString name()    const override { return "CTS"; }
    QString version() const override { return "1.1"; }

    void executeRequest( const QgsServerRequest &request, QgsServerResponse &response,
                         const QgsProject *project ) override
    {
      Q_UNUSED( project )
      Q_UNUSED( request )
//      std::cout<<request.serverParameters().value(QString("SERVICE")).toStdString().c_str()<<std::endl;
//      QgsServiceRegistry *QgsServer::sServiceRegistry = nullptr;
//      sServiceRegistry = new QgsServiceRegistry();
//      QgsService *service = sServiceRegistry->getService( QString("WCS"), "1.0.1" );
      QUrl url = request.originalUrl();
      QUrlQuery q( url );

      const QList<QPair<QString, QString> > queryItems = q.queryItems();
      RequestType mRequestType=REQ_UNSET;
      for ( const QPair<QString, QString> &param : queryItems )
      {
//      response.write( param.first.toUpper()+" "+param.second.toLower()+QString ("\n"));
            if (param.first.toUpper().contains(QString("REQUEST"),Qt::CaseInsensitive)){
                if (param.second.toUpper().contains(QString("GETTRACK"),Qt::CaseInsensitive)){
                    mRequestType = REQ_GETTRACK;
//                    response.write( QString( "GETTRACK!!!!!!:\n" ) );
                }
                if (param.second.compare(QString("GETAIRPATH"),Qt::CaseInsensitive)==0){
                    mRequestType = REQ_GETAIRPATH;
                    response.write( QString( "GETAIRPATH:\n" ) );
                }
                if (param.second.compare(QString("GETBOTHPATH"),Qt::CaseInsensitive)==0){
                    mRequestType = REQ_GETBOTHPATH;
                    response.write( QString( "GETBOTHPATH:\n" ) );
                }
                if (param.second.compare(QString("GETGROUNDPATH"),Qt::CaseInsensitive)==0){
                    mRequestType = REQ_GETGROUNDPATH;
                    response.write( QString( "GETGROUNDPATH:\n" ) );
                }
                if (mRequestType == REQ_UNSET){
                    response.write( QString( "UNKNOWN REQUEST:\n" ) );
                    response.write( param.second );
                    response.write( QString( "\n" ) );
                }
            }
      }
      std::vector<std::string> countryVector;
      switch (mRequestType){
          case REQ_GETTRACK:
              {
//                  response.write( QString( "GETTRACK:\n" ) );
                  for ( const QPair<QString, QString> &param : queryItems )
                  {
                      if (param.first.toUpper().contains(QString("cnt"),Qt::CaseInsensitive)){
                          countryVector.push_back(param.second.toStdString());
                      }
                  }

//                  for (auto tmp : countryVector) {
//                      std::string tmpString("cnt "+tmp+"\n");
//                      response.write( QString::fromStdString( tmpString));
//                  }
                  std::vector<Line> path = Path(countryVector, airports, capitals);
                  for (auto tmp : path) {
                        response.write(QString::fromStdString("From "+tmp.begin.name+" To "+tmp.end.name+"\n"));
                  }
//long double getPathLength(std::vector<Line>& Path, Path_type state) { // both == Ground + Air
//                  long double mPathLength=getPathLength(path,ground);
//                  response.write(QString::fromStdString("Ground distance = "+std::to_string(mPathLength)+"Km \n"));
//                  mPathLength=getPathLength(path,both);
//                  response.write(QString::fromStdString("Total distance = "+std::to_string(mPathLength)+"Km \n"));
//                  mPathLength=getPathLength(path,air);
//                  response.write(QString::fromStdString("Flight distance = "+std::to_string(mPathLength)+"Km \n"));
                  break;
              }
          case REQ_GETAIRPATH:
              {
//                  response.write( QString( "GETTRACK:\n" ) );
                  for ( const QPair<QString, QString> &param : queryItems )
                  {
                      if (param.first.toUpper().contains(QString("cnt"),Qt::CaseInsensitive)){
                          countryVector.push_back(param.second.toStdString());
                      }
                  }

                  std::vector<Line> path = Path(countryVector, airports, capitals);
                  long double mPathLength=getPathLength(path,air);
                  response.write(QString::fromStdString("Flight distance = "+std::to_string(mPathLength)+"Km \n"));
                  break;
              }
          case REQ_GETBOTHPATH:
              {
//                  response.write( QString( "GETTRACK:\n" ) );
                  for ( const QPair<QString, QString> &param : queryItems )
                  {
                      if (param.first.toUpper().contains(QString("cnt"),Qt::CaseInsensitive)){
                          countryVector.push_back(param.second.toStdString());
                      }
                  }

                  std::vector<Line> path = Path(countryVector, airports, capitals);
                  long double mPathLength=getPathLength(path,both);
                  response.write(QString::fromStdString("Full distance = "+std::to_string(mPathLength)+"Km \n"));
                  break;
              }
          case REQ_GETGROUNDPATH:
              {
//                  response.write( QString( "GETTRACK:\n" ) );
                  for ( const QPair<QString, QString> &param : queryItems )
                  {
                      if (param.first.toUpper().contains(QString("cnt"),Qt::CaseInsensitive)){
                          countryVector.push_back(param.second.toStdString());
                      }
                  }

                  std::vector<Line> path = Path(countryVector, airports, capitals);
                  long double mPathLength=getPathLength(path,ground);
                  response.write(QString::fromStdString("Ground distance = "+std::to_string(mPathLength)+"Km \n"));
                  break;
              }
          default:
              break;
      }

//        if ( sFilter.contains( param.first.toUpper() ) )
//          q.removeAllQueryItems( param.first );
//      response.write( QString( "Hello world from CTS" ) );
    }
};

// Module
class QgsSampleModule: public QgsServiceModule
{
  public:
    void registerSelf( QgsServiceRegistry &registry, QgsServerInterface *serverIface ) override
    {
      Q_UNUSED( serverIface )
      QgsDebugMsg( QStringLiteral( "CTS::registerSelf called" ) );
      registry.registerService( new  SampleService() );
    }
};

// Entry points
QGISEXTERN QgsServiceModule *QGS_ServiceModule_Init()
{
  static QgsSampleModule sModule;
    readAirports(AIR, airports);
    readCapital(CAPITAL, capitals);
  return &sModule;
}
QGISEXTERN void QGS_ServiceModule_Exit( QgsServiceModule * )
{
  // Nothing to do
}





