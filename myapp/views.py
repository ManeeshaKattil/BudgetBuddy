import json
import random

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max, Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from datetime import datetime
# Create your views here.
from BudgetBuddy import settings
from myapp.forecast import forecast_fn
from myapp.models import *
from django.utils import timezone


def logout_get(request):
    logout(request)
    return render(request, "index.html")

def login_get(request):
    logout(request)
    return render(request, "index.html")

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']

    a=authenticate(request,username=username,password=password)
    if a is not None:
        if a.groups.filter(name='Admin').exists():


            login(request,a)
            return redirect('/admin_home_get')
        elif a.groups.filter(name='Expert').exists():
            # obb = auth.authenticate(username="admin", password="admin")
            # if obb is not None:
            #     auth.login(request,obb)
            login(request,a)
            return redirect('/expert_home_get')
        else:
            messages.warning(request, 'Username or password is invalid')
            return redirect('/login_get')
    else:
        messages.warning(request,'Invalid Username or password')
        return redirect('/login_get/')

@login_required(login_url='/login_get/')
def admin_home_get(request):
    return render(request, "admin/adminindex.html")

@login_required(login_url='/login_get/')
def manage_expert_get(request):
    ob=Expert.objects.all()
    return render(request, "admin/manage_expert.html",{"experts":ob})

@login_required(login_url='/login_get/')
def manage_expert_post(request):
    name=request.POST['search']
    ob=Expert.objects.filter(Name__icontains=name)
    return render(request, "admin/manage_expert.html",{"experts":ob,'name':name})

@login_required(login_url='/login_get/')
def view_users_get(request):
    var=User_table.objects.all()
    return render(request, "admin/vuser.html",{'data':var})

@login_required(login_url='/login_get/')
def view_report_get(request,id):
    # request.session['uid'] = id
    var=Transaction.objects.filter(User_id=id)
    return render(request, "admin/report.html",{'data':var})

@login_required(login_url='/login_get/')
def view_report_post(request):
    ob = Transaction.objects.all()
    return render(request, "admin/report.html",{"data":ob})

@login_required(login_url='/login_get/')
def view_feedback_get(request):
    a=Feedback_table.objects.all()
    return render(request, "admin/feedback1 (1).html", {'data':a})

@login_required(login_url='/login_get/')
def view_feedback_post(request):
    name = request.POST['search']
    ob = Feedback_table.objects.filter(Date__icontains=name)
    return render(request, "admin/feedback1 (1).html",{"data":ob})

@login_required(login_url='/login_get/')
def complaint_get(request):
    a=Complaint.objects.all()
    return render(request, "admin/complaint.html",{'data':a})


@login_required(login_url='/login_get/')
def complaint_post(request):
    name = request.POST['search']
    ob = Complaint.objects.filter(Date__icontains=name)
    return render(request, "admin/complaint.html",{'data':ob})


def add_expert_get(request):
    return render(request, "admin/addExpert.html")


def add_expert_post(request):
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']
    photo = request.FILES['photo']

    fs=FileSystemStorage()
    path=fs.save(photo.name,photo)
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    phone_no = request.POST['phone']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']

    user=User.objects.create(username=username,password=make_password(password),first_name=name,email=email)
    user.save()
    user.groups.add(Group.objects.get(name='Expert'))

    a=Expert()
    a.LOGIN=user
    a.Name=name
    a.DOB=dob
    a.Gender=gender
    a.Photo=path
    a.Place=place
    a.Post=post
    a.Pin=pin
    a.Phone_number=phone_no
    a.Email=email
    a.save()
    messages.success(request, 'success')
    return redirect('/manage_expert_get/#aaa')

@login_required(login_url='/login_get/')
def reply_get(request,id):
    request.session['c_id']=id
    return render(request, "admin/reply.html")

@login_required(login_url='/login_get/')
def reply_post(request):
    Reply = request.POST['replyText']

    a=Complaint.objects.filter(id=request.session['c_id']).update(Reply=Reply)

    messages.success(request, 'Sended')
    return redirect('/complaint_get/#aaa')

@login_required(login_url='/login_get/')
def edit_tips(request,id):
    a=Tips.objects.get(id=id)
    request.session['id']=id

    return render(request, "expert/editTips.html",{'data':a})

@login_required(login_url='/login_get/')
def manage_tips_get(request):
    a=Tips.objects.filter(Expert__LOGIN__id=request.user.id)
    return render(request, "expert/manage_tips.html",{"tips":a})

@login_required(login_url='/login_get/')
def manage_tips_post(request):
    name = request.POST['search']
    a = Tips.objects.filter(Expert__LOGIN__id=request.user.id,Tip__icontains=name)
    return render(request, "expert/manage_tips.html",{"tips":a,'name':name})

@login_required(login_url='/login_get/')
def delete_tips(request,id):
    ob=Tips.objects.get(id=id)
    ob.delete()
    messages.success(request, 'deleted')
    return redirect('/manage_tips_get/#aaa')

@login_required(login_url='/login_get/')
def add_suggestions_get(request):
    print(request.session['uid'],"aaaaaaaaaaaaaaaaaaa")
    return render(request, "expert/AddSuggestions.html")

@login_required(login_url='/login_get/')
def add_suggestions_post(request):
    suggestions = request.POST['suggestions']

    a=Suggestions()
    a.Expert = Expert.objects.get(LOGIN__id=request.user.id)
    a.User_id = request.session['uid']
    a.Suggestion=suggestions
    a.Date = datetime.today()
    a.save()
    messages.success(request, 'Added')
    return redirect('/add_suggestions_get/#aaa')

@login_required(login_url='/login_get/')
def expert_home_get(request):
    return render(request, "expert/expertindex.html")

@login_required(login_url='/login_get/')
def expert_feedback_get(request):
    a = Feedback_table.objects.all()
    return render(request, "expert/feedback2.html", {'data':a})

@login_required(login_url='/login_get/')
def expert_feedback_post(request):
    name = request.POST['search']
    ob = Feedback_table.objects.filter(Date__icontains=name)
    return render(request, "expert/feedback2.html",{'data':ob})

@login_required(login_url='/login_get/')
def insert_tips_get(request):
    return render(request, "expert/insertTips.html")

@login_required(login_url='/login_get/')
def insert_tips_post(request):
    tips = request.POST['tip']
    details = request.POST['details']

    a=Tips()
    a.Expert=Expert.objects.get(LOGIN__id=request.user.id )
    a.Tip=tips
    a.Details=details
    a.Date = datetime.today()
    a.save()
    messages.success(request, 'Added')
    return redirect('/manage_tips_get/#aaa')

@login_required(login_url='/login_get/')
def edit_tips_post(request):
    tips = request.POST['tip']
    details = request.POST['details']

    a=Tips.objects.get(id=request.session['id'])
    a.Expert=Expert.objects.get(LOGIN__id=request.user.id )
    a.Tip=tips
    a.Details=details
    a.Date = datetime.today()
    a.save()
    messages.success(request, 'Added')
    return redirect('/manage_tips_get/#aaa')

@login_required(login_url='/login_get/')
def expert_view_user_get(request):
    a = User_table.objects.all()
    return render(request, "expert/view_user.html",{'data':a})

@login_required(login_url='/login_get/')
def expert_view_user_post(request):
    name = request.POST['search']
    ob = User_table.objects.filter(Name__icontains=name)
    return render(request, "expert/view_user.html",{'data':ob})

from django.db.models import Sum

@login_required(login_url='/login_get/')
def view_user_details_get(request, id):
    request.session['uid'] = id
    var = Transaction.objects.filter(User_id=id)
    credit_total = Transaction.objects.filter(User_id=id, Tan_type='Credit').aggregate(total=Sum('Amount'))['total']
    debit_total = Transaction.objects.filter(User_id=id, Tan_type='Debit').aggregate(total=Sum('Amount'))['total']

    print("Credit Total:", credit_total)
    print("Debit Total:", debit_total)

    return render(request, "expert/viewUserDetails.html", {
        'data': var,
        'credit_total': credit_total,
        'debit_total': debit_total
    })



@login_required(login_url='/login_get/')
def edit_expert(request,id):
    a=Expert.objects.get(LOGIN_id=id)
    request.session['id']=id
    return render(request, "admin/editExpert.html",{'data':a})

@login_required(login_url='/login_get/')
def edit_expert_post(request):
    name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['gender']

    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    phone_no = request.POST['phone']
    email = request.POST['email']




    a=Expert.objects.get(LOGIN=request.session['id'])
    user=User.objects.get(id=request.session['id'])
    user.email=email
    user.first_name=name
    user.save()

    if 'photo' in request.FILES:
        photo = request.FILES['photo']

        fs = FileSystemStorage()
        path = fs.save(photo.name, photo)
        a.Photo = path

    a.Name=name
    a.DOB=dob
    a.Gender=gender
    a.Place=place
    a.Post=post
    a.Pin=pin
    a.Phone_number=phone_no
    a.Email=email
    a.save()
    messages.success(request, 'success')
    return redirect('/manage_expert_get/#aaa')

@login_required(login_url='/login_get/')
def delete_expert(request,id):
    ob=Expert.objects.get(id=id)
    ob.delete()
    messages.success(request, 'deleted')
    return redirect('/manage_expert_get/#aaa')

def forgotPassword(request):
    return render(request,'forgotPassword.html')

def forgotPassword_otp(request):
    email=request.POST['email']
    try:
        user=User.objects.filter(email=email).first
    except User.DoesNotExist:
        messages.warning(request,'Email doesnt match')
        return redirect('/login_get')
    otp=random.randint(100000,999999)
    request.session['otp']=str(otp)
    request.session['email'] = email

    send_mail('Your Verification Code',
    f'Your verification code is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False)
    messages.success(request,'OTP sent To your Mail')
    return redirect('/verifyOtp/')

def verifyOtp(request):
    return render(request,'otpverification.html')

def verifyOtpPost(request):
    entered_otp=request.POST['entered_otp']
    if request.session.get('otp') == entered_otp:
        messages.success(request,'otp verified')
        return redirect('/new_password/')
    else:
        messages.warning(request,'Invalid OTP!!')
        return redirect('/login_get')

def new_password(request):
    return render(request,'new_password.html')

def changePassword(request):
    newpassword=request.POST['newPassword']
    confirmPassword=request.POST['confirmPassword']
    if newpassword == confirmPassword:
        email=request.session.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(confirmPassword)
            user.save()
            messages.success(request, 'Password Updated Successfully')
            return redirect('/login_get')
        else:
            messages.warning(request, 'User not found')
            return redirect('/new_password/')
    else:
        messages.warning(request, 'The password doesnt match!!')
        return redirect('/new_password/')







# flutter part
# user


def user_register(request):
    Name = request.POST['Name']
    DOB = request.POST['DOB']
    Gender = request.POST['Gender']
    Photo = request.FILES['photo']

    fs=FileSystemStorage()
    path=fs.save(Photo.name,Photo)
    Place = request.POST['Place']
    Post = request.POST['Post']
    Pin = request.POST['Pin']
    Phone_number = request.POST['Phone_number']
    Email = request.POST['Email']
    username = request.POST['username']
    password = request.POST['password']

    user=User.objects.create(username=username,password=make_password(password),first_name=password,email=Email)
    user.save()
    user.groups.add(Group.objects.get(name='User'))

    a=User_table()
    a.LOGIN=user
    a.Name=Name
    a.DOB=DOB
    a.Gender=Gender
    a.Photo=path
    a.Place=Place
    a.Post=Post
    a.Pin=Pin
    a.Phone_number=Phone_number
    a.Email=Email
    a.save()
    return JsonResponse({'status':'ok'})


def user_login(request):
    username=request.POST['username']
    password=request.POST['password']
    print(username,password)

    a=authenticate(request,username=username,password=password)
    print(a)
    if a is not None:
        if a.groups.filter(name='user').exists():
            # login(request,a)
            data = {"task": "ok","lid":a.id}
            return JsonResponse(data)
        else:
            data = {"task": "not"}
            r = json.dumps(data)
            print(r)
            return JsonResponse(r)
    else:
        data = {"task": "not"}
        # r = json.dumps(data)
        # print(r)
        return JsonResponse(data)



def viewtips(request):
    lid = request.POST['lid']
    ob = Tips.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'Tip':i.Tip,'expert':i.Expert.Name,'date':str(i.Date),'id':i.id,'details':i.Details}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def viewExpert(request):
    ob=Expert.objects.all()
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={
            'id':i.id,
            'loginid':i.LOGIN.id,
              'Name':i.Name,
              'DOB':i.DOB,
              'Gender':i.Gender,
              'Photo':i.Photo.url,
              'Place':i.Place,
              'Post':i.Post,
              'Pin':i.Pin,
              'Phone_number':i.Phone_number,
              'Email':i.Email}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def viewProfile(request):
    print(request.POST)
    lid=request.POST['lid']
    i=User_table.objects.get(LOGIN=lid)
    print({"status":"ok", 'Name':i.Name,
              'DOB':str(i.DOB),
              'Gender':i.Gender,
              'Photo':i.Photo.url,
              'Place':i.Place,
              'Post':i.Post,
              'Pin':i.Pin,
              'Phone_number':i.Phone_number,
              'Email':i.Email})
    return JsonResponse({"status":"ok", 'Name':i.Name,
              'DOB':str(i.DOB),
              'Gender':i.Gender,
              'Photo':i.Photo.url,
              'Place':i.Place,
              'Post':i.Post,
              'Pin':i.Pin,
              'Phone_number':i.Phone_number,
              'Email':i.Email})

def edit_profile(request):
    Name = request.POST['Name']
    DOB = request.POST['DOB']
    Gender = request.POST['Gender']

    Place = request.POST['Place']
    Post = request.POST['Post']
    Pin = request.POST['Pin']
    Phone_number = request.POST['Phone_number']
    Email = request.POST['Email']
    lid = request.POST['lid']

    a=User_table.objects.get(LOGIN=lid)



    if 'photo' in request.FILES:
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        path = fs.save(Photo.name, Photo)
        a.Photo = path
        a.save()

    a.Name=Name
    a.DOB=DOB
    a.Gender=Gender
    a.Place=Place
    a.Post=Post
    a.Pin=Pin
    a.Phone_number=Phone_number
    a.Email=Email
    a.save()
    return JsonResponse({'status':'ok'})

def add_feedback(request):
    Expert = request.POST['eid']
    Feedback = request.POST['Feedback']
    lid = request.POST['lid']


    a = Feedback_table()
    a.Feedback = Feedback
    a.Date = datetime.now().today()
    a.User = User_table.objects.get(LOGIN_id=lid)
    a.Expert_id= Expert
    a.save()
    return JsonResponse({'status': 'ok'})


def viewfeedback(request):
    lid=request.POST['lid']
    ob=Feedback_table.objects.filter(User__LOGIN__id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'Feedback':i.Feedback,'User':i.User.Name,'Date':str(i.Date),'id':i.id,'Expert':i.Expert.Name}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})

def viewsuggestion(request):
    lid = request.POST['lid']
    ob=Suggestions.objects.filter(User__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'id':i.id,
            'Suggestion':i.Suggestion,
              'uname':i.User.Name,'date':str(i.Date),'expert':i.Expert.Name}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def add_reminder(request):
    Type = request.POST['Type']
    Details = request.POST['Details']
    Amount = request.POST['Amount']
    r_date = request.POST['r_date']
    lid = request.POST['lid']

    a = Reminder()
    a.Type = Type
    a.Details = Details
    a.Amount = Amount
    a.User = User_table.objects.get(LOGIN_id=lid)
    a.Date = datetime.now().today()
    a.reminder_date = r_date
    a.Status = 'pending'
    a.save()
    return JsonResponse({'status': 'ok'})


def view_reminder(request):
    lid = request.POST['lid']
    ob=Reminder.objects.filter(User__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    total=0
    for i in ob:
        total+=i.Amount
        data={'id':i.id,
              'User':i.User.Name,
              'reminder_date':str(i.reminder_date),
              'Type':i.Type,
              'Amount':i.Amount,
              'Date':str(i.Date),
              'Details':i.Details}
        mdata.append(data)
        print(mdata)
    print(total,"aaaaaaaaaaaaaa")
    return JsonResponse({"status":"ok","data":mdata,"total":total})

def add_complaint(request):
    complaint = request.POST['Complaint']
    lid = request.POST['lid']


    a = Complaint()
    a.Complaint = complaint
    a.Date = datetime.now().today()
    a.User = User_table.objects.get(LOGIN__id=lid)
    a.Reply = 'pending'
    a.save()
    return JsonResponse({'status': 'ok'})

def view_complaint(request):
    lid = request.POST['lid']
    ob=Complaint.objects.filter(User__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'id':i.id,
              'User':i.User.Name,
              'Complaint':i.Complaint,
              'Reply':i.Reply,
              'Date':str(i.Date)}
        mdata.append(data)
    print(mdata)
    return JsonResponse({"status":"ok","data":mdata})


def add_income_expense(request):
    Tan_type = request.POST['Tan_type']
    Date = request.POST['Date']
    Exp_type = request.POST['Exp_type']
    Amount = request.POST['Amount']
    Mode = request.POST['Mode']
    lid = request.POST['lid']



    a = Transaction()
    a.Exp_type = Exp_type
    a.Date = Date
    a.User = User_table.objects.get(LOGIN_id=lid)
    a.Mode = Mode
    a.Amount = Amount
    a.Tan_type = Tan_type
    a.save()
    return JsonResponse({'status': 'ok'})


    # id.add(arr[i]['id'].toString());
    #     User.add(arr[i]['User']);
    #     Date.add(arr[i]['Date'].toString());
    #     Exp_type.add(arr[i]['Exp_type']);
    #     Mode.add(arr[i]['Mode']);
    #     Amount.add(arr[i]['Amount'].toString());
    #     Tan_type.add(arr[i]['Tan_type']);    id.add(arr[i]['id'].toString());
    #     User.add(arr[i]['User']);
    #     Date.add(arr[i]['Date'].toString());
    #     Exp_type.add(arr[i]['Exp_type']);
    #     Mode.add(arr[i]['Mode']);
    #     Amount.add(arr[i]['Amount'].toString());
    #     Tan_type.add(arr[i]['Tan_type']);

def view_expense(request):
    lid = request.POST['lid']
    ob=Transaction.objects.filter(User__LOGIN_id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={
            'id':i.id,
            'User':i.User.Name,
            'Exp_type':i.Exp_type,
            'Mode':i.Mode,
            'Date':str(i.Date),
            'Amount':i.Amount,
            'Tan_type':i.Tan_type

        }
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})

def search_report(request):
    # From = request.POST['Date']
    # To = request.POST['Date']
    # lid = request.POST['lid']
    #
    #
    # a = Transaction()
    # a.Exp_type = Exp_type
    # a.Date = datetime.now().today()
    # a.User = User_table.objects.get(LOGIN_id=lid)
    # a.Mode = Mode
    # a.Amount = Amount
    # a.Tan_type = Tan_type
    # a.save()
    return JsonResponse({'status': 'ok'})

# def view_report(request):
#     lid = request.POST['lid']
#     ob=Transaction.objects.filter(User__LOGIN_id=lid)
#     print(ob,"HHHHHHHHHHHHHHH")
#     mdata=[]
#     for i in ob:
#         data={
#             'id':i.id,
#             'User':i.User.Name,
#             'Exp_type':i.Exp_type,
#             'Mode':i.Mode,
#             'Date':str(i.Date),
#             'Amount':i.Amount,
#             'Tan_type':i.Tan_type
#
#         }
#         mdata.append(data)
#         print(mdata)
#     return JsonResponse({"status":"ok","data":mdata})

def set_goal(request):
    Amount = request.POST['Amount']
    # Date = request.POST['Date']
    Details = request.POST['Details']
    lid = request.POST['lid']



    a = Goal()
    a.Amount = Amount
    a.Date = datetime.now().today()
    a.User = User_table.objects.get(LOGIN_id=lid)
    a.Details = Details
    a.save()
    return JsonResponse({'status': 'ok'})

def view_goal(request):
    lid=request.POST['lid']
    ob=Goal.objects.filter(User__LOGIN__id=lid)
    print(ob,"HHHHHHHHHHHHHHH")
    mdata=[]
    for i in ob:
        data={'Amount':i.Amount,'User':i.User.Name,'Date':str(i.Date),'id':i.id,'Details':i.Details}
        mdata.append(data)
        print(mdata)
    return JsonResponse({"status":"ok","data":mdata})



def view_report(request):
    lid = request.POST.get('lid')
    fromdate = request.POST.get('fromdate')
    todate = request.POST.get('todate')
    ob = Transaction.objects.filter(User__LOGIN_id=lid)
    if fromdate and todate:
        try:
            from_date_obj = datetime.strptime(fromdate, "%Y-%m-%d").date()
            to_date_obj = datetime.strptime(todate, "%Y-%m-%d").date()

            ob = ob.filter(Date__range=[from_date_obj, to_date_obj])
        except Exception as e:
            print("Date parse error:", e)
            return JsonResponse({"status": "error", "message": "Invalid date format"})

    print(ob, "HHHHHHHHHHHHHHH")

    mdata = []
    for i in ob:
        data = {
            'id': i.id,
            'User': i.User.Name,
            'Exp_type': i.Exp_type,
            'Mode': i.Mode,
            'Date': str(i.Date),
            'Amount': i.Amount,
            'Tan_type': i.Tan_type
        }
        mdata.append(data)

    if mdata:
        return JsonResponse({"status": "ok", "data": mdata})
    else:
        return JsonResponse({"status": "no", "data": []})

# def forecast(request):
#     lid = request.POST.get('lid')
#     ob = Transaction.objects.filter(User__LOGIN_id=lid)
#     print(ob, "HHHHHHHHHHHHHHH")
#     mdata = []
#     datelist=[]
#     for i in ob:
#         if str(i.Date) not in datelist:
#             datelist.append(str(i.Date))
#     for date in datelist:
#         debit_total = Transaction.objects.filter(User_id=lid, Tan_type='Debit', Date = date).aggregate(total=Sum('Amount'))['total']
#
#         # data = {
#         #     'id': i.id,
#         #     # 'User': i.User.Name,
#         #     # 'Exp_type': i.Exp_type,
#         #     # 'Mode': i.Mode,
#         #     'Date': str(i.Date),
#         #     'Amount': i.Amount,
#         #     'Tan_type': i.Tan_type
#         #
#         # }
#         # mdata.append(data)
#         # print(mdata)
#     return JsonResponse({"status": "ok", "data": mdata})



# def forecast(request):
#     lid = request.POST.get('lid')
#     ob = Transaction.objects.filter(User__LOGIN_id=lid)
#     print(ob, "HHHHHHHHHHHHHHH")
#     mdata = []
#     datelist=[]
#     for i in ob:
#         if str(i.Date) not in datelist:
#             datelist.append(str(i.Date))
#     for date in datelist:
#         debit_total = Transaction.objects.filter(User_id=lid, Tan_type='Debit', Date = date).aggregate(total=Sum('Amount'))['total']
#
#     return JsonResponse({"status": "ok", "data": mdata})





from django.db.models import Sum
import numpy as np

def forecast(request):
    lid = request.POST['lid']
    ob = Transaction.objects.filter(User__LOGIN_id=lid).order_by('Date')
    datelist = []
    mdata = []
    for i in ob:
        date_str = str(i.Date)
        if date_str not in datelist:
            datelist.append(date_str)

    datelist = sorted(datelist)
    daily_expenses = []
    for date in datelist:
        debit_total = Transaction.objects.filter(
            User__LOGIN_id=lid,
            Tan_type='Debit',
            Date=date
        ).aggregate(total=Sum('Amount'))['total'] or 0

        daily_expenses.append({"date":date,"amt":debit_total})
        mdata.append({
            "date": date,
            "total_debit": debit_total
        })

    print(mdata)
    return JsonResponse({
        "status": "ok",
        "data": mdata,
        "predicted_future_expense": round(100.23456, 2)
    })

########################
from datetime import datetime, timedelta


def get_dates_between(start_date_str, end_date_str, date_format='%Y-%m-%d'):

    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, date_format).date()
    end_date = datetime.strptime(end_date_str, date_format).date()

    # Calculate the number of days between the dates
    delta = end_date - start_date

    # Generate all dates in the range
    dates_list = []
    for i in range(delta.days + 1):  # +1 to include the end date
        current_date = start_date + timedelta(days=i)
        dates_list.append(current_date.strftime(date_format))  # Convert back to string format

    return dates_list

def get_dates_between1(start_date_str, end_date_str, date_format='%Y-%m-%d'):

    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, date_format).date()
    end_date = end_date_str

    # Calculate the number of days between the dates


    # Generate all dates in the range
    dates_list = []
    for i in range(end_date):  # +1 to include the end date
        current_date = start_date + timedelta(days=i+1)
        dates_list.append(current_date.strftime(date_format))  # Convert back to string format

    return dates_list

def forecast1(request):
    lid = request.POST['lid']
    ob = Transaction.objects.filter(User__LOGIN_id=lid,Tan_type='Debit').order_by('Date')
    from_date=ob[0].Date
    last_date=ob[len(ob)-1].Date

    datelist = get_dates_between(str(from_date),str(datetime.now().strftime("%Y-%m-%d")))
    mdata = []
    daily_expenses = []
    X=[]
    Y=[]
    i=1
    for date in datelist:
        debit_total = Transaction.objects.filter(
            User__LOGIN_id=lid,
            Tan_type='Debit',
            Date=date
        ).aggregate(total=Sum('Amount'))['total'] or 0
        k=str(date)
        X.append(i)
        Y.append(debit_total)
        daily_expenses.append({"date":k,"amt":debit_total})

        i=i+1

        mdata.append({
            "date": date,
            "total_debit": debit_total
        })
    mdata=[]
    res = forecast_fn(X, Y)
    new_dates=get_dates_between1(datetime.now().strftime("%Y-%m-%d"),len(res)+1)
    for i in range(len(res)):
        mdata.append({
            "date": new_dates[i],
            "total_debit": res[i]
        })
    print(res, "kkkkkkkkkkkkkkkkkkkkkk")
    print(mdata)
    return JsonResponse({
        "status": "ok",
        "data": mdata,
        "predicted_future_expense": round(100.23456, 2)
    })

########################




def expert_chat_withuser(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = User_table.objects.get(LOGIN=cid)

    return render(request, "expert/Chat.html", {'photo': qry.Photo, 'name': qry.Name, 'toid': cid})

def chat_view(request):
    fromid = request.user.id
    toid = request.session["userid"]
    qry = User_table.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(
        Q(From_id_id=fromid, To_id_id=toid) | Q(From_id_id=toid, To_id_id=fromid)
    ).order_by('Date', 'Time')

    l = []
    for i in res:
        l.append({
            "id": i.id,
            "message": i.Message,
            "to": i.To_id_id,
            "date": i.Date,
            "time": i.Time,
            "from": i.From_id_id
        })

    return JsonResponse({
        'photo': qry.Photo.url if qry.Photo else "",
        "data": l,
        'name': qry.Name,
        'toid': request.session["userid"]
    })

def chat_send(request):
    data = json.loads(request.body)  # Parse JSON body
    msg = data.get('msg')
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.Message = message
    chatobt.To_id_id = toid
    chatobt.From_id_id = lid
    chatobt.Date = d
    chatobt.Time = datetime.datetime.now().strftime("%I:%M %p")
    chatobt.save()

    return JsonResponse({"status": "ok"})



def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime

    c=Chat()
    c.From_id_id=FROM_id
    c.To_id_id=TOID_id
    c.Message=msg
    c.Date=datetime.now()
    c.Time=datetime.now().strftime("%I:%M %p")

    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(From_id_id=fromid, To_id_id=toid) | Q(From_id_id=toid, To_id_id=fromid)).order_by('Date', 'Time')
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.Message, "from": i.From_id_id, "date": str(i.Date), "to": i.To_id_id, "time": str(i.Time)})



    return JsonResponse({"status":"ok",'data':l})

def forgotpasswordflutter(request):
    email = request.POST['email']
    try:
        user = User.objects.filter(email=email).first()
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    otp = random.randint(100000, 999999)
    PasswordResetOTP.objects.create(email=email, otp=otp)

    send_mail('Your Verification Code',
              f'Your verification code is {otp}',
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)
    return JsonResponse({'status': 'ok', 'message': 'OTP sent'})


def verifyOtpflutterPost(request):
    email = request.POST['email']
    entered_otp = request.POST['entered_otp']
    otp_obj = PasswordResetOTP.objects.filter(email=email).latest('created_at')
    if otp_obj.otp == entered_otp:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})


def changePasswordflutter(request):
    email = request.POST['email']
    newpassword = request.POST['newPassword']
    confirmPassword = request.POST['confirmPassword']
    if newpassword == confirmPassword:
        try:
            user = User.objects.filter(email=email).first()
            user.set_password(confirmPassword)
            user.save()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})


def delete_income(request):
    eid = request.POST['eid']
    Transaction.objects.get(id = eid).delete()
    return JsonResponse({'status': 'ok'})


def delete_reminder(request):
    eid = request.POST['eid']
    Reminder.objects.get(id = eid).delete()
    return JsonResponse({'status': 'ok'})

def delete_goal(request):
    eid = request.POST['eid']
    Goal.objects.get(id = eid).delete()
    return JsonResponse({'status': 'ok'})


def user_get_notification(request):
    print(request.POST,'  :   USerrrrr')
    lid = request.POST['lid']
    ob = Transaction.objects.filter(
        User__LOGIN_id=lid,
        Date__year=datetime.now().year,
        Date__month=datetime.now().month,
        Tan_type='Debit'
    ).aggregate(total=Sum('Amount'))['total'] or 0
    if ob>50000:
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        var = Notification.objects.filter(User__LOGIN_id=lid,Date=datetime.today())
        if len(var)>0:
            print('@@@@@@@@@@@@@@@@@@@@')

        else:
            ob1=Notification()
            ob1.User = User_table.objects.get(LOGIN__id=lid)
            ob1.Date =datetime.today()
            ob1.save()
            return JsonResponse({
                'status': 'ok',
                'type': 'me',
                'monthly_expense': ob
            })

    print('EEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    ob=Reminder.objects.filter(User__LOGIN__id=lid,Status='pending',reminder_date=datetime.today().date())
    if len(ob)>0:
        print('SSSSSSSSSSSSSS')
        ob1 = ob[0]
        ob1.Status='Viewed'
        ob1.save()
        return JsonResponse({
            'status': 'ok',
            'type': 'rem',
            'monthly_expense': str(ob1.Type)+" - "+str(ob1.Amount)
        })
    return JsonResponse({'status': 'NA'})







#
#
# #############graph######
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
# import numpy as np
# import pandas as pd
#
# def forecast_fn(x, y, degree=1, n_future=1):
#     df = pd.DataFrame({'Time': x, 'Value': y})
#     X = df[['Time']].values.reshape(-1, 1)
#     Y = df['Value'].values
#
#     # Transform features
#     poly = PolynomialFeatures(degree=degree)
#     X_poly = poly.fit_transform(X)
#
#     model = LinearRegression()
#     model.fit(X_poly, Y)
#
#     resultlist = []
#     for ii in range(1, n_future + 1):
#         future_time = X[-1, 0] + ii
#         print(future_time,"future_time")
#         ft_poly = poly.transform(np.array([[future_time]]))
#         pred = model.predict(ft_poly)
#         resultlist.append(pred[0])
#     return resultlist[0]