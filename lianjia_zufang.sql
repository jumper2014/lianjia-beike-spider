# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.21)
# Database: lianjia
# Generation Time: 2018-03-31 12:54:33 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table xiaoqu
# ------------------------------------------------------------


DROP TABLE IF EXISTS `zufang`;

CREATE TABLE `zufang` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `update_date` varchar(10) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,  -- 区县
  `area` varchar(50) DEFAULT NULL,      -- 区域
  `xiaoqu` varchar(100) DEFAULT NULL,  -- 小区
  `layout` varchar(100) DEFAULT NULL,   -- 布局
  `price` int(11) DEFAULT NULL,
  `title` varchar(150) DEFAULT NULL,
  `page_url` varchar(300) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,       -- 平方米
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
