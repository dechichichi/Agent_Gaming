CREATE TABLE `model` (
                     `uid`     VARCHAR(255) NOT NULL,
                     `event_list` LONGTEXT NOT NULL,
                     `target`    FLOAT,
                     `other_feature`   FLOAT,
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;