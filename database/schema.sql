-- SnapGram - Mini Instagram Database Schema
-- MySQL 8.0+
-- Run: mysql -u root -p < database/schema.sql

CREATE DATABASE IF NOT EXISTS snapgram_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE snapgram_db;

-- Users (managed by Django's auth system, shown for reference)
-- Django creates this automatically via migrations

-- User Profiles
CREATE TABLE IF NOT EXISTS core_profile (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    bio TEXT,
    avatar VARCHAR(255),
    website VARCHAR(200),
    location VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Posts
CREATE TABLE IF NOT EXISTS core_post (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    author_id INT NOT NULL,
    image VARCHAR(255) NOT NULL,
    caption TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    INDEX idx_author (author_id),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Comments
CREATE TABLE IF NOT EXISTS core_comment (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    post_id BIGINT UNSIGNED NOT NULL,
    author_id INT NOT NULL,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES core_post(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    INDEX idx_post (post_id),
    INDEX idx_author (author_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Likes
CREATE TABLE IF NOT EXISTS core_like (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    post_id BIGINT UNSIGNED NOT NULL,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES core_post(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_post_user (post_id, user_id),
    INDEX idx_post (post_id),
    INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Follows
CREATE TABLE IF NOT EXISTS core_follow (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    follower_id INT NOT NULL,
    following_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (follower_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (following_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_follow (follower_id, following_id),
    INDEX idx_follower (follower_id),
    INDEX idx_following (following_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Stories
CREATE TABLE IF NOT EXISTS core_story (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    author_id INT NOT NULL,
    image VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    INDEX idx_author_created (author_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Useful views
CREATE OR REPLACE VIEW post_stats AS
SELECT
    p.id AS post_id,
    p.author_id,
    p.caption,
    p.created_at,
    COUNT(DISTINCT l.id) AS likes_count,
    COUNT(DISTINCT c.id) AS comments_count
FROM core_post p
LEFT JOIN core_like l ON l.post_id = p.id
LEFT JOIN core_comment c ON c.post_id = p.id
GROUP BY p.id;

SELECT 'SnapGram database schema created successfully!' AS status;
