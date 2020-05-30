
table_dict = {}
table_dict["$AGHTD"] = "autopilothtd"
table_dict["$TIROT"] = "rot"
table_dict["$IIHRM"] = "inclineshrm"
table_dict["$WIMWV"] = "wi_anemoclinmwv"
table_dict["$GPRMC"] = "gpsrmc"

create_table_sql = {}
create_table_sql["$AGHTD"] = "autopilothtd"
create_table_sql["$TIROT"] = "rot"
create_table_sql["$IIHRM"] = "inclineshrm"
create_table_sql["$WIMWV"] = "wi_anemoclinmwv"

create_table_sql["$GPRMC"] = '''CREATE TABLE if not exists  `gpsrmc` (
  `SAMPLE_TIMESTAMP` datetime NOT NULL,
  `RMC_LOCATION_STATUS` varchar(1) DEFAULT NULL COMMENT '定位状态，A=有效定位，V=无效定位',
  `RMC_LATITUDE` decimal(9,4) DEFAULT NULL COMMENT '纬度',
  `RMC_LATITUDE_HEMISPHERE` varchar(1) DEFAULT NULL COMMENT '纬度半球N(北半球)或S(南半球)',
  `RMC_LONGITUDE` decimal(9,4) DEFAULT NULL COMMENT '经度',
  `RMC_LONGITUDE_HEMISPHERE` varchar(1) DEFAULT NULL COMMENT '经度半球E(东经)或W(西经)',
  `RMC_GROUND_SPEED` decimal(9,4) DEFAULT NULL COMMENT '对地航速',
  `RMC_GROUND_WEEK` varchar(6) DEFAULT NULL COMMENT '对地航向(以真北为参考基准)',
  `RMC_DATE` varchar(6) DEFAULT NULL COMMENT 'Date: ddmmyy',
  `RMC_DECLINATION` decimal(8,2) DEFAULT NULL COMMENT '磁偏角',
  `RMC_DECLINATION_DIRECTION` varchar(1) DEFAULT NULL COMMENT '磁偏角方向，E(东)或W(西)',
  `RMC_MODE_INDICATOR` varchar(6) DEFAULT NULL COMMENT 'Mode Indicator',
  `RMC_NAVIGATION_STATUS` varchar(6) DEFAULT NULL COMMENT 'Navigational status',
  PRIMARY KEY (`SAMPLE_TIMESTAMP`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='RMC来自于全球定位系统接收机';'''