-- Créé automatiquement au premier démarrage de postgres.
-- Crée la base "litellm" et accorde tous les droits à l'utilisateur principal.
-- Le script n'est exécuté qu'une seule fois (si le volume postgres_data est vierge).

DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'litellm') THEN
    CREATE DATABASE litellm;
  END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE litellm TO :"POSTGRES_USER";
