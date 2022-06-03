/***************************************************************************
                       qgshttpheaderswidget.cpp
  This class implements simple UI for http header.

                              -------------------
          begin                : 2021-09-09
          copyright            : (C) 2021 B. De Mezzo
          email                : benoit dot de dot mezzo at oslandia dot com

***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

#include "qgshttpheaderwidget.h"
#include "ui_qgshttpheaderwidget.h"
#include "qgsapplication.h"


QgsHttpHeaderWidget::QgsHttpHeaderWidget( QWidget *parent )
  : QWidget( parent )
{
  setupUi( this );
  btnAddQueryPair->setIcon( QgsApplication::getThemeIcon( QStringLiteral( "/symbologyAdd.svg" ) ) );
  btnRemoveQueryPair->setIcon( QgsApplication::getThemeIcon( QStringLiteral( "/symbologyRemove.svg" ) ) );
  grpbxAdvanced->setCollapsed( true );

  // Action and interaction connections
  connect( btnAddQueryPair, &QToolButton::clicked, this, &QgsHttpHeaderWidget::addQueryPair );
  connect( btnRemoveQueryPair, &QToolButton::clicked, this, &QgsHttpHeaderWidget::removeQueryPair );
}

QgsHttpHeaderWidget::~QgsHttpHeaderWidget() = default;

void QgsHttpHeaderWidget::addQueryPairRow( const QString &key, const QString &val )
{
  const int rowCnt = tblwdgQueryPairs->rowCount();
  tblwdgQueryPairs->insertRow( rowCnt );

  const Qt::ItemFlags itemFlags = Qt::ItemIsEnabled | Qt::ItemIsSelectable
                                  | Qt::ItemIsEditable | Qt::ItemIsDropEnabled;

  QTableWidgetItem *keyItem = new QTableWidgetItem( key );
  keyItem->setFlags( itemFlags );
  tblwdgQueryPairs->setItem( rowCnt, 0, keyItem );

  QTableWidgetItem *valueItem = new QTableWidgetItem( val );
  keyItem->setFlags( itemFlags );
  tblwdgQueryPairs->setItem( rowCnt, 1, valueItem );
}

QgsHttpHeaders QgsHttpHeaderWidget::httpHeaders() const
{
  QgsHttpHeaders querypairs;
  for ( int i = 0; i < tblwdgQueryPairs->rowCount(); ++i )
  {
    if ( tblwdgQueryPairs->item( i, 0 )->text().isEmpty() )
    {
      continue;
    }
    querypairs [ tblwdgQueryPairs->item( i, 0 )->text() ] = QVariant( tblwdgQueryPairs->item( i, 1 )->text() ) ;
  }

  if ( !mRefererLineEdit->text().isEmpty() )
  {
    querypairs [ "referer" ] = QVariant( mRefererLineEdit->text() ) ;
  }
  return querypairs;
}


void QgsHttpHeaderWidget::addQueryPair()
{
  addQueryPairRow( QString(), QString() );
  tblwdgQueryPairs->setFocus();
  tblwdgQueryPairs->setCurrentCell( tblwdgQueryPairs->rowCount() - 1, 0 );
  tblwdgQueryPairs->edit( tblwdgQueryPairs->currentIndex() );
}


void QgsHttpHeaderWidget::removeQueryPair()
{
  tblwdgQueryPairs->removeRow( tblwdgQueryPairs->currentRow() );
}


void QgsHttpHeaderWidget::setFromSettings( const QgsSettings &settings, const QString &key )
{
  // load headers from settings
  QgsHttpHeaders headers;
  headers.setFromSettings( settings, key );

  // push headers to table
  tblwdgQueryPairs->clearContents();
  /*QTableWidgetItem * item;
  int row = 0;*/
  QList<QString> lst = headers.keys();
  for ( auto ite = lst.constBegin(); ite != lst.constEnd(); ++ite )
  {
    if ( ite->compare( "referer" ) != 0 )
    {
      addQueryPairRow( *ite, headers[ *ite ].toString() );
    }
    else
    {
      mRefererLineEdit->setText( headers[ *ite ].toString() );
    }
  }
}

void QgsHttpHeaderWidget::updateSettings( QgsSettings &settings, const QString &key ) const
{
  QgsHttpHeaders h = httpHeaders();
  h.updateSettings( settings, key );
}
