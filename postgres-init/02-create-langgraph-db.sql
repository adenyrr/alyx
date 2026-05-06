-- Créé automatiquement au premier démarrage de postgres.
-- Crée la base "langgraph" pour les checkpoints LangGraph (persistance état multi-tours).
-- Le script n'est exécuté qu'une seule fois (si le volume postgres_data est vierge).

CREATE DATABASE IF NOT EXISTS langgraph;
ALTER DATABASE langgraph OWNER TO :"POSTGRES_USER";
GRANT ALL PRIVILEGES ON DATABASE langgraph TO :"POSTGRES_USER";
