# agents/delay_handler.py

def delay_handler(state: dict) -> dict:
    return {
        "delivery_status": "Delivery delayed. Will retry in 24 hours.",
        "next_step": "reschedule"
    }
