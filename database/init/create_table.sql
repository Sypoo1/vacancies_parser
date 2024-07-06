CREATE TABLE IF NOT EXISTS vacancies (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id BIGINT NOT NULL,
    name VARCHAR(1000) NOT NULL,
    url VARCHAR(1000) NOT NULL,
    salary_currency CHAR(10),
    salary_from INTEGER,
    salary_to INTEGER,
    salary_gross BOOLEAN,
    area VARCHAR(1000)
);