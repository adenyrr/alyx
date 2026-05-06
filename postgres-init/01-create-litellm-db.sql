-- Créé automatiquement au premier démarrage de postgres.
-- Crée la base "litellm" et accorde tous les droits à l'utilisateur principal.
-- Le script n'est exécuté qu'une seule fois (si le volume postgres_data est vierge).

CREATE DATABASE IF NOT EXISTS litellm;
ALTER DATABASE litellm OWNER TO :"POSTGRES_USER";
GRANT ALL PRIVILEGES ON DATABASE litellm TO :"POSTGRES_USER";
