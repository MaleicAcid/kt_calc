
table_dict = {}
table_dict["$AGHTD"] = "autopilothtd"
table_dict["$TIROT"] = "rot"
table_dict["$IIHRM"] = "inclineshrm"
table_dict["$WIMWV"] = "wi_anemoclinmwv"
table_dict["$GPRMC"] = "gpsrmc"

create_table_sql = {}
create_table_sql["$AGHTD"] = '''CREATE TABLE if not exists `autopilothtd` (
  `SAMPLE_TIMESTAMP` datetime NOT NULL,
  `HTD_COVER` varchar(1) DEFAULT NULL COMMENT '覆盖，A=使用，V=不使用',
  `HTD_RUDDER_COMMAND` decimal(6,2) DEFAULT NULL COMMENT '舵角命令（度）',
  `HTD_DIRECTION_COMMAND` varchar(1) DEFAULT NULL COMMENT '舵方向命令，L/R=左舷/右舷',
  `HTD_CHOICE_DRIVE_MODL` varchar(4) DEFAULT NULL COMMENT '选择的驾驶模式',
  `HTD_TURN_MODL` varchar(1) DEFAULT NULL COMMENT '转向模式：R=半径受控,T=转向率受控，N=转向不受控；',
  `HTD_RUDDER_LIMIT_COMMAND` decimal(6,2) DEFAULT NULL COMMENT '舵限制命令（度）；',
  `HTD_RUDDER_DEVIATE_COMMAND` decimal(6,2) DEFAULT NULL COMMENT '航向偏离限制命令（度）；',
  `HTD_RADIUS_COMMAND` decimal(6,2) unsigned DEFAULT NULL COMMENT '航向改变时的转弯半径命令（海里）',
  `HTD_TURN_RATE_COMMAND` decimal(6,2) DEFAULT NULL COMMENT '航向改变时的转向率命令（度/英里）',
  `HTD_RUDDER_ORDER` decimal(6,2) DEFAULT NULL COMMENT '舵令（度）',
  `HTD_DEVIATON_LIMIT_COMMAND` decimal(6,2) DEFAULT NULL COMMENT '航迹偏离限制命令（海里）',
  `HTD_TRACKS_COMMAND` varchar(8) DEFAULT NULL COMMENT '航迹命令',
  `HTD_REFERNCE_COURSE` varchar(1) DEFAULT NULL COMMENT '在使用的参考航向，T/M；',
  `HTD_RUDDER_STATUS` varchar(1) DEFAULT NULL COMMENT '舵的状态，A=在限制里，V=在限制外',
  `HTD_COURSE_STATUS` varchar(1) DEFAULT NULL COMMENT '航向偏离状态，A=在限制里，V=在限制外',
  `HTD_TRACKS_STATUS` varchar(1) DEFAULT NULL COMMENT '航迹偏离状态，A=在限制里，V=在限制外',
  `HTD_COURSE` decimal(6,2) DEFAULT NULL COMMENT '航向（度）',
  PRIMARY KEY (`SAMPLE_TIMESTAMP`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='轨迹控制数据表';'''
create_table_sql["$TIROT"] = '''CREATE TABLE if not exists `rot` (
  `SAMPLE_TIMESTAMP` datetime NOT NULL,
  `ROT` decimal(6,2) DEFAULT NULL COMMENT 'Rate of turn, degrees/minute, "-" = bow turns to port',
  `SATAUS` varchar(1) DEFAULT NULL COMMENT 'Status  A = Data valid\r\nV = Data invalid',
  PRIMARY KEY (`SAMPLE_TIMESTAMP`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='轨迹控制数据表';'''
create_table_sql["$IIHRM"] = '''CREATE TABLE if not exists `inclineshrm` (
  `SAMPLE_TIMESTAMP` datetime NOT NULL,
  `HRM_LONGITUDINAL_HORN` decimal(6,2) DEFAULT NULL COMMENT '横倾角，“-”=左舷',
  `HRM_LONGITUDINAL_CYCLE` decimal(6,2) DEFAULT NULL COMMENT '横摇周期，秒',
  `HRM_LEFT_AMPLITUDE` decimal(6,2) DEFAULT NULL COMMENT '左舷摇摆振幅，度',
  `HRM_RIGHT_AMPLITUDE` decimal(6,2) DEFAULT NULL COMMENT '右舷摇摆振幅，度',
  `HRM_STATUS` varchar(1) DEFAULT NULL COMMENT '状态指示，A=数据有效，V=数据无效',
  `HRM_SWING_PEAK_LEFT` decimal(6,2) DEFAULT NULL COMMENT '摇摆峰值，船艏，度',
  `HRM_SWING_PEAK_RIGHT` decimal(6,2) DEFAULT NULL COMMENT '摇摆峰值，船艉，度',
  `HRM_PEAK_TIMESTAMP` decimal(8,2) DEFAULT NULL COMMENT '峰值重置时间',
  `HRM_PEAK_DAY` decimal(6,2) DEFAULT NULL COMMENT '峰值重置日，1-31',
  `HRM_PEAK_MONTH` decimal(6,2) DEFAULT NULL COMMENT '峰值重置月份，1-12',
  PRIMARY KEY (`SAMPLE_TIMESTAMP`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='HRM 纵倾角、纵摇周期和振幅表';'''

create_table_sql["$WIMWV"] = '''CREATE TABLE if not exists `wi_anemoclinmwv` (
  `SAMPLE_TIMESTAMP` datetime NOT NULL,
  `MWV_DIRECTION` decimal(6,2) DEFAULT NULL COMMENT '风向，0-360 度',
  `MWV_REFERENCE` varchar(1) DEFAULT NULL COMMENT '参照， R = 相对， T =绝对；',
  `MWV_WIND_SPEED` decimal(6,2) DEFAULT NULL COMMENT '风速；',
  `MWV_WIND_SPEED_UNIT` varchar(5) DEFAULT NULL COMMENT '风速单位， K=KM/H （千米/时） M=M/S （米/秒） N=KNOTS（节）',
  `MWV_STATUS` varchar(1) DEFAULT NULL COMMENT '状态，A = 数据有效 V=数据无效',
  PRIMARY KEY (`SAMPLE_TIMESTAMP`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='风速风向仪语句MWV风速风向测量语句';'''

create_table_sql["$GPRMC"] = '''CREATE TABLE if not exists `gpsrmc` (
  `SAMPLE_TIMESTAMP` datetime NOT NULL,
  `RMC_UTX_POS_FIX` decimal(8,3) DEFAULT NULL COMMENT 'UTC of position fix',
  `RMC_LOCATION_STATUS` varchar(1) DEFAULT NULL COMMENT '定位状态，A=有效定位，V=无效定位',
  `RMC_LATITUDE` decimal(12,4) DEFAULT NULL COMMENT '纬度',
  `RMC_LATITUDE_HEMISPHERE` varchar(1) DEFAULT NULL COMMENT '纬度半球N(北半球)或S(南半球)',
  `RMC_LONGITUDE` decimal(12,4) DEFAULT NULL COMMENT '经度',
  `RMC_LONGITUDE_HEMISPHERE` varchar(1) DEFAULT NULL COMMENT '经度半球E(东经)或W(西经)',
  `RMC_GROUND_SPEED` decimal(12,4) DEFAULT NULL COMMENT '对地航速',
  `RMC_GROUND_WEEK` varchar(6) DEFAULT NULL COMMENT '对地航向(以真北为参考基准)',
  `RMC_DATE` varchar(6) DEFAULT NULL COMMENT 'Date: ddmmyy',
  `RMC_DECLINATION` decimal(12,4) DEFAULT NULL COMMENT '磁偏角',
  `RMC_DECLINATION_DIRECTION` varchar(1) DEFAULT NULL COMMENT '磁偏角方向，E(东)或W(西)',
  `RMC_NAVIGATION_STATUS` varchar(1) DEFAULT NULL COMMENT 'Navigational status',
  PRIMARY KEY (`SAMPLE_TIMESTAMP`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='RMC来自于全球定位系统接收机';'''