create table QA
(
    id       int auto_increment
        primary key,
    Question varchar(65535) null,
    Answer   varchar(255) null
);

INSERT INTO QA.QA (id, Question, Answer) VALUES (1, 'Hello', 'Fine');
INSERT INTO QA.QA (id, Question, Answer) VALUES (4, 'Hello', 'A_Chorus_Line');
INSERT INTO QA.QA (id, Question, Answer) VALUES (5, 'Here', 'Hot_Springs,_Arkansas');