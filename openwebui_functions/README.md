# Fonctions natives Open WebUI

Ce dossier contient des **Functions natives Open WebUI** — distinctes du pipeline
Alyx hébergé dans le conteneur `pipelines`. Elles doivent être installées
manuellement côté Open WebUI car elles utilisent des events interactifs
(`input`, `confirmation`, `execute`) qui nécessitent le WebSocket bidirectionnel
du mode natif, indisponible pour un pipeline externe.

## Installation

1. Open WebUI → **Admin Panel → Functions → +** (Create New Function).
2. Coller le contenu du fichier `.py`.
3. Enregistrer, puis **activer** la fonction.
4. Pour une Action : elle apparaît comme bouton dans la barre d'outils des
   messages. Régler éventuellement ses *Valves* dans la fiche de la fonction.

## Fichiers

- [`alyx_actions.py`](alyx_actions.py) — **Action** : bouton « ✨ Alyx » sous chaque
  message. Au clic, ouvre une boîte de saisie proposant des opérations de suivi
  (`approfondir`, `resumer`, `exporter`, `artifact`, `presentation`) ou une
  consigne libre, puis resoumet automatiquement la consigne à Alyx.

  > Le pont de resoumission repose sur `window.parent.postMessage({type:'input:prompt:submit', …})`,
  > le même mécanisme que celui documenté pour les embeds rich-UI. À vérifier selon
  > la version d'Open WebUI ; en cas d'évolution du frontend, adapter le payload `execute`.
