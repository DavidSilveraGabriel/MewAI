import streamlit as st
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import uuid # To generate unique IDs for runs
import time # To simulate some delay if needed and for unique IDs

# Import the Mininos class from your existing crew script
# Ensure the script can find the 'src' directory.
# If running streamlit run backend/streamlit_app.py from the root MewAI directory,
# this relative import should work if the backend directory is in PYTHONPATH
# or if streamlit handles the path correctly.
# If issues arise, might need sys.path manipulation, but let's try this first.
try:
    from src.crew import Mininos
except ImportError:
    # If the direct import fails, try adding the backend directory to the path
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from src.crew import Mininos

# --- Basic Configuration ---
# Load environment variables from .env file in the backend directory
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

# Setup logging (optional but good practice)
log_dir = Path(__file__).parent / "src" / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "streamlit_crew.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

# --- Streamlit UI ---
st.set_page_config(page_title="MewAI Crew Execution", layout="wide")
st.title("🐱 MewAI Crew Execution Interface")
st.markdown("Enter a topic and kick off the CrewAI agents to generate content.")

# --- Input Section ---
topic = st.text_input("Enter the topic for the crew:", value=os.getenv('TOPIC', 'AI LLMs'))

# --- Progress Display Area ---
# Using st.status for cleaner progress updates
status_placeholder = st.status("Waiting for kickoff...", expanded=False)

# --- Results Display Area ---
st.subheader("Crew Results")
results_placeholder = st.empty() # Placeholder for final results

# --- Callback Function for Progress ---
# This function will be passed to the Mininos class
# It needs to update Streamlit elements
def streamlit_progress_callback(generation_id: str, progress_info: dict):
    """Updates Streamlit UI based on progress info from Mininos."""
    message = progress_info.get("message", "Processing...")
    progress = progress_info.get("progress") # Percentage (optional)

    # Update the status box
    status_placeholder.update(label=message, state="running", expanded=True)

    # Log the progress
    logger.info(f"[{generation_id}] Progress: {message} ({progress}%)")

# --- Button to Start Crew ---
if st.button("🚀 Kick Off Crew!"):
    if not topic:
        st.error("Please enter a topic before kicking off the crew.")
    else:
        # Clear previous results
        results_placeholder.empty()
        status_placeholder.update(label="Initializing Crew...", state="running", expanded=True)

        # Generate a unique ID for this run
        generation_id = f"st-{uuid.uuid4()}-{int(time.time())}"
        logger.info(f"Starting crew run with ID: {generation_id} for topic: '{topic}'")

        try:
            # Instantiate Mininos with the topic and the Streamlit callback
            mininos_instance = Mininos(
                topic=topic,
                generation_id=generation_id,
                progress_callback=streamlit_progress_callback
            )

            # Run the crew (this is a blocking call)
            # Consider running in a thread for long tasks, but start simple
            status_placeholder.write("Crew execution started...")
            final_results = mininos_instance.run_crew_and_get_results()
            status_placeholder.write("Crew execution finished.")

            # Display final results
            if final_results.get("status") == "success":
                status_placeholder.update(label="Crew execution completed successfully!", state="complete", expanded=False)
                results_placeholder.success("Crew finished successfully!")
                st.json(final_results) # Display the full results dictionary

                # Optionally display specific parts more nicely
                if final_results.get("social_media"):
                    st.subheader("Generated Social Media Content:")
                    st.write(final_results["social_media"]) # Might be dict or string
                if final_results.get("images"):
                    st.subheader("Generated Image Info:")
                    st.write(final_results["images"]) # Path or message from tool

            else:
                error_message = final_results.get("message", "An unknown error occurred.")
                status_placeholder.update(label=f"Crew execution failed: {error_message}", state="error", expanded=True)
                results_placeholder.error(f"Crew execution failed: {error_message}")
                st.json(final_results) # Show error details

        except Exception as e:
            logger.error(f"[{generation_id}] Error during Streamlit crew execution: {e}", exc_info=True)
            status_placeholder.update(label=f"Critical error: {e}", state="error", expanded=True)
            results_placeholder.error(f"An unexpected error occurred: {e}")

# --- Footer or additional info ---
st.markdown("---")
st.markdown("Check `backend/src/logs/streamlit_crew.log` for detailed logs.")
