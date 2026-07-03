def parse_request(request):

    customer_phone = request.form.get("From")
    business_phone = request.form.get("To")
    message = request.form.get("Body")

    return customer_phone, business_phone, message