/***************************************************************************
    qgsmaptoolmeasurebearing.h
    ------------------------
    begin                : June 2021
    copyright            : (C) 2021 by Nyall Dawson
    email                : nyall dot dawson at gmail dot com
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#ifndef QGSMAPTOOLMEASUREBEARING_H
#define QGSMAPTOOLMEASUREBEARING_H

#include "qgsmaptool.h"
#include "qgspointxy.h"
#include "qgsdistancearea.h"
#include "qgis_app.h"

class QgsDisplayAngle;
class QgsRubberBand;
class QgsSnapIndicator;

//! Map tool to measure bearing between two points
class APP_EXPORT QgsMapToolMeasureBearing: public QgsMapTool
{
    Q_OBJECT
  public:
    QgsMapToolMeasureBearing( QgsMapCanvas *canvas );
    ~QgsMapToolMeasureBearing() override;

    Flags flags() const override { return QgsMapTool::AllowZoomRect; }
    void canvasMoveEvent( QgsMapMouseEvent *e ) override;
    void canvasReleaseEvent( QgsMapMouseEvent *e ) override;
    void keyPressEvent( QKeyEvent *e ) override;
    void activate() override;
    void deactivate() override;

  private:
    //! Points defining the angle (three for measuring)
    QList<QgsPointXY> mAnglePoints;
    QgsRubberBand *mRubberBand = nullptr;
    QgsDisplayAngle *mResultDisplay = nullptr;

    //! Creates a new rubber band and deletes the old one
    void createRubberBand();

    //! Tool for measuring
    QgsDistanceArea mDa;

    std::unique_ptr<QgsSnapIndicator> mSnapIndicator;

  public slots:
    //! Recalculate angle if projection state changed
    void updateSettings();

  private slots:
    //! Deletes the rubber band and the dialog
    void stopMeasuring();

    //! Configures distance area objects with ellipsoid / output crs
    void configureDistanceArea();

    friend class TestQgsMeasureBearingTool;

};

#endif // QGSMAPTOOLMEASUREBEARING_H
