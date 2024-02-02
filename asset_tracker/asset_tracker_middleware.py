
from django.urls import resolve



class AssetTrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        #print("middleware is running ")

        # logg request path
        #print(f"Asset Tracker MiddleWare - Request Path: {request.path}")

        try:

            #resolve to get the view name
            match = resolve(request.path_info)
            view_name = match.func


            if view_name.__name__ == "asset_types":
               print("Asset Tracker MiddleWare - Asset types Listed!")
            if view_name.__name__ == "index":
               print("Asset Tracker MiddleWare - Dashboard Page Loaded!")
            if view_name.__name__ == "asset_types_detail":
               print("Asset Tracker MiddleWare - Asset types detail Loaded!")
            if view_name.__name__ == "asset_type_update":
               print("Asset Tracker MiddleWare - Asset types Updated!")
            if view_name.__name__ == "asset_type_add":
               print("Asset Tracker MiddleWare - New Asset type Added!")
            if view_name.__name__ == "asset_type_delete":
               print("Asset Tracker MiddleWare -  Asset type Deleted!")

            if view_name.__name__ == "asset_add":
               print("Asset Tracker MiddleWare - New Asset Added!")
            if view_name.__name__ == "assets":
               print("Asset Tracker MiddleWare - Assets Listed!")
            if view_name.__name__ == "asset_detail":
               print("Asset Tracker MiddleWare - Asset Detail Listed!")
            if view_name.__name__ == "asset_update":
               print("Asset Tracker MiddleWare - Asset Updated!")
            if view_name.__name__ == "asset_delete":
               print("Asset Tracker MiddleWare - Asset Deleted!")
            if view_name.__name__ == "generate_csv":
               print("Asset Tracker MiddleWare - Assets CSV File downloaded !")

        except Exception as e:
            print(f"Asset Tracker MiddleWare -Unable to resolve the view name: {e}!")
        
        response = self.get_response(request)

        return response
