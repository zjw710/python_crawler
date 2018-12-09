/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1_3306
Source Server Version : 50553
Source Host           : 127.0.0.1:3306
Source Database       : pycrawler

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2018-12-09 13:14:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ganjiphone
-- ----------------------------
DROP TABLE IF EXISTS `ganjiphone`;
CREATE TABLE `ganjiphone` (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `phone` varchar(255) DEFAULT NULL COMMENT '手机号',
  `type` tinyint(1) DEFAULT '1' COMMENT '1.二手房',
  `name` varchar(255) DEFAULT NULL COMMENT '姓名 ',
  `company` varchar(255) DEFAULT NULL COMMENT '公司名',
  `area` varchar(255) DEFAULT NULL COMMENT '地区简称,如广州为gz',
  `com_desc` varchar(255) DEFAULT NULL COMMENT '公司描述',
  `status` tinyint(1) DEFAULT '2' COMMENT '1.已采集标记 2.未采集标记',
  `pm_result` text,
  `ctime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`p_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1181 DEFAULT CHARSET=utf8;
