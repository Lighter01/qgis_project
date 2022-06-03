# -*- coding: utf-8 -*-
"""
Test the QgsSettingsEntry classes

Run with: ctest -V -R PyQgsSettingsEntry

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

from qgis import core as qgis_core
from qgis.core import Qgis, QgsSettings, QgsSettingsEntryVariant, QgsSettingsEntryString, QgsSettingsEntryStringList, QgsSettingsEntryBool, QgsSettingsEntryInteger, QgsSettingsEntryDouble, QgsSettingsEntryEnumFlag, QgsUnitTypes, QgsMapLayerProxyModel, QgsSettingsEntryGroup
from qgis.testing import start_app, unittest

from qgis.PyQt.QtGui import QColor

__author__ = 'Damiano Lombardi'
__date__ = '02/04/2021'
__copyright__ = 'Copyright 2021, The QGIS Project'


start_app()


class TestQgsSettingsEntry(unittest.TestCase):

    cnt = 0

    def setUp(self):
        self.pluginName = "UnitTest"

    def tearDown(self):
        pass

    def test_settings_entry_base(self):
        settingsKey = "settingsEntryBase/variantValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = 42
        description = "Variant value for basic functionality test"
        settingsEntryVariant = QgsSettingsEntryVariant(settingsKey, self.pluginName, defaultValue, description)

        # Check key
        self.assertEqual(settingsEntryVariant.key(), settingsKeyComplete)

        # Passing dynamicKeyPart to a non dynamic settings has no effect
        self.assertEqual(settingsEntryVariant.key("gugus"), settingsKeyComplete)

        self.assertEqual(settingsEntryVariant.hasDynamicKey(), False)

        # At this point settings should still not exists in underlyng QSettings as it was still not written (setValue)
        self.assertEqual(settingsEntryVariant.exists(), False)
        settingsEntryVariant.setValue(43)
        self.assertEqual(settingsEntryVariant.exists(), True)
        settingsEntryVariant.remove()
        self.assertEqual(settingsEntryVariant.exists(), False)

        # DefaultValue
        self.assertEqual(settingsEntryVariant.defaultValueAsVariant(), defaultValue)

        # Set/Get value
        # as settings still does not exists return default value
        self.assertEqual(settingsEntryVariant.valueAsVariant(), defaultValue)
        settingsEntryVariant.setValue(43)
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), 43)
        self.assertEqual(settingsEntryVariant.valueAsVariant(), 43)

        # Settings type
        self.assertEqual(settingsEntryVariant.settingsType(), Qgis.SettingsType.Variant)

        # Description
        self.assertEqual(settingsEntryVariant.description(), description)

    def test_settings_plugin_key(self):
        # be sure that the constructor in PyQGIS only creates keys with plugins prefix
        settings_types = [x for x in dir(qgis_core) if x.startswith('QgsSettingsEntry') and not x.endswith('Base') and x != 'QgsSettingsEntryGroup']
        hardcoded_types = {
            'QgsSettingsEntryBool': True,
            'QgsSettingsEntryColor': QColor(),
            'QgsSettingsEntryDouble': 0.0,
            'QgsSettingsEntryEnumFlag': QgsUnitTypes.LayoutMeters,
            'QgsSettingsEntryInteger': 1,
            'QgsSettingsEntryString': 'Hello',
            'QgsSettingsEntryStringList': [],
            'QgsSettingsEntryVariant': 1
        }
        self.assertEqual(settings_types, list(hardcoded_types.keys()))
        for setting_type, default_value in hardcoded_types.items():
            settings_key = "settings/key_{}".format(setting_type)
            settings_key_complete = "plugins/{}/{}".format(self.pluginName, settings_key)
            QgsSettings().remove(settings_key_complete)
            settings_entry = eval('qgis_core.{}(settings_key, self.pluginName, default_value)'.format(setting_type))
            self.assertEqual(settings_entry.key(), settings_key_complete)

    def test_settings_entry_base_default_value_override(self):
        settingsKey = "settingsEntryBase/defaultValueOverride/variantValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = 42
        defaultValueOverride = 123
        description = "Variant value for default override functionality test"
        settingsEntryVariant = QgsSettingsEntryVariant(settingsKey, self.pluginName, defaultValue, description)

        # Normal default value
        self.assertEqual(settingsEntryVariant.value(), defaultValue)

        # Normal default value
        self.assertEqual(settingsEntryVariant.value(), defaultValue)

        # Overridden default value
        self.assertEqual(settingsEntryVariant.valueWithDefaultOverride(defaultValueOverride), defaultValueOverride)

    def test_settings_entry_base_dynamic_key(self):
        settingsKeyDynamic = "settingsEntryBase/%1/variantValue"
        dynamicKeyPart1 = "first"
        dynamicKeyPart2 = "second"
        settingsKeyComplete1 = "plugins/{}/{}".format(self.pluginName, settingsKeyDynamic).replace("%1", dynamicKeyPart1)
        settingsKeyComplete2 = "plugins/{}/{}".format(self.pluginName, settingsKeyDynamic).replace("%1", dynamicKeyPart2)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete1)
        QgsSettings().remove(settingsKeyComplete2)

        defaultValue = 42
        settingsEntryVariantDynamic = QgsSettingsEntryVariant(settingsKeyDynamic, self.pluginName, defaultValue, "Variant value for dynamic key functionality test")

        # Check key
        self.assertEqual(settingsEntryVariantDynamic.key(dynamicKeyPart1), settingsKeyComplete1)
        self.assertEqual(settingsEntryVariantDynamic.key(dynamicKeyPart2), settingsKeyComplete2)

        # Get set values
        settingsEntryVariantDynamic.setValue(43, dynamicKeyPart1)
        settingsEntryVariantDynamic.setValue(44, dynamicKeyPart2)
        self.assertEqual(QgsSettings().value(settingsKeyComplete1, defaultValue), 43)
        self.assertEqual(QgsSettings().value(settingsKeyComplete2, defaultValue), 44)
        self.assertEqual(settingsEntryVariantDynamic.value(dynamicKeyPart1), 43)
        self.assertEqual(settingsEntryVariantDynamic.value(dynamicKeyPart2), 44)

    def test_settings_entry_base_dynamic_multiple_keys(self):
        settingsKeyDynamic = "settingsEntryBase/%1/anotherPart_%2/variantValue"
        dynamicKeyPart1 = "first"
        dynamicKeyPart2 = "second"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKeyDynamic).replace("%1", dynamicKeyPart1).replace("%2", dynamicKeyPart2)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = 42
        settingsEntryVariantDynamic = QgsSettingsEntryVariant(settingsKeyDynamic, self.pluginName, defaultValue, "Variant value for dynamic multiple keys functionality test")

        # Check key
        self.assertEqual(settingsEntryVariantDynamic.key([dynamicKeyPart1, dynamicKeyPart2]), settingsKeyComplete)

        # Get set values
        settingsEntryVariantDynamic.setValue(43, [dynamicKeyPart1, dynamicKeyPart2])
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), 43)
        self.assertEqual(settingsEntryVariantDynamic.value([dynamicKeyPart1, dynamicKeyPart2]), 43)

    def test_settings_entry_variant(self):
        settingsKey = "settingsEntryVariant/variantValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = 42
        description = "Variant value functionality test"
        settingsEntryVariant = QgsSettingsEntryVariant(settingsKey, self.pluginName, defaultValue, description)

        # Set/Get value
        # as settings still does not exists return default value
        self.assertEqual(settingsEntryVariant.valueAsVariant(), defaultValue)
        settingsEntryVariant.setValue("abc")
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), "abc")
        self.assertEqual(settingsEntryVariant.valueAsVariant(), "abc")

        # Settings type
        self.assertEqual(settingsEntryVariant.settingsType(), Qgis.SettingsType.Variant)

    def test_settings_entry_string(self):
        settingsKey = "settingsEntryString/stringValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = "abc"
        description = "String value functionality test"
        settingsEntryString = QgsSettingsEntryString(settingsKey, self.pluginName, defaultValue, description)

        # Set/Get value
        # as settings still does not exists return default value
        self.assertEqual(settingsEntryString.valueAsVariant(), defaultValue)
        settingsEntryString.setValue("xyz")
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), "xyz")
        self.assertEqual(settingsEntryString.valueAsVariant(), "xyz")

        # Settings type
        self.assertEqual(settingsEntryString.settingsType(), Qgis.SettingsType.String)

    def test_settings_entry_stringlist(self):
        settingsKey = "settingsEntryStringList/stringListValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = ["abc", "def"]
        description = "String list value functionality test"
        settingsEntryStringList = QgsSettingsEntryStringList(settingsKey, self.pluginName, defaultValue, description)

        # Set/Get value
        # as settings still does not exists return default value
        self.assertEqual(settingsEntryStringList.valueAsVariant(), defaultValue)
        settingsEntryStringList.setValue(["uvw", "xyz"])
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), ["uvw", "xyz"])
        self.assertEqual(settingsEntryStringList.valueAsVariant(), ["uvw", "xyz"])

        # Settings type
        self.assertEqual(settingsEntryStringList.settingsType(), Qgis.SettingsType.StringList)

    def test_settings_entry_bool(self):
        settingsKey = "settingsEntryBool/boolValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = False
        description = "Bool value functionality test"
        settingsEntryBool = QgsSettingsEntryBool(settingsKey, self.pluginName, defaultValue, description)

        # Set/Get value
        # as settings still does not exists return default value
        self.assertEqual(settingsEntryBool.valueAsVariant(), defaultValue)
        settingsEntryBool.setValue(True)
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), True)
        self.assertEqual(settingsEntryBool.valueAsVariant(), True)

        # Settings type
        self.assertEqual(settingsEntryBool.settingsType(), Qgis.SettingsType.Bool)

    def test_settings_entry_integer(self):
        settingsKey = "settingsEntryInteger/integerValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = 42
        description = "Integer value functionality test"
        settingsEntryInteger = QgsSettingsEntryInteger(settingsKey, self.pluginName, defaultValue, description)

        # Set/Get value
        # as settings still does not exists return default value
        self.assertEqual(settingsEntryInteger.valueAsVariant(), defaultValue)
        settingsEntryInteger.setValue(43)
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), 43)
        self.assertEqual(settingsEntryInteger.valueAsVariant(), 43)

        # Set/Get negative value
        settingsEntryInteger.setValue(-42)
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), -42)
        self.assertEqual(settingsEntryInteger.valueAsVariant(), -42)

        # Settings type
        self.assertEqual(settingsEntryInteger.settingsType(), Qgis.SettingsType.Integer)

    def test_settings_entry_double(self):
        settingsKey = "settingsEntryDouble/doubleValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = 3.14
        description = "Double value functionality test"
        settingsEntryDouble = QgsSettingsEntryDouble(settingsKey, self.pluginName, defaultValue, description)

        # Set/Get value
        # as settings still does not exists return default value
        self.assertEqual(settingsEntryDouble.valueAsVariant(), defaultValue)
        settingsEntryDouble.setValue(1.618)
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), 1.618)
        self.assertEqual(settingsEntryDouble.valueAsVariant(), 1.618)

        # Set/Get negative value
        settingsEntryDouble.setValue(-273.15)
        # Verify setValue using QgsSettings
        self.assertEqual(QgsSettings().value(settingsKeyComplete, defaultValue), -273.15)
        self.assertEqual(settingsEntryDouble.valueAsVariant(), -273.15)

        # Settings type
        self.assertEqual(settingsEntryDouble.settingsType(), Qgis.SettingsType.Double)

    def test_settings_entry_enum(self):
        settingsKey = "settingsEntryEnum/enumValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        defaultValue = QgsUnitTypes.LayoutMeters
        description = "Enum value functionality test"
        settingsEntryEnum = QgsSettingsEntryEnumFlag(settingsKey, self.pluginName, defaultValue, description)

        # Check default value
        self.assertEqual(settingsEntryEnum.defaultValue(), QgsUnitTypes.LayoutMeters)

        # Check set value
        success = settingsEntryEnum.setValue(QgsUnitTypes.LayoutFeet)
        self.assertEqual(success, True)
        qgsSettingsValue = QgsSettings().enumValue(settingsKeyComplete, QgsUnitTypes.LayoutMeters)
        self.assertEqual(qgsSettingsValue, QgsUnitTypes.LayoutFeet)

        # Check get value
        QgsSettings().setEnumValue(settingsKeyComplete, QgsUnitTypes.LayoutPicas)
        self.assertEqual(settingsEntryEnum.value(), QgsUnitTypes.LayoutPicas)

        # Check settings type
        self.assertEqual(settingsEntryEnum.settingsType(), Qgis.SettingsType.EnumFlag)

        # assign to inexisting value
        success = settingsEntryEnum.setValue(-1)
        self.assertEqual(success, False)

        # Current value should not have changed
        qgsSettingsValue = QgsSettings().enumValue(settingsKeyComplete, QgsUnitTypes.LayoutMeters)
        self.assertEqual(qgsSettingsValue, QgsUnitTypes.LayoutPicas)

        # With save as integer option
        settingsEntryEnumAsInteger = QgsSettingsEntryEnumFlag(settingsKey, self.pluginName, defaultValue, description, Qgis.SettingsOption.SaveEnumFlagAsInt)
        settingsEntryEnumAsInteger.remove()
        self.assertEqual(settingsEntryEnumAsInteger.value(), defaultValue)
        success = settingsEntryEnumAsInteger.setValue(QgsUnitTypes.LayoutFeet)
        self.assertEqual(success, True)
        qgsSettingsValue = QgsSettings().value(settingsKeyComplete, int(QgsUnitTypes.LayoutMeters))
        self.assertEqual(qgsSettingsValue, int(QgsUnitTypes.LayoutFeet))

    def test_settings_entry_flag(self):
        settingsKey = "settingsEntryFlag/flagValue"
        settingsKeyComplete = "plugins/{}/{}".format(self.pluginName, settingsKey)

        pointAndLine = QgsMapLayerProxyModel.Filters(QgsMapLayerProxyModel.PointLayer | QgsMapLayerProxyModel.LineLayer)
        pointAndPolygon = QgsMapLayerProxyModel.Filters(QgsMapLayerProxyModel.PointLayer | QgsMapLayerProxyModel.PolygonLayer)
        hasGeometry = QgsMapLayerProxyModel.Filters(QgsMapLayerProxyModel.HasGeometry)

        # Make sure settings does not exists
        QgsSettings().remove(settingsKeyComplete)

        description = "Flag value functionality test"
        settingsEntryFlag = QgsSettingsEntryEnumFlag(settingsKey, self.pluginName, pointAndLine, description)

        # Check default value
        self.assertEqual(settingsEntryFlag.defaultValue(), pointAndLine)

        # Check set value
        success = settingsEntryFlag.setValue(hasGeometry)
        self.assertEqual(success, True)
        qgsSettingsValue = QgsSettings().flagValue(settingsKeyComplete, pointAndLine)
        self.assertEqual(qgsSettingsValue, hasGeometry)

        # Check get value
        QgsSettings().setValue(settingsKeyComplete, 'PointLayer|PolygonLayer')
        self.assertEqual(settingsEntryFlag.value(), pointAndPolygon)

        # Check settings type
        self.assertEqual(settingsEntryFlag.settingsType(), Qgis.SettingsType.EnumFlag)

    def test_settings_entry_group(self):
        settingsEntryString_1 = QgsSettingsEntryString('my/key/has/levels/my-setting-key-1', self.pluginName)
        settingsEntryString_2 = QgsSettingsEntryString('my/key/has/levels/my-setting-key-2', self.pluginName)
        settingsEntryString_3 = QgsSettingsEntryString('my-setting-key-3', self.pluginName)
        settingsEntryString_4 = QgsSettingsEntryString('my-setting-key-4', self.pluginName)

        group_1 = QgsSettingsEntryGroup([settingsEntryString_1, settingsEntryString_2])
        self.assertTrue(group_1.isValid())
        group_2 = QgsSettingsEntryGroup([settingsEntryString_3, settingsEntryString_4])
        self.assertTrue(group_2.isValid())
        with self.assertRaises(ValueError):
            QgsSettingsEntryGroup([settingsEntryString_1, settingsEntryString_3])

        settingsEntryString_1.setValue('value-1')
        settingsEntryString_2.setValue('value-2')
        self.assertTrue(settingsEntryString_1.exists())
        self.assertTrue(settingsEntryString_2.exists())
        group_1.removeAllSettingsAtBaseKey()
        self.assertFalse(settingsEntryString_1.exists())
        self.assertFalse(settingsEntryString_2.exists())

        settingsEntryString_1.setValue('value-1')
        settingsEntryString_2.setValue('value-2')
        self.assertTrue(settingsEntryString_1.exists())
        self.assertTrue(settingsEntryString_2.exists())
        group_1.removeAllChildrenSettings()
        self.assertFalse(settingsEntryString_1.exists())
        self.assertFalse(settingsEntryString_2.exists())


if __name__ == '__main__':
    unittest.main()
