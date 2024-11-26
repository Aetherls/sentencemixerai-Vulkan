from waitress import serve
from App import app
import schedule
import threading
import time
import os

# Define the function to be run on schedule
def clean_dir(dir):
   try:
     files = os.listdir(dir)
     for file in files:
       file_path = os.path.join(dir, file)
       if os.path.isfile(file_path):
         os.remove(file_path)
     print("All files deleted successfully.")
   except OSError:
     print("Error occurred while deleting files.")

# Function to run the scheduler
def run_scheduler():
    schedule.every().day.at("00:00").do(clean_dir, "tmp/")  # Schedule task every day at midnight

    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=9000)
