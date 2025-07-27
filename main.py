"""Main terminal loop for the calendar assistant. Handles user input, interpretation, and calendar actions."""

from dotenv import load_dotenv

# Load environment variables from .env FIRST
load_dotenv()

import openai_client
from utils.command_dispatcher import dispatch
from core.conversation_manager import ConversationState

# Main terminal loop
if __name__ == "__main__":
    print("Welcome to the Terminal Calendar Assistant! Type 'exit' to quit.")

    # Initialize conversation state for session memory
    conversation_state = ConversationState()

    while True:
        user_input = input("\n> ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        # Get conversation context for LLM
        context = conversation_state.get_context_for_llm_prompt()

        # Interpret the command using GPT-4o with conversation context
        interpreted = openai_client.interpret_command(user_input, context)
        print(f"\n[Interpreted]: {interpreted}")

        # Handle different action types
        action = interpreted.get("action") if interpreted else None
        details = interpreted.get("details") if interpreted else {}
        if not isinstance(details, dict):
            details = {}

        start_date = details.get("start_date")
        end_date = details.get("end_date")

        # Dispatch action to handler
        try:
            dispatch(action, details)
        except KeyError:
            print("[Not implemented yet]")

        # Update conversation state with this turn
        conversation_state.append_turn(user_input, action, details)
