CREATE TABLE QGIS.SOME_DATA ( "pk" INTEGER PRIMARY KEY, "cnt" INTEGER, "name" VARCHAR2(100) DEFAULT 'qgis', "name2" VARCHAR2(100) DEFAULT 'qgis', "num_char" VARCHAR2(100), "dt" TIMESTAMP, "date" DATE, "time" VARCHAR2(100), GEOM SDO_GEOMETRY);

INSERT INTO QGIS.SOME_DATA ("pk", "cnt", "name", "name2", "num_char", "dt", "date", "time", GEOM)
      SELECT 5, -200, NULL, 'NuLl', '5', TIMESTAMP '2020-05-04 12:13:14', DATE '2020-05-02','12:13:01', SDO_GEOMETRY( 2001,4326,SDO_POINT_TYPE(-71.123, 78.23, NULL), NULL, NULL) from dual
  UNION ALL SELECT 3,  300, 'Pear', 'PEaR', '3', NULL, NULL, NULL, NULL from dual
  UNION ALL SELECT 1,  100, 'Orange', 'oranGe', '1', TIMESTAMP '2020-05-03 12:13:14', DATE '2020-05-03','12:13:14', SDO_GEOMETRY( 2001,4326,SDO_POINT_TYPE(-70.332, 66.33, NULL), NULL, NULL) from dual
  UNION ALL SELECT 2,  200, 'Apple', 'Apple', '2', TIMESTAMP '2020-05-04 12:14:14', DATE '2020-05-04','12:14:14', SDO_GEOMETRY( 2001,4326,SDO_POINT_TYPE(-68.2, 70.8, NULL), NULL, NULL) from dual
  UNION ALL SELECT 4,  400, 'Honey', 'Honey', '4', TIMESTAMP '2021-05-04 13:13:14', DATE '2021-05-04','13:13:14', SDO_GEOMETRY( 2001,4326,SDO_POINT_TYPE(-65.32, 78.3, NULL), NULL, NULL) from dual;

INSERT INTO user_sdo_geom_metadata (TABLE_NAME, COLUMN_NAME, DIMINFO, SRID) VALUES ( 'SOME_DATA', 'GEOM', sdo_dim_array(sdo_dim_element('X',-75,-55,0.005),sdo_dim_element('Y',65,85,0.005)),4326);

CREATE INDEX some_data_spatial_idx ON QGIS.SOME_DATA(GEOM) INDEXTYPE IS MDSYS.SPATIAL_INDEX;

CREATE TABLE QGIS.SOME_POLY_DATA ( "pk" INTEGER PRIMARY KEY, GEOM SDO_GEOMETRY);

INSERT INTO QGIS.SOME_POLY_DATA ("pk", GEOM)
      SELECT 1, SDO_GEOMETRY( 2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1), SDO_ORDINATE_ARRAY(-69.0,81.4 , -69.0,80.2 , -73.7,80.2 , -73.7,76.3 , -74.9,76.3 , -74.9,81.4 , -69.0,81.4)) from dual
  UNION ALL SELECT 2, SDO_GEOMETRY( 2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1), SDO_ORDINATE_ARRAY(-67.6,81.2 , -66.3,81.2 , -66.3,76.9 , -67.6,76.9 , -67.6,81.2))from dual
  UNION ALL SELECT 3, SDO_GEOMETRY( 2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1), SDO_ORDINATE_ARRAY(-68.4,75.8 , -67.5,72.6 , -68.6,73.7 , -70.2,72.9 , -68.4,75.8)) from dual
  UNION ALL SELECT 4,  NULL from dual;

INSERT INTO user_sdo_geom_metadata (TABLE_NAME, COLUMN_NAME, DIMINFO, SRID) VALUES ( 'SOME_POLY_DATA', 'GEOM', sdo_dim_array(sdo_dim_element('X',-80,-55,0.005),sdo_dim_element('Y',65,85,0.005)),4326);

CREATE INDEX some_poly_data_spatial_idx ON QGIS.SOME_POLY_DATA(GEOM) INDEXTYPE IS MDSYS.SPATIAL_INDEX;


CREATE TABLE QGIS.POINT_DATA ( "pk" INTEGER PRIMARY KEY, GEOM SDO_GEOMETRY);
INSERT INTO QGIS.POINT_DATA ("pk", GEOM)
 SELECT 1, SDO_GEOMETRY( 2001,4326,SDO_POINT_TYPE(1, 2, NULL), NULL, NULL) from dual
  UNION ALL SELECT 2, SDO_GEOMETRY( 3001,4326,SDO_POINT_TYPE(1, 2, 3), NULL, NULL) from dual
  UNION ALL SELECT 3, SDO_GEOMETRY( 3005,4326,NULL, sdo_elem_info_array (1,1,1, 4,1,1), sdo_ordinate_array (1,2,3, 4,5,6)) from dual
  UNION ALL SELECT 4, SDO_GEOMETRY( 2005,4326,NULL, sdo_elem_info_array (1,1,1, 3,1,1), sdo_ordinate_array (1,2, 3,4)) from dual
  UNION ALL SELECT 5, SDO_GEOMETRY( 3005,4326,NULL, sdo_elem_info_array (1,1,2), sdo_ordinate_array (1,2,3, 4,5,6)) from dual
  UNION ALL SELECT 6, SDO_GEOMETRY( 2001,4326,NULL, sdo_elem_info_array (1,1,1), sdo_ordinate_array (1,2)) from dual
  UNION ALL SELECT 7, SDO_GEOMETRY( 2001,4326, SDO_POINT_TYPE(3, 4, NULL), NULL, NULL) from dual
  UNION ALL SELECT 8, SDO_GEOMETRY( 2001,4326,NULL, sdo_elem_info_array (1,1,1), sdo_ordinate_array (5,6)) from dual;

CREATE TABLE QGIS.LINE_DATA ( "pk" INTEGER PRIMARY KEY, GEOM SDO_GEOMETRY);
INSERT INTO QGIS.LINE_DATA ("pk", GEOM)
      SELECT 1, SDO_GEOMETRY( 2002,3857,NULL, SDO_ELEM_INFO_ARRAY(1,2,1), SDO_ORDINATE_ARRAY(1,2,3,4,5,6)) from dual
  UNION ALL SELECT 2, SDO_GEOMETRY(2002,3857,NULL, SDO_ELEM_INFO_ARRAY(1, 2, 2), SDO_ORDINATE_ARRAY(1, 2, 5, 4, 7, 2.2, 10, .1, 13, 4)) from dual
  UNION ALL SELECT 3, SDO_GEOMETRY(2002,3857,NULL, SDO_ELEM_INFO_ARRAY(1,4,3, 1,2,1, 3,2,2, 11,2,1), SDO_ORDINATE_ARRAY(-1, -5, 1, 2, 5, 4, 7, 2.2, 10, 0.1, 13, 4, 17, -6.)) from dual
  UNION ALL SELECT 4, SDO_GEOMETRY(3002,3857,NULL, SDO_ELEM_INFO_ARRAY(1,2,1), SDO_ORDINATE_ARRAY(1,2,3,4,5,6,7,8,9)) from dual
  UNION ALL SELECT 5, SDO_GEOMETRY(2006,3857,NULL, SDO_ELEM_INFO_ARRAY(1,2,1, 5,2,1), SDO_ORDINATE_ARRAY(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)) from dual
  UNION ALL SELECT 6, SDO_GEOMETRY(3006,3857,NULL, SDO_ELEM_INFO_ARRAY(1,2,1, 7,2,1), SDO_ORDINATE_ARRAY(1, 2, 11, 3, 4, -11, 5, 6, 9, 7, 8, 1, 9, 10, -3)) from dual
  UNION ALL SELECT 7, SDO_GEOMETRY(2006,3857,NULL, SDO_ELEM_INFO_ARRAY(1,2,2, 11,2,2), SDO_ORDINATE_ARRAY(1, 2, 5, 4, 7, 2.2, 10, .1, 13, 4, -11, -3, 5, 7, 10, -1)) from dual
  UNION ALL SELECT 8, SDO_GEOMETRY(2006,3857,NULL, SDO_ELEM_INFO_ARRAY(1,4,3, 1,2,1, 3,2,2, 11,2,1, 15,2,2, 25,2,1), SDO_ORDINATE_ARRAY(-1, -5, 1, 2, 5, 4, 7, 2.2, 10, .1, 13, 4, 17, -6, 1, 3, 5, 5, 7, 3.2, 10, 1.1, 13, 5, -11, -3, 5, 7, 10, -1)) from dual;

CREATE TABLE QGIS.POLY_DATA ( "pk" INTEGER PRIMARY KEY, GEOM SDO_GEOMETRY);
INSERT INTO QGIS.POLY_DATA ("pk", GEOM)
      SELECT 1, SDO_GEOMETRY(2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1), SDO_ORDINATE_ARRAY(1, 2, 11, 2, 11, 22, 1, 22, 1, 2)) from dual
  UNION ALL SELECT 2, SDO_GEOMETRY(3003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1), SDO_ORDINATE_ARRAY(1, 2, 3, 11, 2, 13, 11, 22, 15, 1, 22, 7, 1, 2, 3)) from dual
  UNION ALL SELECT 3, SDO_GEOMETRY(2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1, 11,2003,1, 19,2003,1), SDO_ORDINATE_ARRAY(1, 2, 11, 2, 11, 22, 1, 22, 1, 2, 5, 6, 8, 9, 8, 6, 5, 6, 3, 4, 5, 6, 3, 6, 3, 4)) from dual
  UNION ALL SELECT 4, SDO_GEOMETRY(3003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1, 16,2003,1), SDO_ORDINATE_ARRAY(1, 2, 3, 11, 2, 13, 11, 22, 15, 1, 22, 7, 1, 2, 3, 5, 6, 1, 8, 9, -1, 8, 6, 2, 5, 6, 1)) from dual
  UNION ALL SELECT 5, SDO_GEOMETRY(2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,3), SDO_ORDINATE_ARRAY(1.0, 2.0, 11.0, 22.0)) from dual
  UNION ALL SELECT 6, SDO_GEOMETRY(2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,4), SDO_ORDINATE_ARRAY(1.0, 2.0, 11.0, 22.0, 15.0, 4.0)) from dual
  UNION ALL SELECT 7, SDO_GEOMETRY(2007,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1, 11,1003,1, 21,2003,1, 29,2003,1), SDO_ORDINATE_ARRAY(1, 2, 11, 2, 11, 22, 1, 22, 1, 2, 1, 2, 11, 2, 11, 22, 1, 22, 1, 2, 5, 6, 8, 9, 8, 6, 5, 6, 3, 4, 5, 6, 3, 6, 3, 4)) from dual
  UNION ALL SELECT 8, SDO_GEOMETRY(3007,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,1, 16,1003,1, 31,2003,1), SDO_ORDINATE_ARRAY(1, 2, 3, 11, 2, 13, 11, 22, 15, 1, 22, 7, 1, 2, 3, 1, 2, 3, 11, 2, 13, 11, 22, 15, 1, 22, 7, 1, 2, 3, 5, 6, 1, 8, 9, -1, 8, 6, 2, 5, 6, 1)) from dual
  UNION ALL SELECT 9, SDO_GEOMETRY(2003,4326,NULL, SDO_ELEM_INFO_ARRAY(1,1003,2), SDO_ORDINATE_ARRAY(1, 3, 3, 5, 4, 7, 7, 3, 1, 3)) from dual
  UNION ALL SELECT 10, SDO_GEOMETRY(2003, NULL, NULL, SDO_ELEM_INFO_ARRAY(1,1003,2, 11,2003,2), SDO_ORDINATE_ARRAY(1, 3, 3, 5, 4, 7, 7, 3, 1, 3, 3.1, 3.3, 3.3, 3.5, 3.4, 3.7, 3.7, 3.3, 3.1, 3.3)) from dual
  UNION ALL SELECT 11, SDO_GEOMETRY(2003, NULL, NULL, SDO_ELEM_INFO_ARRAY(1,1005,4, 1,2,1, 3,2,2, 11,2,1, 13,2,2), SDO_ORDINATE_ARRAY(-1, -5, 1, 2, 5, 4, 7, 2.2, 10, .1, 13, 4, 17, -6, 5, -7, -1, -5)) from dual
  UNION ALL SELECT 12, SDO_GEOMETRY(2007, NULL, NULL, SDO_ELEM_INFO_ARRAY(1,1003,2, 11,1003,2), SDO_ORDINATE_ARRAY(1, 3, 3, 5, 4, 7, 7, 3, 1, 3, 11, 3, 13, 5, 14, 7, 17, 3, 11, 3)) from dual
  UNION ALL SELECT 13, SDO_GEOMETRY(3003, 5698, NULL, SDO_ELEM_INFO_ARRAY(1, 1005, 4, 1, 2, 2, 7, 2, 1, 10, 2, 2, 22, 2, 1), SDO_ORDINATE_ARRAY(-1, -5, 1, 5, -7, 2, 17, -6, 3, 13, 4, 4, 10, .1, 5, 7, 2.2, 6, 5, 4, 7, 1, 2, 8, -1, -5, 1)) from dual
  UNION ALL SELECT 14, SDO_GEOMETRY(2007, 3857, NULL, SDO_ELEM_INFO_ARRAY(1, 1003, 1), SDO_ORDINATE_ARRAY(22, 22, 28, 22, 28, 26, 22, 26, 22, 22)) from dual
  UNION ALL SELECT 15, SDO_GEOMETRY(2007, 3857, NULL, SDO_ELEM_INFO_ARRAY(1, 1005, 2, 1, 2, 2, 5, 2, 1, 9, 1003, 2), SDO_ORDINATE_ARRAY(-1, -5, 5, -7, 17, -6, -1, -5, 1, 3, 7, 3, 4, 7, 3, 5, 1, 3)) from dual;

CREATE TABLE QGIS.DATE_TIMES ( "id" INTEGER PRIMARY KEY, "date_field" DATE, "datetime_field" TIMESTAMP );

INSERT INTO QGIS.DATE_TIMES ("id", "date_field", "datetime_field" ) VALUES (1, DATE '2004-03-04', TIMESTAMP '2004-03-04 13:41:52' );

CREATE TABLE QGIS.POINT_DATA_IDENTITY ( "pk" NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, GEOM SDO_GEOMETRY);
INSERT INTO QGIS.POINT_DATA_IDENTITY (GEOM)
 SELECT SDO_GEOMETRY( 2001,4326,SDO_POINT_TYPE(1, 2, NULL), NULL, NULL) from dual;

CREATE TABLE QGIS.GENERATED_COLUMNS ( "pk" INTEGER PRIMARY KEY, "generated_field" GENERATED ALWAYS AS ('test:' || "pk") VIRTUAL);
INSERT INTO QGIS.GENERATED_COLUMNS ("pk") SELECT 1 FROM dual;


COMMIT;
