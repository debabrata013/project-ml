import json
from services.category_service import fetch_all_categories, save_category, delete_category
from services.inventory_service import (
    fetch_all_inventory, 
    fetch_inventory_by_name, 
    fetch_inventory_by_status, 
    fetch_inventory_by_category, 
    save_inventory_item, 
    delete_inventory_item
)

def fetch_all_cat() -> dict:
    return fetch_all_categories({})

def save_cat(input: str) -> dict:
    input_dict = json.loads(input)
    return save_category(input_dict)

def delete_cat(input: str) -> dict:
    input_dict = json.loads(input)
    return delete_category(input_dict)

def fetch_all_inv() -> dict: 
    return fetch_all_inventory({})

def save_inv_item(input: str) -> dict:
    input_dict = json.loads(input)
    return save_inventory_item(input_dict)

def fetch_inv_by_category(input: str) -> dict:
    input_dict = json.loads(input)
    return fetch_inventory_by_category(input_dict)

def fetch_inv_by_status(input: str) -> dict:
    input_dict = json.loads(input)
    return fetch_inventory_by_status(input_dict)

def fetch_inv_by_name(input: str) -> dict:
    input_dict = json.loads(input)
    return fetch_inventory_by_name(input_dict)

def update_inv_item(input: str) -> dict:
    input_dict = json.loads(input)
    return save_inventory_item(input_dict)

def delete_inv_item(input: str) -> dict:
    input_dict = json.loads(input)
    return delete_inventory_item(input_dict)

def count_all_inv() -> dict:
    items = fetch_all_inventory({})
    return {"total_count": len(items), "items": items}

def count_inv_by_category(input: str) -> dict:
    input_dict = json.loads(input)
    items = fetch_inventory_by_category(input_dict)
    return {"count": len(items), "category": input_dict["cat_name"], "items": items}

def count_inv_by_status(input: str) -> dict:
    input_dict = json.loads(input)
    items = fetch_inventory_by_status(input_dict)
    return {"count": len(items), "status": input_dict["item_status"], "items": items}

def count_inv_by_user(input: str) -> dict:
    input_dict = json.loads(input)
    username = input_dict["username"]
    all_items = fetch_all_inventory({})
    user_items = [item for item in all_items if item.get("last_updated_by") == username]
    return {"count": len(user_items), "username": username, "items": user_items}

def get_most_active_user() -> dict:
    all_items = fetch_all_inventory({})
    user_counts = {}
    for item in all_items:
        user = item.get("last_updated_by", "unknown")
        user_counts[user] = user_counts.get(user, 0) + 1
    
    if not user_counts:
        return {"most_active_user": None, "count": 0, "user_counts": {}}
    
    most_active = max(user_counts, key=user_counts.get)
    return {"most_active_user": most_active, "count": user_counts[most_active], "user_counts": user_counts}

def get_recent_updates() -> dict:
    all_items = fetch_all_inventory({})
    if not all_items:
        return {"recent_updates": [], "most_recent_user": None}
    
    sorted_items = sorted(all_items, key=lambda x: x.get("last_updated_at", ""), reverse=True)
    most_recent = sorted_items[0] if sorted_items else None
    
    return {
        "most_recent_user": most_recent.get("last_updated_by") if most_recent else None,
        "most_recent_item": most_recent.get("item_name") if most_recent else None,
        "last_updated_at": most_recent.get("last_updated_at") if most_recent else None,
        "recent_updates": sorted_items[:10]
    }

def process_receipt_image(input: str) -> dict:
    try:
        import google.generativeai as genai
        import base64
        import re
        
        input_dict = json.loads(input)
        image_data = input_dict["image_data"]
        username = input_dict["username"]
        
        # Configure Gemini
        genai.configure(api_key=input_dict.get("api_key", ""))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        
        prompt = "Extract all items from this receipt/bill. Return only a JSON array with objects containing 'item_name', 'category' (guess appropriate category like fruits, vegetables, dairy, etc.), and 'quantity_status' (set to 'medium' for all items). Example: [{'item_name': 'apples', 'category': 'fruits', 'quantity_status': 'medium'}]"
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        
        # Parse JSON response
        json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if json_match:
            items_data = json.loads(json_match.group())
        else:
            return {"error": "Could not extract items from receipt", "raw_response": response.text}
        
        # Add items to inventory
        added_items = []
        for item in items_data:
            try:
                item_input = {
                    "item_name": item["item_name"],
                    "cat_name": item["category"],
                    "item_status": item["quantity_status"],
                    "comment": "Added from receipt",
                    "username": username
                }
                result = save_inventory_item(item_input)
                added_items.append(result)
            except Exception as e:
                continue
        
        return {
            "success": True,
            "extracted_items": items_data,
            "added_items": added_items,
            "total_added": len(added_items)
        }
        
    except Exception as e:
        return {"error": f"Failed to process receipt: {str(e)}"}