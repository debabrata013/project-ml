from google.adk.agents import LlmAgent
from home_inv_agent.prompt import ROOT_AGENT_PROMPT
from home_inv_agent.tools import *

MODEL = "gemini-1.5-flash"

root_agent = LlmAgent(
    name="home_inventory_agent",
    model=MODEL,
    description="Agent to manage and keep a track of Home Inventory",
    instruction=ROOT_AGENT_PROMPT,
    tools=[
        fetch_all_cat,
        save_cat,
        delete_cat,
        fetch_all_inv,
        save_inv_item,
        fetch_inv_by_category,
        fetch_inv_by_status,
        fetch_inv_by_name,
        update_inv_item,
        delete_inv_item,
        count_all_inv,
        count_inv_by_category,
        count_inv_by_status,
        count_inv_by_user,
        get_most_active_user,
        get_recent_updates,
        process_receipt_image
    ],
)
