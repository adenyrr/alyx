-- Créé automatiquement au premier démarrage de postgres.
-- Crée la base "langgraph" pour les checkpoints LangGraph (persistance état multi-tours).
-- Le script n'est exécuté qu'une seule fois (si le volume postgres_data est vierge).

\c postgres

SELECT 'CREATE DATABASE langgraph'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'langgraph')\gexec

GRANT ALL PRIVILEGES ON DATABASE langgraph TO :"POSTGRES_USER";
