import random

def delivery_agent(state: dict) -> dict:
    delivery_outcome = random.choice(["success", "delay", "failure"])
    
    if delivery_outcome == "success":
        return {
            "delivery_status": "Delivered successfully",
            "issue_detected": False
        }
    elif delivery_outcome == "delay":
        return {
            "delivery_status": "Delivery delayed due to traffic",
            "issue_detected": True,
            "issue_type": "delay"
        }
    else:  # failure
        return {
            "delivery_status": "Delivery failed due to vehicle breakdown",
            "issue_detected": True,
            "issue_type": "failure"
        }
