USE IFPEBPT;

CREATE TABLE IF NOT EXISTS paciente (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    pre_hematocrit FLOAT NOT NULL,
    pre_hemoglobin FLOAT NOT NULL,
    pre_lactate FLOAT NOT NULL,
    height FLOAT NOT NULL,
    redo TINYINT NOT NULL,
    cpb FLOAT NOT NULL, 
    anoxia FLOAT NOT NULL,
    female TINYINT NOT NULL,
    normothermia TINYINT NOT NULL,
    age INT,
    hb FLOAT,
    probability FLOAT,
    prediction FLOAT
);
