-- Bancos auxiliares do Lab 2 (executado uma unica vez na criacao do volume)
CREATE DATABASE langfuse;
CREATE DATABASE langflow;
-- Extensao pgvector no banco de RAG
\c techpix
CREATE EXTENSION IF NOT EXISTS vector;
