DROP TABLE IF EXISTS `metafields`;
CREATE TABLE `metafields`
(
    `id`              VARCHAR(16) NOT NULL,
    `site`            VARCHAR(100) NOT NULL,
    `handle`          VARCHAR(255) DEFAULT '',
    `metafield_name`  VARCHAR(255) DEFAULT '',
    `metafield_value` TEXT         DEFAULT '',
    `date_added`      DATETIME     DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`, `site`, `metafield_name`)
) engine = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;