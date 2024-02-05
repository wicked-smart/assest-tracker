import os
from django.urls import resolve
from datetime import datetime, timezone
import pytz



class AssetTrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_path = 'asset_tracker.log'
        self.max_file_size = 1e5  # Maximum file size in bytes
        self.setup_logging()

    def setup_logging(self):
        #  if the log file exists and exceeds the maximum size
        if os.path.exists(self.log_path) and os.path.getsize(self.log_path) > self.max_file_size:
             
            #create a new log file
            base_name, extension = os.path.splitext(self.log_path)
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            new_log_path = f'{base_name}_{timestamp}{extension}'

           
            self.log_path = new_log_path
            
            with open(new_log_path, 'a') as log_file:
                pass 
            


    def log_message(self, message):
        # Check if the log file exceeds the maximum size
        if os.path.getsize(self.log_path) > self.max_file_size:
            self.setup_logging()  

        # Add the log message
        timestamp = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {message}\n"

        
        with open(self.log_path, 'a') as log_file:
            log_file.write(log_message)

    
    def __call__(self, request):

        #print("middleware is running ")

        # logg request path
        #print(f"Asset Tracker MiddleWare - Request Path: {request.path}")

        try:

            #resolve to get the view name
            match = resolve(request.path_info)
            view_name = match.func


            if view_name.__name__ == "asset_types":
               self.log_message("Asset Tracker MiddleWare - Asset types Listed!")
            
            if view_name.__name__ == "index":
               self.log_message("Asset Tracker MiddleWare - Dashboard Page Loaded!")
            if view_name.__name__ == "asset_types_detail":
               self.log_message("Asset Tracker MiddleWare - Asset types detail Loaded!")
            if view_name.__name__ == "asset_type_update":
               self.log_message("Asset Tracker MiddleWare - Asset types Updated!")
            if view_name.__name__ == "asset_type_add":
               self.log_message("Asset Tracker MiddleWare - New Asset type Added!")
            if view_name.__name__ == "asset_type_delete":
               self.log_message("Asset Tracker MiddleWare -  Asset type Deleted!")

            if view_name.__name__ == "asset_add":
               self.log_message("Asset Tracker MiddleWare - New Asset Added!")
            if view_name.__name__ == "assets":
               self.log_message("Asset Tracker MiddleWare - Assets Listed!")
            if view_name.__name__ == "asset_detail":
               self.log_message("Asset Tracker MiddleWare - Asset Detail Listed!")
            if view_name.__name__ == "asset_update":
               self.log_message("Asset Tracker MiddleWare - Asset Updated!")
            if view_name.__name__ == "asset_delete":
               self.log_message("Asset Tracker MiddleWare - Asset Deleted!")
            if view_name.__name__ == "generate_csv":
              self.log_message("Asset Tracker MiddleWare - Assets CSV File downloaded !")

        except Exception as e:
            self.log_message(f"Asset Tracker MiddleWare -Unable to resolve the view name: {e}!")
        
        response = self.get_response(request)

        return response