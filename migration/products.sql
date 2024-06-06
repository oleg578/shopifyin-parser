DROP TABLE IF EXISTS products;
CREATE TABLE products
(
    `id`          VARCHAR(16)  NOT NULL,
    `site`        VARCHAR(100) NOT NULL,
    `handle`      VARCHAR(255)  DEFAULT '',
    `url`         VARCHAR(1024) DEFAULT '',
    `variant_id`  VARCHAR(16)   DEFAULT '',
    `variant_sku` VARCHAR(100)  DEFAULT '',
    `date_added`  DATETIME      DEFAULT '0000-00-00 00:00:00',
    PRIMARY KEY (`id`, `site`, `variant_id`)
) engine = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;