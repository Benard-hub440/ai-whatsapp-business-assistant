# ==========================================
# Imports
# ==========================================
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse

from utils.loader import load_products, find_business
from utils.memory import store_message, get_history
from utils.prompts import build_messages
from utils.ai import ask_ai
from utils.orders import save_order
from utils.validator import find_product

# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)

model = "input more powerfull model from ollama"


# ==========================================
# WhatsApp Webhook
# ==========================================

@app.route("/whatsapp", methods=["POST"])
def whatsapp():

    try:

        # --------------------------------------
        # Customer Information
        # --------------------------------------
        phone = request.form.get("From")
        business_phone = request.form.get("To")
        message = request.form.get("Body", "").strip()

        print("=" * 60)
        print("FROM :", phone)
        print("TO   :", business_phone)
        print("MSG  :", message)

        # --------------------------------------
        # Find Business
        # --------------------------------------
        business = find_business(business_phone)

        if business is None:

            resp = MessagingResponse()
            resp.message(
                "Sorry, this business is not registered."
            )

            return Response(
                str(resp),
                mimetype="text/xml"
            )

        # --------------------------------------
        # Load Products
        # --------------------------------------
        products = load_products(
            business["product_file"]
        )

        # --------------------------------------
        # Save Customer Message
        # --------------------------------------
        store_message(
            phone,
            "user",
            message
        )

        # --------------------------------------
        # Conversation History
        # --------------------------------------
        history = get_history(phone)

        # --------------------------------------
        # Build AI Prompt
        # --------------------------------------
        messages = build_messages(
            business,
            products,
            history
        )

        # --------------------------------------
        # Ask AI
        # --------------------------------------
        ai_response = ask_ai(
            model=model,
            messages=messages
        )

        print("=" * 60)
        print("AI RESPONSE")
        print(ai_response)
        print("=" * 60)

        intent = ai_response.get("intent", "unknown")
        reply = ai_response.get(
            "reply",
            "Sorry, I couldn't process your request."
        )

        product_name = ai_response.get(
            "product",
            ""
        ).strip()

        quantity = ai_response.get(
            "quantity",
            0
        )

        print("DEBUG")
        print(f"Intent       : {intent}")
        print(f"Product Name : {product_name}")
        print(f"Quantity     : {quantity}")
        print("=" * 60)

        # --------------------------------------
        # Process Orders
        # --------------------------------------
        if intent == "order":

            print("✅ ORDER INTENT DETECTED")

            if quantity <= 0:
                quantity = 1

            if not product_name:

                print("❌ AI DID NOT RETURN A PRODUCT")

                reply = (
                    "Sorry, I couldn't determine "
                    "which product you want to order."
                )

            else:

                print("Searching product...")
                print(product_name)

                product = find_product(
                    products,
                    product_name
                )

                print("RESULT FROM find_product()")
                print(product)

                if product is None:

                    print("❌ PRODUCT NOT FOUND")

                    reply = (
                        f"Sorry, we don't stock "
                        f"'{product_name}'."
                    )

                elif not product["available"]:

                    print("❌ PRODUCT NOT AVAILABLE")

                    reply = (
                        f"Sorry, {product['name']} "
                        f"is currently unavailable."
                    )

                elif quantity > product["stock"]:

                    print("❌ NOT ENOUGH STOCK")

                    reply = (
                        f"Sorry, we only have "
                        f"{product['stock']} "
                        f"{product['unit']}(s) available."
                    )

                else:

                    print("✅ PRODUCT FOUND")
                    print("CALLING save_order()...")

                    order = save_order(
                        filename=business["orders_file"],
                        customer=phone,
                        product=product,
                        quantity=quantity
                    )

                    print("RETURNED FROM save_order()")
                    print(order)

                    reply = (
                        f"{reply}\n\n"
                        f"✅ Order Number: #{order['order_id']}\n"
                        f"📦 Product: {order['product']}\n"
                        f"🔢 Quantity: {order['quantity']} {order['unit']}(s)\n"
                        f"💰 Unit Price: "
                        f"{order['currency']} "
                        f"{order['unit_price']}\n"
                        f"💵 Total: "
                        f"{order['currency']} "
                        f"{order['total_price']}\n"
                        f"📌 Status: {order['status']}"
                    )

        else:

            print("ℹ️ REQUEST IS NOT AN ORDER")
        # --------------------------------------
        # Save Assistant Reply
        # --------------------------------------
        store_message(
            phone,
            "assistant",
            reply
        )

        print("=" * 60)
        print("FINAL REPLY")
        print(reply)
        print("=" * 60)

        # --------------------------------------
        # Send WhatsApp Reply
        # --------------------------------------
        resp = MessagingResponse()
        resp.message(reply)

        return Response(
            str(resp),
            mimetype="text/xml"
        )

    except Exception as e:

        print("=" * 60)
        print("APPLICATION ERROR")
        print(e)
        print("=" * 60)

        resp = MessagingResponse()
        resp.message(
            "Sorry, something went wrong. Please try again."
        )

        return Response(
            str(resp),
            mimetype="text/xml"
        )


# ==========================================
# Run Flask
# ==========================================

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )