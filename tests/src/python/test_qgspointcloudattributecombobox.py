# -*- coding: utf-8 -*-
"""QGIS Unit tests for QgsPointCloudAttributeComboBox

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Nyall Dawson'
__date__ = '09/11/2020'
__copyright__ = 'Copyright 2020, The QGIS Project'

import qgis  # NOQA

from qgis.core import (
    QgsProviderRegistry,
    QgsPointCloudLayer,
    QgsPointCloudAttributeCollection,
    QgsPointCloudAttributeProxyModel,
    QgsPointCloudAttribute
)
from qgis.gui import QgsPointCloudAttributeComboBox
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.PyQt.QtTest import QSignalSpy

from qgis.testing import start_app, unittest
from utilities import unitTestDataPath

start_app()


def create_attributes():
    collection = QgsPointCloudAttributeCollection()
    collection.push_back(QgsPointCloudAttribute('x', QgsPointCloudAttribute.Float))
    collection.push_back(QgsPointCloudAttribute('y', QgsPointCloudAttribute.Float))
    collection.push_back(QgsPointCloudAttribute('z', QgsPointCloudAttribute.Float))
    collection.push_back(QgsPointCloudAttribute('cat', QgsPointCloudAttribute.Char))
    collection.push_back(QgsPointCloudAttribute('red', QgsPointCloudAttribute.Int32))
    return collection


class TestQgsPointCloudAttributeComboBox(unittest.TestCase):

    def testGettersSetters(self):
        """ test combobox getters/setters """
        w = QgsPointCloudAttributeComboBox()
        w.setAttributes(create_attributes())
        self.assertEqual([a.name() for a in w.attributes().attributes()], ['x', 'y', 'z', 'cat', 'red'])

        w.setAttribute('red')
        self.assertEqual(w.currentAttribute(), 'red')

        self.assertIsNone(w.layer())

    def testSignals(self):
        w = QgsPointCloudAttributeComboBox()
        w.setAttributes(create_attributes())

        spy = QSignalSpy(w.attributeChanged)
        w.setAttribute('z')
        self.assertEqual(len(spy), 1)
        self.assertEqual(spy[-1][0], 'z')
        w.setAttribute('z')
        self.assertEqual(len(spy), 1)
        self.assertEqual(spy[-1][0], 'z')
        w.setAttribute('red')
        self.assertEqual(len(spy), 2)
        self.assertEqual(spy[-1][0], 'red')
        w.setAttribute(None)
        self.assertEqual(len(spy), 3)
        self.assertEqual(spy[-1][0], None)
        w.setAttribute(None)
        self.assertEqual(len(spy), 3)
        self.assertEqual(spy[-1][0], None)

    @unittest.skipIf('ept' not in QgsProviderRegistry.instance().providerList(), 'EPT provider not available')
    def testSetLayer(self):
        cb = QgsPointCloudAttributeComboBox()
        self.assertIsNone(cb.layer())
        layer = QgsPointCloudLayer(unitTestDataPath() + '/point_clouds/ept/sunshine-coast/ept.json', 'test', 'ept')
        self.assertTrue(layer.isValid())
        cb.setLayer(layer)
        self.assertEqual(cb.layer(), layer)
        self.assertEqual([cb.itemText(i) for i in range(cb.count())], ['X', 'Y', 'Z', 'Intensity', 'ReturnNumber', 'NumberOfReturns', 'ScanDirectionFlag', 'EdgeOfFlightLine', 'Classification', 'ScanAngleRank', 'UserData', 'PointSourceId', 'GpsTime', 'Red', 'Green', 'Blue'])

    def testFilter(self):
        cb = QgsPointCloudAttributeComboBox()
        cb.setAttributes(create_attributes())

        self.assertEqual([cb.itemText(i) for i in range(cb.count())], ['x', 'y', 'z', 'cat', 'red'])
        cb.setFilters(QgsPointCloudAttributeProxyModel.Numeric)
        self.assertEqual([cb.itemText(i) for i in range(cb.count())], ['x', 'y', 'z', 'red'])
        self.assertEqual(cb.filters(), QgsPointCloudAttributeProxyModel.Numeric)
        cb.setFilters(QgsPointCloudAttributeProxyModel.Char)
        self.assertEqual([cb.itemText(i) for i in range(cb.count())], ['cat'])
        self.assertEqual(cb.filters(), QgsPointCloudAttributeProxyModel.Char)
        cb.setFilters(QgsPointCloudAttributeProxyModel.Char | QgsPointCloudAttributeProxyModel.Int32)
        self.assertEqual([cb.itemText(i) for i in range(cb.count())], ['cat', 'red'])
        self.assertEqual(cb.filters(), QgsPointCloudAttributeProxyModel.Char | QgsPointCloudAttributeProxyModel.Int32)


if __name__ == '__main__':
    unittest.main()
