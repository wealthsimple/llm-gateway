-- SQL to initialize local db

CREATE TABLE openai_requests(
    id serial primary key,
    user_input VARCHAR,
    user_email VARCHAR,
    openai_response JSON,
    openai_model VARCHAR,
    temperature FLOAT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    openai_endpoint VARCHAR
);

CREATE TABLE cohere_requests(
    id serial primary key,
    user_input VARCHAR,
    user_email VARCHAR,
    cohere_response JSON,
    cohere_model VARCHAR,
    temperature FLOAT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    cohere_endpoint VARCHAR
);

CREATE TABLE awsbedrock_requests(
    id serial primary key,
    user_input VARCHAR,
    user_email VARCHAR,
    awsbedrock_response JSON,
    awsbedrock_model VARCHAR,
    temperature FLOAT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    awsbedrock_endpoint VARCHAR
    extras JSON
);
