import os
from dotenv import load_dotenv

load_dotenv()


class CommunicationAgent:
    """
    ReviveAI Agent 3

    Generates personalized customer recovery
    communication based on:
    - Customer segment
    - Failure type
    - Recovery strategy
    - Transaction value
    """

    def __init__(self):
        self.gemini_available = False
        self.model = None

        # Gemini is optional.
        # The application works without it.

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            try:
                import google.generativeai as genai

                genai.configure(
                    api_key=api_key
                )

                self.model = genai.GenerativeModel(
                    "gemini-1.5-flash"
                )

                self.gemini_available = True

            except Exception:
                self.gemini_available = False

    # ========================================================
    # CUSTOMER TONE
    # ========================================================

    def get_customer_tone(self, segment):

        tones = {
            "premium":
                "professional, personalized and concierge-style",

            "regular":
                "friendly, professional and concise",

            "new":
                "welcoming, reassuring and helpful",

            "at_risk":
                "empathetic, supportive and non-aggressive"
        }

        return tones.get(
            segment,
            "professional and friendly"
        )

    # ========================================================
    # FAILURE EXPLANATION
    # ========================================================

    def get_failure_message(self, failure_type):

        messages = {

            "card_declined":
                "Your card issuer declined the payment.",

            "insufficient_funds":
                "There may not be enough available balance "
                "to complete the payment.",

            "expired_card":
                "The payment method appears to be expired.",

            "gateway_error":
                "We experienced a temporary payment "
                "processing issue.",

            "authentication_failed":
                "The payment could not be authenticated.",

            "network_error":
                "A temporary connection issue interrupted "
                "the payment."
        }

        return messages.get(
            failure_type,
            "We were unable to complete your payment."
        )

    # ========================================================
    # CTA
    # ========================================================

    def get_cta(self, strategy):

        ctas = {

            "smart_retry":
                "Please try the payment again in a few moments.",

            "customer_outreach":
                "Please review your payment details and "
                "complete the payment.",

            "alternative_payment":
                "Please try another available payment method.",

            "payment_plan":
                "Please review the available payment options.",

            "discount_offer":
                "Use the available offer to complete your purchase.",

            "human_escalation":
                "Our support team will assist you with completing "
                "your payment."
        }

        return ctas.get(
            strategy,
            "Please try completing your payment again."
        )

    # ========================================================
    # TEMPLATE GENERATOR
    # ========================================================

    def generate_template_message(
        self,
        transaction,
        recovery_result
    ):

        segment = transaction[
            "customer_segment"
        ]

        failure_type = transaction[
            "failure_type"
        ]

        strategy = recovery_result[
            "best_strategy"
        ]

        amount = float(
            transaction["transaction_amount"]
        )

        tone = self.get_customer_tone(
            segment
        )

        failure_message = (
            self.get_failure_message(
                failure_type
            )
        )

        cta = self.get_cta(
            strategy
        )

        # ---------------------------------------------
        # Subject
        # ---------------------------------------------

        if segment == "premium":

            subject = (
                "Personal assistance needed to complete "
                "your payment"
            )

        elif failure_type == "expired_card":

            subject = (
                "Update your payment method to continue"
            )

        elif failure_type in [
            "gateway_error",
            "network_error"
        ]:

            subject = (
                "Your payment could not be completed"
            )

        else:

            subject = (
                "Action needed to complete your payment"
            )

        # ---------------------------------------------
        # Greeting
        # ---------------------------------------------

        if segment == "premium":

            greeting = "Hello, valued customer,"

        elif segment == "new":

            greeting = "Welcome,"

        else:

            greeting = "Hello,"

        # ---------------------------------------------
        # Message
        # ---------------------------------------------

        body = f"""
{greeting}

We noticed that your recent payment of
₹{amount:,.2f} could not be completed.

{failure_message}

We'd like to help you complete your
purchase with minimal interruption.

{cta}

If you need assistance, our support team
is available to help.

Thank you,
ReviveAI Customer Support
""".strip()

        return {
            "subject": subject,
            "body": body,
            "tone": tone,
            "generation_method": "template"
        }

    # ========================================================
    # GEMINI GENERATOR
    # ========================================================

    def generate_ai_message(
        self,
        transaction,
        recovery_result
    ):

        if not self.gemini_available:

            return self.generate_template_message(
                transaction,
                recovery_result
            )

        segment = transaction[
            "customer_segment"
        ]

        failure = transaction[
            "failure_type"
        ]

        strategy = recovery_result[
            "best_strategy"
        ]

        amount = transaction[
            "transaction_amount"
        ]

        tone = self.get_customer_tone(
            segment
        )

        prompt = f"""
You are a professional payment recovery
communication assistant.

Generate a concise customer recovery email.

Customer segment:
{segment}

Failed payment amount:
₹{amount:,.2f}

Failure type:
{failure}

Recommended recovery strategy:
{strategy}

Tone:
{tone}

Requirements:

1. Do not blame the customer.
2. Do not expose internal AI reasoning.
3. Clearly explain the issue.
4. Give one clear action.
5. Keep the message under 150 words.
6. Do not invent discounts.
7. Do not invent transaction details.
8. Include a useful subject line.

Return exactly:

SUBJECT:
<subject>

BODY:
<body>
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            text = response.text.strip()

            if "BODY:" in text:

                parts = text.split(
                    "BODY:",
                    1
                )

                subject = (
                    parts[0]
                    .replace("SUBJECT:", "")
                    .strip()
                )

                body = parts[1].strip()

            else:

                subject = (
                    "Action needed to complete your payment"
                )

                body = text

            return {
                "subject": subject,
                "body": body,
                "tone": tone,
                "generation_method": "Gemini AI"
            }

        except Exception:

            # Safe fallback
            return self.generate_template_message(
                transaction,
                recovery_result
            )

    # ========================================================
    # PUBLIC METHOD
    # ========================================================

    def generate_message(
        self,
        transaction,
        recovery_result
    ):

        return self.generate_ai_message(
            transaction,
            recovery_result
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    transaction = {
        "transaction_amount": 1871.80,
        "failure_type": "expired_card",
        "customer_segment": "regular"
    }

    recovery_result = {
        "best_strategy":
            "alternative_payment"
    }

    agent = CommunicationAgent()

    message = agent.generate_message(
        transaction,
        recovery_result
    )

    print("\n" + "=" * 70)
    print("REVIVEAI — COMMUNICATION AGENT TEST")
    print("=" * 70)

    print(
        f"\nGeneration method: "
        f"{message['generation_method']}"
    )

    print(
        f"\nTone: "
        f"{message['tone']}"
    )

    print(
        f"\nSubject:\n"
        f"{message['subject']}"
    )

    print(
        f"\nBody:\n"
        f"{message['body']}"
    )

    print("\n" + "=" * 70)
    print("COMMUNICATION AGENT TEST COMPLETED")
    print("=" * 70)