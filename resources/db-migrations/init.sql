DROP TABLE IF EXISTS user_answers;
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS questions;

CREATE TABLE questions (
    question_id INT(11) NOT NULL AUTO_INCREMENT,
    question_text VARCHAR(500) NOT NULL,
    PRIMARY KEY (question_id)
);

CREATE TABLE options (
    option_id INT(11) NOT NULL AUTO_INCREMENT,
    question_id INT(11) NOT NULL,
    option_text VARCHAR(300) NOT NULL,
    additional_id INT(11) NOT NULL,
    PRIMARY KEY (option_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

CREATE TABLE user_answer (
    answer_id INT(11) NOT NULL AUTO_INCREMENT,
    user_id INT(11) NOT NULL,
    question_id INT(11) NOT NULL,
    chosen_option_id INT(11) NOT NULL,
    PRIMARY KEY (answer_id),
    UNIQUE (user_id, question_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id),
    FOREIGN KEY (chosen_option_id) REFERENCES options(option_id)
);