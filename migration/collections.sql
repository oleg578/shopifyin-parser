DROP TABLE IF EXISTS `collections`;
CREATE TABLE `collections`
(
    `id`               VARCHAR(16)  NOT NULL,
    `site`             VARCHAR(100) NOT NULL,
    `handle`           VARCHAR(255) DEFAULT '',
    `title`            VARCHAR(255) DEFAULT '',
    `image_width`      INT UNSIGNED DEFAULT NULL,
    `image_height`     INT UNSIGNED DEFAULT NULL,
    `image_alt_text`   VARCHAR(255) DEFAULT '',
    `top_row`          BOOLEAN      DEFAULT FALSE,
    `product_id`       VARCHAR(16)  DEFAULT NULL,
    `product_handle`   VARCHAR(255) DEFAULT '',
    `product_position` INT UNSIGNED DEFAULT NULL,
    `products_count`   INT UNSIGNED DEFAULT NULL,
    `date_added`       DATETIME     DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`, `site`, `product_id`)
) engine = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;