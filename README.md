# 🚀 Multi-Client WhatsApp AI SaaS Dashboard

An advanced, production-ready WhatsApp Automation SaaS platform designed for multiple clients. This system allows businesses to plug in their own WhatsApp instances (Evolution-API / Baileys) and custom Gemini AI prompts to run autonomous customer support bots.

---

## 🔥 Key Features
- **Multi-Client Architecture:** A single central database handling independent clients seamlessly.
- **Zero-Overhead & Free Tier Ready:** Uses open-source API connectors with no artificial chat limits.
- **Dynamic Context Routing:** Automatically maps incoming webhooks to the correct client's configuration and Gemini system instructions.
- **Custom AI Personas:** Every business owner can define their own bot's logic and behavioral prompt.

---

## 🛠️ Database Setup
The system uses an optimized SQLite relational schema tracking client profiles and their active API tokens dynamically.

### Run the Initialization Script:
```bash
python init_db.py
