import json
import ollama


# ==========================================
# Default Error Response
# ==========================================

def error_response():

    return {
        "intent": "unknown",
        "reply": (
            "Sorry, I encountered an internal error. "
            "Please try again."
        ),
        "product": "",
        "quantity": 0
    }


# ==========================================
# Ask AI
# ==========================================

def ask_ai(model, messages):

    try:

        response = ollama.chat(
            model=model,
            messages=messages
        )

        raw_reply = response["message"]["content"]

        print("=" * 60)
        print("RAW AI RESPONSE")
        print(raw_reply)
        print("=" * 60)

        # --------------------------------------
        # Remove Markdown Code Blocks
        # --------------------------------------

        cleaned = (
            raw_reply
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # --------------------------------------
        # Extract JSON if extra text exists
        # --------------------------------------

        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start != -1 and end != -1:

            cleaned = cleaned[start:end + 1]

        print("=" * 60)
        print("CLEANED RESPONSE")
        print(cleaned)
        print("=" * 60)

        # --------------------------------------
        # Parse JSON
        # --------------------------------------

        data = json.loads(cleaned)

        try:
            quantity = int(data.get("quantity", 0))
        except (TypeError, ValueError):
            quantity = 0

        return {

            "intent": data.get(
                "intent",
                "unknown"
            ),

            "reply": data.get(
                "reply",
                ""
            ),

            "product": data.get(
                "product",
                ""
            ),

            "quantity": quantity
        }

    # --------------------------------------
    # AI Returned Plain Text
    # --------------------------------------

    except json.JSONDecodeError:

        print("=" * 60)
        print("WARNING")
        print("AI returned plain text instead of JSON.")
        print("=" * 60)

        return {

            "intent": "question",

            "reply": raw_reply,

            "product": "",

            "quantity": 0
        }

    # --------------------------------------
    # Ollama Error
    # --------------------------------------

    except Exception as e:

        print("=" * 60)
        print("OLLAMA ERROR")
        print(e)
        print("=" * 60)

        return error_response()