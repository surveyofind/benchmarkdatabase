from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from benchmark.models import User
from.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
import datetime
import csv
# Create your views here.


def login_view(request):
    gd_users = User.objects.filter(gdc=True)
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        if user_type == 'gtstation':
            user = authenticate(request, username=username, password=password)
            if user and user.gdc:
                login(request, user)
                request.session['user_id'] = user.id  # Save user ID in session
                request.session['user_type'] = user_type
                return redirect(reverse('gtstationdashboard'))
        elif user_type == 'gcp':
            user = authenticate(request, username=username, password=password)
            if user and user.gdc:
                login(request, user)
                request.session['user_id'] = user.id  # Save user ID in session
                request.session['user_type'] = user_type
                return redirect(reverse('gcpdashboard'))  
        elif user_type == 'sbm':
            user = authenticate(request, username=username, password=password)
            if user and user.gdc:
                login(request, user)
                request.session['user_id'] = user.id  # Save user ID in session
                request.session['user_type'] = user_type
                return redirect(reverse('sbmdashboard'))      
        return render(request, 'login.html', {'error': 'Invalid username or password or user type'})
    return render(request, 'login.html',{'gd_users': gd_users})



def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        # Create the user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        if user_type == 'gdc':
            user.gdc = True
        elif user_type == 'cors':
            user.cors = True
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def gtstationdashboard(request):
    query = request.POST.get('searchdata','')
    request.session['query'] = query
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = gtstation.objects.filter(gdc_username=username)
    
    if query:
        user_data = user_data.filter(Q(state__icontains=query)|Q(district__icontains=query)|Q(conduction_of_gtstation__icontains=query))
    context = {
        'user_data':user_data
    }
    return render(request,'gtstationdashboard.html',context)


def gtstationdownload_csv(request):
    user_id = request.session.get('user_id')
    query = request.session.get('query')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = gtstation.objects.filter(gdc_username=username)
    if query:
        user_data = user_data.filter(Q(state__icontains=query)|Q(district__icontains=query)|Q(conduction_of_gtstation__icontains=query))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gt_station_data.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Key Id.', 'GT STATION NAME', 'PAMPHLET NO.', 'STATE', 'DISTRICT', 'TAHSIL', 'PIN CODE',
        'APPROX LATITUDE', 'APPROX LONGITUDE', 'TRIANGULATED HEIGHT (M)', 'ELLIPSOID HEIGHT (M)',
        'ORTHOMETRIC Height (m)', 'GRAVITY VALUE (MICROGAL)', 'GT STATION INSCRIPTION', 'OLD DESCRIPTION',
        'REVISED DESCRIPTION (IF NECESSARY)', 'CONDITION OF GT STATION', 'IMAGE EAST UPLOADED BY THE FIELD TEAM',
        'IMAGE WEST UPLOADED BY THE FIELD TEAM', 'IMAGE NORTH UPLOADED BY THE FIELD TEAM',
        'IMAGE SOUTH UPLOADED BY THE FIELD TEAM', 'INSPECTING PERSON NAME & DESIGNATION',
        'INSPECTING PERSON CONTACT NO.', 'LAST DATE OF VISIT', 'INSPECTION REMARK', 'GD USERNAME'
    ])

    for i in user_data:
        writer.writerow([
            i.keyid, i.gtstation_name, i.pamphlet_no, i.state, i.district, i.tahsil, i.pincode,
            i.latitude, i.longitude, i.triangulatedheight, i.ellipsoidheight, i.orthometrichight,
            i.gravityvalue, i.gt_station_inscription, i.old_description, i.revised_description,
            i.conduction_of_gtstation, i.image_east.url if i.image_east else 'No Image Available',
            i.image_west.url if i.image_west else 'No Image Available',
            i.image_north.url if i.image_north else 'No Image Available',
            i.image_south.url if i.image_south else 'No Image Available',
            i.authorised_person_name_and_designation, i.authorised_person_contactno,
            i.last_date_of_vist, i.inspection_remark, i.gdc_username
        ])

    return response


def gcpdashboard(request):
    query = request.POST.get('searchdata','')
    request.session['query'] = query
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = gcpdata.objects.filter(gdc_username=username)
    if query:
        user_data = user_data.filter(Q(state__icontains=query)|Q(gcp_name__icontains=query)|Q(district__icontains=query)|Q(conduction_of_gcp__icontains=query)|Q(tahsil__icontains=query))
    context = {
        'user_data':user_data
    }
    return render(request,'gcpdashboard.html',context)


def download_gcp_data_csv(request):
    query = request.session.get('query')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = gcpdata.objects.filter(gdc_username=username)
    if query:
        user_data = user_data.filter(Q(state__icontains=query)|Q(gcp_name__icontains=query)|Q(district__icontains=query)|Q(conduction_of_gcp__icontains=query)|Q(tahsil__icontains=query))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gcp_data.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Key Id.', 'PID', 'GCP NAME', 'STATE', 'DISTRICT', 'TAHSIL', 'PIN CODE',
        'LATITUDE', 'LONGITUDE', 'Ellipsoid HEIGHT (m)', 'ORTHOMETRIC HEIGHT (m)', 'GRAVITY VALUE (MICROGAL)',
        'GCP ON PILLAR/ROCK', 'GCP OLD DESCRIPTION', 'GCP REVISED DESCRIPTION (IF NECESSARY)',
        'CONDITION OF GCP', 'IMAGE EAST UPLOADED BY THE FIELD TEAM', 'IMAGE WEST UPLOADED BY THE FIELD TEAM',
        'IMAGE NORTH UPLOADED BY THE FIELD TEAM', 'IMAGE SOUTH UPLOADED BY THE FIELD TEAM',
        'INSPECTING PERSON NAME & DESIGNATION', 'INSPECTING PERSON CONTACT NO.', 'LAST DATE OF VISIT',
        'INSPECTION REMARK', 'GD USERNAME'
    ])

    for i in user_data:
        writer.writerow([
            i.keyid, i.pid, i.gcp_name, i.state, i.district, i.tahsil, i.pincode,
            i.latitude, i.longitude, i.ellipsoidheight, i.orthometrichight, i.gravityvalue,
            i.gcp_on_pillar, i.old_description, i.revised_description,
            i.conduction_of_gcp, i.image_east.url if i.image_east else 'No Image Available',
            i.image_west.url if i.image_west else 'No Image Available',
            i.image_north.url if i.image_north else 'No Image Available',
            i.image_south.url if i.image_south else 'No Image Available',
            i.authorised_person_name_and_designation, i.authorised_person_contactno,
            i.last_date_of_vist, i.inspection_remark, i.gdc_username
        ])

    return response


def sbmdashboard(request):
    query = request.POST.get('searchdata','')
    request.session['query'] = query
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = sbmdata.objects.filter(gdc_username=username)
    if query:
        user_data = user_data.filter(Q(state__icontains=query)|Q(sbm_type__icontains=query)|Q(district__icontains=query)|Q(conduction_of_reference_pillar__icontains=query)|Q(tahsil__icontains=query))
    context = {
        'user_data':user_data
    }
    return render(request,'sbmdasboard.html',context)


def download_sbm_data_csv(request):
    query = request.session.get('query')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = sbmdata.objects.filter(gdc_username=username)
    if query:
        user_data = user_data.filter(Q(state__icontains=query)|Q(sbm_type__icontains=query)|Q(district__icontains=query)|Q(conduction_of_reference_pillar__icontains=query)|Q(tahsil__icontains=query))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sbm_data.csv"'

    writer = csv.writer(response)
    header_row = [
        'Key Id.', 'SBM TYPE', 'PAMPHLET NO.', 'STATE', 'DISTRICT', 'TAHSIL', 'PIN CODE',
        'LATITUDE', 'LONGITUDE', 'SBM INSCRIPTION', 'SBM OLD DESCRIPTION', 'SBM REVISED DESCRIPTION (IF NECESSARY)',
        'CONDITION OF SBM', 'CONDITION OF REFERENCE PILLAR (IF NECESSARY)', 'IMAGE EAST UPLOADED BY THE FIELD TEAM',
        'IMAGE WEST UPLOADED BY THE FIELD TEAM', 'IMAGE NORTH UPLOADED BY THE FIELD TEAM', 'IMAGE SOUTH UPLOADED BY THE FIELD TEAM',
        'INSPECTING PERSON NAME & DESIGNATION', 'INSPECTING PERSON CONTACT NO.', 'LAST DATE OF VISIT',
        'INSPECTION REMARK', 'GDC NAME','LAST UPDATE TIME'
    ]
    
    writer.writerow(header_row)

    for i in user_data:
        row = [
            i.keyid, i.sbm_type, i.pamphlet_no, i.state, i.district, i.tahsil, i.pincode,
            i.latitude, i.longitude, i.sbm_inscription, i.old_description, i.revised_description,
            i.conduction_of_sbm, i.conduction_of_reference_pillar,
            i.image_east.url if i.image_east else 'No Image Available',
            i.image_west.url if i.image_west else 'No Image Available',
            i.image_north.url if i.image_north else 'No Image Available',
            i.image_south.url if i.image_south else 'No Image Available',
            i.authorised_person_name_and_designation, i.authorised_person_contactno,
            i.last_date_of_vist, i.inspection_remark, i.gdc_username, i.updatetime
        ]
        # Add values for dynamically added columns
          # Assuming a custom method get_item to fetch dynamically added columns

        writer.writerow(row)

    return response

# def sbmdashboard(request):
#     user_id = request.session.get('user_id')
#     user = User.objects.get(id=user_id)
#     username = user.username
#     user_data = sbmdata.objects.filter(gdc_username=username)

#     # Retrieve dynamically added columns from session (if any)
#     dynamic_columns = request.session.get('columns', [])

#     # Prepare a list of dictionaries with attributes for each user_data instance
#     user_data_with_dynamic_columns = []

#     for i in user_data:
#         row = {
#             'id': i.id,
#             'sbm_type': i.sbm_type,
#             'pamphlet_no': i.pamphlet_no,
#             'state': i.state,
#             'district': i.district,
#             'tahsil': i.tahsil,
#             'pincode': i.pincode,
#             'longitude': i.longitude,
#             'latitude': i.latitude,
#             'sbm_inscription': i.sbm_inscription,
#             'old_description': i.old_description,
#             'revised_description': i.revised_description,
#             'conduction_of_sbm': i.conduction_of_sbm,
#             'conduction_of_reference_pillar': i.conduction_of_reference_pillar,
#             'photo_of_sbm': i.photo_of_sbm,
#             'authorised_person_name_and_designation': i.authorised_person_name_and_designation,
#             'authorised_person_contactno': i.authorised_person_contactno,
#             'last_date_of_vist': i.last_date_of_vist,
#             'inspection_remark': i.inspection_remark,
#             'gdc_username': i.gdc_username
#         }
#         for column in dynamic_columns:
#             row[column] = getattr(i, column, '')
#         user_data_with_dynamic_columns.append(row)
        
#     context = {
#         'user_data': user_data_with_dynamic_columns,
#         'dynamic_columns': dynamic_columns
#     }
#     print(context)
#     return render(request, 'sbmdasboard.html', context)


@login_required(login_url='/')
def edit_gcpdata(request, id):
    date = datetime.datetime.now()
    # gcpalldata = gcpdata.objects.get(id=id)
    gcpalldata = get_object_or_404(gcpdata, id=id)
    if request.method == 'POST':
        # gcpalldata.gcp_name = request.POST.get('gcp_name')
        # gcpalldata.state = request.POST.get('state')
        gcpalldata.district = request.POST.get('district')
        gcpalldata.tahsil = request.POST.get('tahsil')
        gcpalldata.pincode = request.POST.get('pincode')
        # gcpalldata.latitude = request.POST.get('latitude')
        # gcpalldata.longitude = request.POST.get('longitude')
        # gcpalldata.ellipsoidheight = request.POST.get('ellipsoidheight')
        gcpalldata.orthometrichight = request.POST.get('orthometrichight')
        gcpalldata.gravityvalue = request.POST.get('gravityvalue')
        if request.POST.get('gcp_on_pillar'):
            gcpalldata.gcp_on_pillar = request.POST['gcp_on_pillar']
        # gcpalldata.gcp_on_pillar = request.POST.get('gcp_on_pillar')
        # gcpalldata.old_description = request.POST.get('old_description')
        gcpalldata.revised_description = request.POST.get('revised_description')
        # gcpalldata.conduction_of_gcp = request.POST.get('conduction_of_gcp')
        if request.POST.get('conduction_of_gcp'):
            gcpalldata.conduction_of_gcp = request.POST['conduction_of_gcp']
        # gcpalldata.photo_of_gcp = request.POST.get('photo_of_gcp')
        gcpalldata.authorised_person_name_and_designation = request.POST.get('authorised_person_name_and_designation')
        gcpalldata.authorised_person_contactno = request.POST.get('authorised_person_contactno')
        gcpalldata.last_date_of_vist = request.POST.get('last_date_of_vist')
        gcpalldata.inspection_remark = request.POST.get('inspection_remark')
        # if request.FILES.get('photo_of_gcp'):
        if 'image_east' in request.FILES:
            gcpalldata.image_east = request.FILES.get('image_east')
        if 'image_west' in request.FILES:
            gcpalldata.image_west = request.FILES.get('image_west')
        if 'image_north' in request.FILES:
            gcpalldata.image_north = request.FILES.get('image_north')
        if 'image_south' in request.FILES:
            gcpalldata.image_south = request.FILES.get('image_south')
        gcpalldata.updatetime = date
        gcpalldata.save()
        messages.success(request, 'Successfully updated your data')
        return redirect('gcpdashboard')
    return render(request, 'gcpedit.html', {'gcpalldata': gcpalldata})




@login_required(login_url='/')
def edit_gtstationdata(request, id):
    date = datetime.datetime.now()
    gtalldata = gtstation.objects.get(id=id)
    if request.method == 'POST':
        # gtalldata.gtstation_name = request.POST.get('gtstation_name')
        # gtalldata.pamphlet_no = request.POST.get('pamphlet_no')
        # gtalldata.state = request.POST.get('state')
        gtalldata.district = request.POST.get('district')
        gtalldata.tahsil = request.POST.get('tahsil')
        gtalldata.pincode = request.POST.get('pincode')
        # gtalldata.latitude = request.POST.get('latitude')
        # gtalldata.longitude = request.POST.get('longitude')
        # gtalldata.ellipsoidheight = request.POST.get('ellipsoidheight')
        gtalldata.gt_station_inscription = request.POST.get('gt_station_inscription')
        gtalldata.old_description = request.POST.get('old_description')
        gtalldata.revised_description = request.POST.get('revised_description')
        if request.POST.get('conduction_of_gtstation'):
            gtalldata.conduction_of_gtstation = request.POST['conduction_of_gtstation']
        # gcpalldata.photo_of_gcp = request.POST.get('photo_of_gcp')
        gtalldata.authorised_person_name_and_designation = request.POST.get('authorised_person_name_and_designation')
        gtalldata.authorised_person_contactno = request.POST.get('authorised_person_contactno')
        gtalldata.last_date_of_vist = request.POST.get('last_date_of_vist')
        gtalldata.inspection_remark = request.POST.get('inspection_remark')
        # if request.FILES.get('photo_of_gcp'):
        if 'image_east' in request.FILES:
            gtalldata.image_east = request.FILES.get('image_east')
        if 'image_west' in request.FILES:
            gtalldata.image_west = request.FILES.get('image_west')
        if 'image_north' in request.FILES:
            gtalldata.image_north = request.FILES.get('image_north')
        if 'image_south' in request.FILES:
            gtalldata.image_south = request.FILES.get('image_south')
        gtalldata.updatetime = date    
        gtalldata.save()
        messages.success(request, 'Successfully updated your data')
        return redirect('gtstationdashboard')
    return render(request, 'edit_gt_station.html', {'gtalldata': gtalldata})



@login_required(login_url='/')
def edit_sbmdata(request, id):
    date = datetime.datetime.now()
    sbmalldata = sbmdata.objects.get(id=id)
    if request.method == 'POST':
        if 'image_east' in request.FILES:
            sbmalldata.image_east = request.FILES.get('image_east')
        if 'image_west' in request.FILES:
            sbmalldata.image_west = request.FILES.get('image_west')
        if 'image_north' in request.FILES:
            sbmalldata.image_north = request.FILES.get('image_north')
        if 'image_south' in request.FILES:
            sbmalldata.image_south = request.FILES.get('image_south')
        if request.POST.get('sbm_type'):
            sbmalldata.sbm_type = request.POST['sbm_type']
        # sbmalldata.pamphlet_no = request.POST.get('pamphlet_no')
        # sbmalldata.state = request.POST.get('state')
        sbmalldata.district = request.POST.get('district')
        sbmalldata.tahsil = request.POST.get('tahsil')
        sbmalldata.pincode = request.POST.get('pincode')
        sbmalldata.latitude = request.POST.get('latitude')
        sbmalldata.longitude = request.POST.get('longitude')
        sbmalldata.sbm_inscription = request.POST.get('sbm_inscription')
        sbmalldata.old_description = request.POST.get('old_description')
        sbmalldata.revised_description = request.POST.get('revised_description')
        if request.POST.get('conduction_of_sbm'):
            sbmalldata.conduction_of_sbm = request.POST['conduction_of_sbm']
        # sbmalldata.conduction_of_reference_pillar = request.POST.get('conduction_of_reference_pillar')
        if request.POST.get('conduction_of_reference_pillar'):
            sbmalldata.conduction_of_reference_pillar = request.POST['conduction_of_reference_pillar']
        # gcpalldata.photo_of_gcp = request.POST.get('photo_of_gcp')
        sbmalldata.authorised_person_name_and_designation = request.POST.get('authorised_person_name_and_designation')
        sbmalldata.authorised_person_contactno = request.POST.get('authorised_person_contactno')
        sbmalldata.last_date_of_vist = request.POST.get('last_date_of_vist')
        sbmalldata.inspection_remark = request.POST.get('inspection_remark')
        # if request.FILES.get('photo_of_gcp'):
        
        sbmalldata.updatetime = date 
        sbmalldata.save()
        messages.success(request, 'Successfully updated your data')
        return redirect('sbmdashboard')
    return render(request, 'editsbm.html', {'sbmalldata': sbmalldata})



def addsbm(request):
    date = datetime.datetime.now()
    gd_username = User.objects.all()
    if request.method == "POST":
        sbm_type = request.POST.get('sbm_type')
        state = request.POST.get('state')
        district = request.POST.get('district')
        tahsil = request.POST.get('tahsil')
        pincode = request.POST.get('pincode')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        sbm_inscription = request.POST.get('sbm_inscription')
        old_description = request.POST.get('old_description')
        revised_description = request.POST.get('revised_description')
        conduction_of_sbm = request.POST.get('conduction_of_sbm')
        conduction_of_reference_pillar = request.POST.get('conduction_of_reference_pillar')
        image_east = request.FILES.get('image_east')
        image_west = request.FILES.get('image_west')
        image_north = request.FILES.get('image_north')
        image_south = request.FILES.get('image_south')
        authorised_person_name_and_designation = request.POST.get('authorised_person_name_and_designation')
        authorised_person_contactno = request.POST.get('authorised_person_contactno')
        last_date_of_vist = request.POST.get('last_date_of_vist')
        inspection_remark = request.POST.get('inspection_remark')
        gdc_username = request.POST.get('gdc_username')

        new_entry = sbmdata(
            sbm_type=sbm_type,
            state=state,
            district=district,
            tahsil=tahsil,
            pincode=pincode,
            latitude=latitude,
            longitude=longitude,
            sbm_inscription=sbm_inscription,
            old_description=old_description,
            revised_description=revised_description,
            conduction_of_sbm=conduction_of_sbm,
            conduction_of_reference_pillar=conduction_of_reference_pillar,
            image_east=image_east,
            image_west=image_west,
            image_north=image_north,
            image_south=image_south,
            authorised_person_name_and_designation=authorised_person_name_and_designation,
            authorised_person_contactno=authorised_person_contactno,
            last_date_of_vist=last_date_of_vist,
            inspection_remark=inspection_remark,
            gdc_username=gdc_username,
            updatetime = date 
        )
        
        new_entry.save()
        
        return redirect('sbmdashboard')  # Redirect to a success page or wherever you want

    return render(request, 'addsbm.html', {'gd_username': gd_username})



def addgtstation(request):
    date = datetime.datetime.now()
    gd_username = User.objects.all()
    if request.method == "POST":
        gtstation_name = request.POST.get('gtstation_name')
        state = request.POST.get('state')
        district = request.POST.get('district')
        tahsil = request.POST.get('tahsil')
        pincode = request.POST.get('pincode')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        triangulatedheight = request.POST.get('triangulatedheight')
        ellipsoidheight = request.POST.get('ellipsoidheight')
        orthometrichight = request.POST.get('orthometrichight')
        gravityvalue = request.POST.get('gravityvalue')
        gt_station_inscription = request.POST.get('gt_station_inscription')
        old_description = request.POST.get('old_description')
        revised_description = request.POST.get('revised_description')
        conduction_of_gtstation = request.POST.get('conduction_of_gtstation')
        image_east = request.FILES.get('image_east')
        image_west = request.FILES.get('image_west')
        image_north = request.FILES.get('image_north')
        image_south = request.FILES.get('image_south')
        authorised_person_name_and_designation = request.POST.get('authorised_person_name_and_designation')
        authorised_person_contactno = request.POST.get('authorised_person_contactno')
        last_date_of_vist = request.POST.get('last_date_of_vist')
        inspection_remark = request.POST.get('inspection_remark')
        gdc_username = request.POST.get('gdc_username')
         # Automatically set the update time to now

        new_entry = gtstation(
            gtstation_name=gtstation_name,
            state=state,
            district=district,
            tahsil=tahsil,
            pincode=pincode,
            latitude=latitude,
            longitude=longitude,
            triangulatedheight=triangulatedheight,
            ellipsoidheight=ellipsoidheight,
            orthometrichight=orthometrichight,
            gravityvalue=gravityvalue,
            gt_station_inscription=gt_station_inscription,
            old_description=old_description,
            revised_description=revised_description,
            conduction_of_gtstation=conduction_of_gtstation,
            image_east=image_east,
            image_west=image_west,
            image_north=image_north,
            image_south=image_south,
            authorised_person_name_and_designation=authorised_person_name_and_designation,
            authorised_person_contactno=authorised_person_contactno,
            last_date_of_vist=last_date_of_vist,
            inspection_remark=inspection_remark,
            gdc_username=gdc_username,
            updatetime=date,
        )
        
        new_entry.save()
        
        return redirect('gtstationdashboard')  # Redirect to a success page or wherever you want

    # Pass the list of users for the dropdown
      # Adjust the filter as needed
    return render(request, 'addongt.html', {'gd_username': gd_username})


# def addsbm(request, id):
#     sbm_instance = get_object_or_404(sbmdata, id=id)
    
#     if request.method == 'POST':
#         form = AddFieldForm(request.POST)
#         if form.is_valid():
#             field_name = form.cleaned_data['field_name']
#             field_value = form.cleaned_data['field_value']
#             sbm_instance.dynamic_fields[field_name] = field_value
#             sbm_instance.save()
#     else:
#         form = AddFieldForm()
    
#     return render(request, 'addsbm.html', {'form': form, 'sbm_instance': sbm_instance})



def admin_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('admin_dashboard')
    return render(request,'adminlogin.html')



def admin_dashboard(request):
    data = gtstation.objects.all()
    context = {
        'data':data
    }
    return render(request,'admin_dashboard.html',context)


def admin_dashboardgcpdata(request):
    data = gcpdata.objects.all()
    context = {
        'data':data
    }
    return render(request,'admingcpdata.html',context)


def admin_dashboardSBMdata(request):
    data = sbmdata.objects.all()
    context = {
        'data':data
    }
    return render(request,'adminsbmdata.html',context)



def gcp_log(request):
    keyid = request.POST.get('keyid')
    request.session['keyid'] = keyid
    data  = BenchmarkGcpdataBackup.objects.filter(keyid=keyid)
    context = {
        'data':data
    }
    return render(request,'gcp_log.html',context)


def benchmark_gcpdata_download(request):
    if request.method == 'GET':
        keyid = request.session.get('keyid')
        benchmark_data = BenchmarkGcpdataBackup.objects.filter(keyid=keyid)
        text_content = ""
        
        for gcp in benchmark_data:
            text_content += f"Key ID: {gcp.keyid}\n"
            text_content += f"GCP Name: {gcp.gcp_name}\n"
            text_content += f"Pamphlet No: {gcp.pamphlet_no}\n"
            text_content += f"State: {gcp.state}\n"
            text_content += f"District: {gcp.district}\n"
            text_content += f"Tahsil: {gcp.tahsil}\n"
            text_content += f"Pincode: {gcp.pincode}\n"
            text_content += f"Longitude: {gcp.longitude}\n"
            text_content += f"Latitude: {gcp.latitude}\n"
            text_content += f"Ellipsoid Height: {gcp.ellipsoidheight}\n"
            text_content += f"Orthometric Height: {gcp.orthometrichight}\n"
            text_content += f"Gravity Value: {gcp.gravityvalue}\n"
            text_content += f"GCP on Pillar: {gcp.gcp_on_pillar}\n"
            text_content += f"Old Description: {gcp.old_description}\n"
            text_content += f"Revised Description: {gcp.revised_description}\n"
            text_content += f"Conduction of GCP: {gcp.conduction_of_gcp}\n"
            text_content += f"Image East: {gcp.image_east}\n"
            text_content += f"Image West: {gcp.image_west}\n"
            text_content += f"Image North: {gcp.image_north}\n"
            text_content += f"Image South: {gcp.image_south}\n"
            text_content += f"Authorised Person Name and Designation: {gcp.authorised_person_name_and_designation}\n"
            text_content += f"Authorised Person Contact No: {gcp.authorised_person_contactno}\n"
            text_content += f"Last Date of Visit: {gcp.last_date_of_vist}\n"
            text_content += f"Inspection Remark: {gcp.inspection_remark}\n"
            text_content += f"Update Time: {gcp.updatetime}\n"
            text_content += f"GDC Username: {gcp.gdc_username}\n"
            text_content += f"PID: {gcp.pid}\n"
            text_content += "\n"  # Add a newline for separation between records
        
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="BenchmarkGcpdataBackup.txt"'
        return response

def gtstation_log(request):
    keyid = request.POST.get('keyid')
    request.session['keyid'] = keyid
    data  = BenchmarkGtstationBackup.objects.filter(keyid=keyid)
    context = {
        'data':data
    }
    return render(request,'gtstationlog.html',context)




def benchmark_gtstation_download(request):
    if request.method == 'GET':
        keyid = request.session.get('keyid')
        benchmark_data = BenchmarkGtstationBackup.objects.filter(keyid=keyid)
        text_content = ""
        
        for gtstation in benchmark_data:
            text_content += f"Key ID: {gtstation.keyid}\n"
            text_content += f"GT Station Name: {gtstation.gtstation_name}\n"
            text_content += f"Pamphlet No: {gtstation.pamphlet_no}\n"
            text_content += f"State: {gtstation.state}\n"
            text_content += f"Ellipsoid Height: {gtstation.ellipsoidheight}\n"
            text_content += f"Triangulated Height: {gtstation.triangulatedheight}\n"
            text_content += f"Orthometric Height: {gtstation.orthometrichight}\n"
            text_content += f"Gravity Value: {gtstation.gravityvalue}\n"
            text_content += f"District: {gtstation.district}\n"
            text_content += f"Tahsil: {gtstation.tahsil}\n"
            text_content += f"Pincode: {gtstation.pincode}\n"
            text_content += f"Longitude: {gtstation.longitude}\n"
            text_content += f"Latitude: {gtstation.latitude}\n"
            text_content += f"GT Station Inscription: {gtstation.gt_station_inscription}\n"
            text_content += f"Old Description: {gtstation.old_description}\n"
            text_content += f"Revised Description: {gtstation.revised_description}\n"
            text_content += f"Conduction of GT Station: {gtstation.conduction_of_gtstation}\n"
            text_content += f"Image East: {gtstation.image_east}\n"
            text_content += f"Image West: {gtstation.image_west}\n"
            text_content += f"Image North: {gtstation.image_north}\n"
            text_content += f"Image South: {gtstation.image_south}\n"
            text_content += f"Authorised Person Name and Designation: {gtstation.authorised_person_name_and_designation}\n"
            text_content += f"Authorised Person Contact No: {gtstation.authorised_person_contactno}\n"
            text_content += f"Last Date of Visit: {gtstation.last_date_of_vist}\n"
            text_content += f"Inspection Remark: {gtstation.inspection_remark}\n"
            text_content += f"Update Time: {gtstation.updatetime}\n"
            text_content += f"GDC Username: {gtstation.gdc_username}\n"
            text_content += "\n"  # Add a newline for separation between records
        
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="BenchmarkGtstationBackup.txt"'
        return response


def sbm_log(request):
    keyid = request.POST.get('keyid')
    request.session['keyid'] = keyid
    data  = BenchmarkSbmdataBackup.objects.filter(keyid=keyid)
    context = {
        'data':data
    }
    return render(request,'sbmlogs.html',context)


def benchmark_sbmdata_download(request):
    if request.method == 'GET':
        keyid = request.session.get('keyid')
        benchmark_data = BenchmarkSbmdataBackup.objects.filter(keyid=keyid)
        text_content = ""
        
        for sbm in benchmark_data:
            text_content += f"Key ID: {sbm.keyid}\n"
            text_content += f"SBM Type: {sbm.sbm_type}\n"
            text_content += f"Pamphlet No: {sbm.pamphlet_no}\n"
            text_content += f"State: {sbm.state}\n"
            text_content += f"District: {sbm.district}\n"
            text_content += f"Tahsil: {sbm.tahsil}\n"
            text_content += f"Pincode: {sbm.pincode}\n"
            text_content += f"Longitude: {sbm.longitude}\n"
            text_content += f"Latitude: {sbm.latitude}\n"
            text_content += f"SBM Inscription: {sbm.sbm_inscription}\n"
            text_content += f"Old Description: {sbm.old_description}\n"
            text_content += f"Revised Description: {sbm.revised_description}\n"
            text_content += f"Conduction of SBM: {sbm.conduction_of_sbm}\n"
            text_content += f"Conduction of Reference Pillar: {sbm.conduction_of_reference_pillar}\n"
            text_content += f"Image East: {sbm.image_east}\n"
            text_content += f"Image West: {sbm.image_west}\n"
            text_content += f"Image North: {sbm.image_north}\n"
            text_content += f"Image South: {sbm.image_south}\n"
            text_content += f"Authorised Person Name and Designation: {sbm.authorised_person_name_and_designation}\n"
            text_content += f"Authorised Person Contact No: {sbm.authorised_person_contactno}\n"
            text_content += f"Last Date of Visit: {sbm.last_date_of_vist}\n"
            text_content += f"Inspection Remark: {sbm.inspection_remark}\n"
            text_content += f"Update Time: {sbm.updatetime}\n"
            text_content += f"GDC Username: {sbm.gdc_username}\n"
            text_content += "\n"  # Add a newline for separation between records
        
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="BenchmarkSbmdataBackup.txt"'
        return response