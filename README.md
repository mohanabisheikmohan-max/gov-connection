# GovConnect AI — Government Citizen Chatbot

A modern government-information chatbot interface with a persistent department
sidebar. Citizens select a department and ask questions in the chat panel.

## Main UI
- Chatbot-style interface
- Department sidebar always visible on desktop
- Department selection
- Department information panel
- Latest update panel
- Responsive/mobile UI
- Animated cards and chat bubbles
- Gemini integration through Python Flask

## Gemini
The project is configured to use:

GEMINI_MODEL=gemini-3.6-flash

The model name is intentionally stored in `.env` so it can be changed without
rewriting the application if the Gemini API exposes a different/current model ID.

## Live government updates
The current package includes the architecture and demo update records. For production,
connect only permitted official APIs, RSS/open-data feeds, or government webpages,
respecting their access rules. Store source URL, published date, checked date and
verification status for every update.

## Important
This is a citizen-information software project and is NOT an official government website.
Do not publish unverified government information as official information.
