from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib import messages
from .forms import *
from django.urls import reverse
import csv
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from assessment import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here


def register_view(request):

    if request.method == "GET":
        return render(request, "asset_tracker/register.html")
    else:
        #Get all the POST data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        emp_code = request.POST.get("employeeCode")
        email= request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        username = email.split('@')[0]

        print(f"username:= {username}")
        
        if (first_name and not last_name) or (not first_name and last_name) or (not first_name and not last_name):
            return render(request, "asset_tracker/register.html", {"name_error": "Both first and last name is required!!"})

        if emp_code is None:
            return render(request, "asset_tracker/register.html", {"code_error": "Both first and last name is required!!"})

        if password != confirmation:
            return render(request, "asset_tracker/register.html", {"confirmation_error": "password and confirmation does not match!!"})
        
        try:
            user = User.objects.create_user(username=username)

            user.set_password(password)

            user.first_name = first_name
            user.last_name = last_name
            user.employee_code = emp_code
            user.email = email
            
            user.save()

        
        except IntegrityError as e:
            return render(request, "asset_tracker/register.html", {"integrity_error": "User already exists! Try with different emailid..."})

        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    

        

def login_view(request):
    if request.method == "GET":
        return render(request, "asset_tracker/login.html")
    else:
        email = request.POST.get("email")
        employee_code = request.POST.get("employeeCode")
        password = request.POST.get("password")
        remember_me = request.POST.get('remember_me')

        print(f"email := {email} and password := {password}")

        username = email.split('@')[0]
        print(username)

        user = authenticate(request, username=username, employee_code=employee_code, password=password)
        print(user)

        if user is not None:
            login(request, user)
            if not remember_me:
                # Session expires when the user closes the browser
                request.session.set_expiry(0)  
            else:
                # longer expiration time for the session cookie
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "asset_tracker/login.html", {"login_error": "Invalid Username and/or Password or Employee Code !"})
 


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login")) 

# Load Home Page
def index(request):
    assets_types = AssetType.objects.filter(created_by=request.user)
    print("assets_types := ", assets_types)
    assets_per_type = []
    labels = []

    for asset_type in assets_types:
        labels.append(asset_type.type)
        assets_per_type.append(asset_type.assets.all().count())
    
    print("lables := ", labels)
    print("assets_count := ", assets_per_type)

    
    active = Asset.objects.filter(created_by=request.user, is_active=True).count()
    inactive = Asset.objects.filter(created_by=request.user, is_active=False).count()


    return render(request, "asset_tracker/index.html", {
        "labels_json": json.dumps(labels),
        "data_json": json.dumps(assets_per_type),
        "active_data_json": json.dumps([active, inactive])
    })


#List all the Asset types
def asset_types(request):

    asset_types = AssetType.objects.filter(created_by=request.user)

    items_per_page = 3  
    paginator = Paginator(asset_types, items_per_page)
    page = request.GET.get('page') # Get page number

    try:
        paginated_queryset = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_queryset = paginator.page(1)

    except EmptyPage:
        # If page is out of range, display last page
        paginated_queryset = paginator.page(paginator.num_pages)

    return render(request, 'asset_tracker/asset_types.html', {"asset_types": paginated_queryset})
    


# Asset type Detail
def asset_types_detail(request, asset_type_id):

    asset_type = AssetType.objects.get(id=asset_type_id)

    return render(request, "asset_tracker/asset_type_detail.html", {
        "asset_type": asset_type
    })

# Udate Asset Type Update
def assset_type_update(request, asset_type_id):
    instance = AssetType.objects.get(id=asset_type_id)
    if request.method == "POST":
        
        form = AssetTypeModelForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Asset type updated succesfully!")
            return HttpResponseRedirect(reverse("asset_types"))
        else:
            messages.error(request, "Form validation failed. Please check the data.")
        
    
    elif request.method == "GET":

        form = AssetTypeModelForm(instance=instance)
        return render(request, "asset_tracker/asset_type_edit.html", {
            "form": form,
            "asset_type_id": asset_type_id
        })

    
# Add New Asset Type
def asset_type_add(request):

    if request.method == 'POST':

        form = AssetTypeModelForm(request.POST)
        if form.is_valid():
            new_asset_type = form.save()
            new_asset_type.created_by = request.user
            new_asset_type.save()

            messages.success(request, "Asset type Added succesfully!")
            return HttpResponseRedirect(reverse("asset_types"))
        else:
            
            messages.error(request, "Form validation failed. Please check the data.")
            return render(request, "asset_tracker/asset_type_add.html", {"form": form})
    else:
        
        form = AssetTypeModelForm()
        return render(request, "asset_tracker/asset_type_add.html", {
            "form": form,
        })



# asset type delete
@csrf_exempt
def asset_type_delete(request, asset_type_id):
    
    try:
        AssetType.objects.filter(id=asset_type_id).delete()
        return JsonResponse({
            'message':'Asset Type Deleted Succesfully!'
        })
    except:
        return JsonResponse({
            'message': 'Error encountered while deleting Asset Type!'
        })



# asset delete operation
@csrf_exempt
def asset_delete(request, asset_id):
    
    try:
        Asset.objects.filter(id=asset_id).delete()
        return JsonResponse({
            'message':'Asset Deleted Succesfully!'
        })
    except:
        return JsonResponse({
            'message': 'Error encountered while deleting Asset!'
        })

#Add new asset
def asset_add(request):

    if request.method == "GET":
        asset_form = AssetModelForm(user=request.user)
        return render(request, "asset_tracker/asset_add.html", {
            "asset_form": asset_form
        })
    
    elif request.method == 'POST':
        asset_form = AssetModelForm(request.POST)
        #asset_image_form = AssetImageModelForm(request.POST, request.FILES)

        if asset_form.is_valid():
            asset = asset_form.save()
            asset.created_by = request.user  
            asset.save()

            for image in request.FILES.getlist('files'):
                AssetImage.objects.create(asset=asset, image=image)
            messages.success(request, "Asset type Added succesfully!")
            return HttpResponseRedirect(reverse("assets"))
        else:
        
            messages.error(request, "Form validation failed. Please check the data.")
            return HttpResponseRedirect(reverse("assets"))
    
    else:
        return render(request, "asset_tracker/asset_add.html", {
            "asset_form": asset_form,
            }
        )
    

# List all the assets
def assets(request):
    assets = Asset.objects.filter(created_by=request.user).order_by('-updated_at')
    items_per_page = 3  
    paginator = Paginator(assets, items_per_page)
    page = request.GET.get('page') # Get page number

    try:
        paginated_queryset = paginator.page(page)
        
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_queryset = paginator.page(1)

    except EmptyPage:
        # If page is out of range, display last page
        paginated_queryset = paginator.page(paginator.num_pages)

    return render(request, 'asset_tracker/assets.html', {"assets": paginated_queryset})
    
    



# Fetch Asset Detail
def asset_detail(request, asset_id):

    asset = Asset.objects.get(id=asset_id)

    return render(request, "asset_tracker/asset_detail.html", {
        "asset": asset
    })

#update asset data
def assset_update(request, asset_id):
    instance = Asset.objects.get(id=asset_id)
    if request.method == "POST":
        
        form = AssetModelForm(request.POST, instance=instance)
        if form.is_valid():
            asset = form.save()
            for image in request.FILES.getlist('files'):
                AssetImage.objects.create(asset=instance, image=image)
            messages.success(request, "Asset updated succesfully!")
            return HttpResponseRedirect(reverse("assets"))
        else:
            messages.error(request, "Form validation failed. Please check the data.")
        
    
    elif request.method == "GET":

        form = AssetModelForm(instance=instance)
        return render(request, "asset_tracker/asset_edit.html", {
            "form": form,
            "asset_id": asset_id
        })


# Generate all the csv data for assets and return to the template
def generate_csv(request):
    assets = Asset.objects.filter(created_by=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assets.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Created_by', 'Alloted To', 'Current Allocation Status', 'Code', 'Type', 'Is Active'])

    for asset in assets:
        writer.writerow([asset.name, asset.created_by, asset.alloted_to, asset.current_allocation_status, asset.code, asset.type, asset.is_active])

    return response

