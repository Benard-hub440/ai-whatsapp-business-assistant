
# AI WhatsApp Business Assistant

An AI-powered WhatsApp Business Assistant built with Python, Flask, Twilio, and Ollama.

The goal of this project is to build a production-ready assistant that can help different businesses automate customer interactions through WhatsApp while keeping the architecture modular and easy to scale.

Unlike a traditional chatbot that simply generates responses, this project is designed so that the AI understands customer requests while Python handles the business logic. This makes the application more reliable and easier to maintain.

---

## Project Goals

The long-term vision of this project is to create a platform that can serve multiple businesses from a single application.

The assistant should be able to:

* Answer customer questions.
* Understand customer intent.
* Process customer orders.
* Keep conversation history.
* Support multiple businesses.
* Store business data persistently.
* Scale from JSON storage to SQL databases.

---

## Current Features

* WhatsApp integration using Twilio
* Flask webhook
* Local AI using Ollama
* Multi-business support
* Product knowledge loaded from JSON
* Conversation history
* AI intent detection
* Customer order processing
* Product validation
* Order storage in JSON

---

## Technologies Used

* Python
* Flask
* Twilio WhatsApp API
* Ollama
* JSON
* Git & GitHub

Future plans include:

* SQLite
* MySQL/PostgreSQL
* Docker
* Dashboard for business owners

---

## Project Structure

```text
whatsapp-ai/
│
├── app.py
│
├── businesses/
│
├── products/
│
├── orders/
│
├── utils/
│   ├── ai.py
│   ├── loader.py
│   ├── memory.py
│   ├── orders.py
│   ├── prompts.py
│   └── validator.py
│
└── .env
```

---

## How the Application Works

1. A customer sends a WhatsApp message.
2. Twilio forwards the message to the Flask webhook.
3. The application identifies which business received the message.
4. The relevant products are loaded.
5. Previous conversation history is retrieved.
6. A prompt is built for the AI.
7. Ollama returns a structured JSON response.
8. Python validates the AI output.
9. If it's a valid order, the order is saved.
10. A reply is sent back to the customer through Twilio.

One design principle used throughout the project is:

> **AI understands language. Python controls the business.**

The AI is responsible for understanding what the customer wants, while Python verifies everything before any business action is performed.

---

## Design Principles

While building this project, I've tried to keep the code modular so that each component has a single responsibility.

Examples include:

* `loader.py` → Loads business and product data.
* `prompts.py` → Builds prompts for the AI.
* `ai.py` → Handles communication with Ollama.
* `orders.py` → Stores customer orders.
* `validator.py` → Validates business rules.

This makes the project easier to debug, extend, and eventually migrate to a database.

---

## Example AI Response

The AI always returns structured JSON.

```json
{
    "intent": "order",
    "reply": "I've noted your order.",
    "product": "512GB SSD",
    "quantity": 2
}
```

Python then decides what to do with that information.

---

## Current Development Status

The project is still under active development.

Completed:

* WhatsApp webhook
* AI integration
* Conversation memory
* Multi-business support
* Product loading
* Order processing
* Product validation

Currently working on:

* Better intent routing
* Smarter product matching
* Inventory management
* Database migration

---

## Future Improvements

Some features I plan to add include:

* SQLite database
* MySQL/PostgreSQL support
* Inventory tracking
* Customer order history
* Business dashboard
* Authentication
* Analytics
* Docker deployment
* REST API
* Admin portal

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/Benard-hub440/ai-whatsapp-business-assistant.git
```

Navigate into the project:

```bash
cd whatsapp-ai
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your environment variables.

Start the Flask application:

```bash
python app.py
```

Make sure you have:

* Ollama running locally.
* A supported model installed (for example, `qwen2.5:1.5b`).
* Twilio configured to point to your Flask webhook.

---

## Why I Built This Project

I started this project to learn how modern AI systems are built beyond simple chatbots.

The main focus has been understanding how to combine large language models with traditional software engineering principles. Rather than letting the AI make every decision, I wanted to build a system where AI handles natural language understanding while Python manages business rules, validation, and data storage.

As the project grows, my goal is to turn it into a reusable platform that can be adapted for different businesses with minimal changes.

---

## License

This project is for learning, experimentation, and portfolio purposes.
