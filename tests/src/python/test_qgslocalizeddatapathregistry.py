# -*- coding: utf-8 -*-
"""QGIS Unit tests for QgsLocalizedDataPathRegistry.

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Denis Rouzaud'
__date__ = '13/05/2020'
__copyright__ = 'Copyright 2019, The QGIS Project'

import qgis  # NOQA

from tempfile import NamedTemporaryFile
import tempfile
from pathlib import Path
import os
import shutil
from qgis.core import (
    QgsApplication,
    QgsPathResolver,
    QgsProject,
    QgsVectorLayer
)
from qgis.PyQt.QtCore import QDir
from qgis.testing import start_app, unittest

start_app()

MAP_PATH = "data/world_map.gpkg"
BASE_PATH = QgsApplication.pkgDataPath() + '/resources'
ABSOLUTE_PATH = '{}/{}'.format(BASE_PATH, MAP_PATH)


class TestQgsLocalizedDataPathRegistry(unittest.TestCase):
    """
    Test resolving and saving localized data paths
    """

    @classmethod
    def setUpClass(cls):
        cls.temp_path = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_path)

    def setUp(self):
        QgsApplication.localizedDataPathRegistry().registerPath(BASE_PATH)

    def tearDown(self):
        QgsApplication.localizedDataPathRegistry().unregisterPath(BASE_PATH)

    def testQgsLocalizedDataPathRegistry(self):
        self.assertEqual(QgsApplication.localizedDataPathRegistry().localizedPath(ABSOLUTE_PATH), MAP_PATH)
        self.assertEqual(QgsApplication.localizedDataPathRegistry().globalPath(MAP_PATH), ABSOLUTE_PATH)

    def testOrderOfPreference(self):
        os.mkdir('{}/data'.format(self.temp_path))
        alt_dir = '{}/{}'.format(self.temp_path, MAP_PATH)
        Path(alt_dir).touch()
        QgsApplication.localizedDataPathRegistry().registerPath(self.temp_path, 0)
        self.assertEqual(QDir.toNativeSeparators(QgsApplication.localizedDataPathRegistry().globalPath(MAP_PATH)), QDir.toNativeSeparators(alt_dir))
        QgsApplication.localizedDataPathRegistry().unregisterPath(self.temp_path)

    def testWithResolver(self):
        self.assertEqual(QgsPathResolver().readPath('localized:' + MAP_PATH), ABSOLUTE_PATH)
        self.assertEqual(QgsPathResolver().writePath(ABSOLUTE_PATH), 'localized:' + MAP_PATH)

    def testProject(self):
        layer = QgsVectorLayer('{}|layername=countries'.format(ABSOLUTE_PATH), 'Test', 'ogr')

        # write
        p = QgsProject()
        fh = NamedTemporaryFile(delete=False)
        p.setFileName(fh.name)
        p.addMapLayer(layer)
        self.assertTrue(p.write())
        found = False
        with open(fh.name) as fh:
            for line in fh:
                if '<datasource>localized:data/world_map.gpkg|layername=countries</datasource>' in line:
                    found = True
                    break
        self.assertTrue(found)

        # read
        p2 = QgsProject()
        p2.setFileName(fh.name)
        p2.read()
        self.assertTrue(len(p2.mapLayers()))
        self.assertEqual(p2.mapLayers()[layer.id()].source(), '{}/{}|layername=countries'.format(BASE_PATH, MAP_PATH))

        os.remove(fh.name)


if __name__ == '__main__':
    unittest.main()
