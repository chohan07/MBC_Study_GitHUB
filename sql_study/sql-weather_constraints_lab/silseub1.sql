USE weather_constraints_lab;

-- 1. app_user 테이블 생성 (PK, UNIQUE, CHECK, NOT NULL)
CREATE TABLE IF NOT EXISTS app_user (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'REPORTER',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_user_email UNIQUE (email),
    CONSTRAINT chk_username CHECK (CHAR_LENGTH(TRIM(username)) > 0),
    CONSTRAINT chk_user_email CHECK (email LIKE '%@%.%'),
    CONSTRAINT chk_user_role CHECK (role IN ('REPORTER', 'ADMIN', 'READER'))
) ENGINE=InnoDB;

-- 2. 기존 news_article 테이블에 user_id 외래키(FK) 추가
ALTER TABLE news_article
ADD COLUMN user_id BIGINT NULL,
ADD CONSTRAINT fk_article_user FOREIGN KEY (user_id)
    REFERENCES app_user(user_id) ON DELETE SET NULL;

-- 3. 초기 사용자(기자) 데이터 입력
INSERT INTO app_user (email, username, role) VALUES
('reporter1@news.com', '김기자', 'REPORTER'),
('reporter2@news.com', '박기자', 'REPORTER'),
('admin@news.com', '관리자', 'ADMIN');

-- 4. 기존 기사에 작성자(user_id) 매핑
UPDATE news_article SET user_id = 1 WHERE article_id IN (1, 2);
UPDATE news_article SET user_id = 2 WHERE article_id = 3;

-- 5. 작성자 + 기사 + 날씨관측값 조인 조회
SELECT 
    a.article_id,
    a.title,
    u.username AS author,
    u.role,
    w.region_name,
    w.temperature,
    w.observed_at
FROM news_article a
LEFT JOIN app_user u ON a.user_id = u.user_id
LEFT JOIN weather_observation w ON a.weather_id = w.weather_id
ORDER BY a.article_id;