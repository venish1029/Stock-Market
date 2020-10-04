from django.shortcuts import render


from django.shortcuts import render,HttpResponse,redirect
from bsedata.bse import BSE
from django.views.decorators.csrf import csrf_exempt
from .models import users,share_owner,sell_data_table
import json
from django.http import JsonResponse


@csrf_exempt
def index(request):
    b = BSE(update_codes = True)
    data_gainer_company=b.topGainers()
    data_looser_company=b.topLosers()
    company=[]
    for i in data_gainer_company:
        company.append(b.getQuote(i['scripCode']))
    for i in data_looser_company:
        company.append(b.getQuote(i['scripCode']))
    if(request.method=='POST'):
        d=request.POST['search_items']
        data=b.getQuote(d)
        search_items=True
        return render(request,'index.html',{'data_gainer_company':data_gainer_company,'data_looser_company':data_looser_company,'search_data':data,'search_items':search_items})
    else:
        main_page=True
        return render(request,'index.html',{'data_gainer_company':data_gainer_company,'data_looser_company':data_looser_company,'company':company,'main_page':main_page})

@csrf_exempt
def user_login(request):
    if(request.method=='POST'):
        try:
            first_name=request.POST['first_name_signup']
            last_name=request.POST['last_name_signup']
            email=request.POST['email_signup']
            mobile=request.POST['mobile_signup']
            password=request.POST['password_signup']

            if(users.objects.filter(gmail=email)):
                sign_up_sucess=False
                email_already=True
                login_problem=False
                return render(request,'user_login.html',{'sign_up_sucess':sign_up_sucess,'email_already':email_already,'login_problem':login_problem})
            else:
                users.objects.create(user_first_name=first_name,user_last_name=last_name,password=password,mobile=mobile,gmail=email).save()
                sign_up_sucess=True
                email_already=False
                login_problem=False
                return render(request,'user_login.html',{'sign_up_sucess':sign_up_sucess,'email_already':email_already,'login_problem':login_problem})
        except:
            email=request.POST["email_login"]
            password=request.POST["password_login"]
            u=users.objects.filter(gmail=email,password=password)
            if(len(u)>0):
                request.session['gmail']=email
                details=users.objects.get(gmail=email)
                data=share_owner.objects.filter(user_gmail=email)
                dictionary_items={}
                b=BSE()
                total_in_table=0
                total_in_actual=0
                for i in data:
                    if(i.company_code in dictionary_items.keys()):
                        dictionary_items[i.company_code][2]=dictionary_items[i.company_code][2]+i.share_quntity
                    else:
                        dictionary_items[i.company_code]=[i.company_code,i.company_name,i.share_quntity]
                    total_in_actual+=float(b.getQuote(i.company_code)['currentValue'])*i.share_quntity
                    total_in_table=total_in_table+i.total
                total_profit=int(total_in_actual-total_in_table)
                return render(request,'admin_Homepage.html',{'details':details,'data':dictionary_items,'profit':total_profit})
            else:
                sign_up_sucess=False
                email_already=False
                login_problem=True
                return render(request,'user_login.html',{'sign_up_sucess':sign_up_sucess,'email_already':email_already,'login_problem':login_problem})
    else:
        sign_up_sucess=False
        email_already=False
        login_problem=False
        return render(request,'user_login.html',{'sign_up_sucess':sign_up_sucess,'email_already':email_already,'login_problem':login_problem})

@csrf_exempt
def admin_Homepage(request):
    email=request.session['gmail']
    details=users.objects.get(gmail=email)
    data=share_owner.objects.filter(user_gmail=email)
    b=BSE()
    total_in_table=0
    total_in_actual=0
    dictionary_items={}
    for i in data:
        if(i.company_code in dictionary_items.keys()):
            dictionary_items[i.company_code][2]=dictionary_items[i.company_code][2]+i.share_quntity
        else:
            dictionary_items[i.company_code]=[i.company_code,i.company_name,i.share_quntity]
        total_in_actual+=float(b.getQuote(i.company_code)['currentValue'])*i.share_quntity
        total_in_table=total_in_table+i.total
    total_profit=int(total_in_actual-total_in_table)
    print(total_in_table)
    
    return render(request,'admin_Homepage.html',{'details':details,'data':dictionary_items,'profit':total_profit})

@csrf_exempt
def search_save(request):
    search_items=request.POST['search_items']
    print(search_items)
    b=BSE()
    search_data=b.getQuote(search_items)
    return render(request,'search_save.html',{'search_data':search_data})

@csrf_exempt
def save_details(request,code):
    no_of_quntity=request.POST['no_of_quantity']
    price=float(request.POST['price_of_share'])
    date=request.POST['select_date']

    b=BSE()
    data=b.getQuote(code)
    comany_name=data['companyName']
   
    total=int(int(no_of_quntity)*float(price))
    company_data={'code':code,'no_of_quntity':no_of_quntity,'price':price,'total':total}
    share_owner.objects.create(user_gmail=request.session['gmail'],date=date,company_code=code,company_name=comany_name,share_quntity=no_of_quntity,share_price=price,total=int(total)).save()
    return render(request,'search_save.html',{'search_data':data,'company_data':company_data})

@csrf_exempt
def search_data(request,code):
    email=request.session['gmail']
    details=users.objects.get(gmail=email)
    data=share_owner.objects.filter(user_gmail=email)
    dictionary_items={}
    b=BSE()
    total_in_table=0
    total_in_actual=0
    for i in data:
        if(i.company_code in dictionary_items.keys()):
            dictionary_items[i.company_code][2]=dictionary_items[i.company_code][2]+i.share_quntity
        else:
            dictionary_items[i.company_code]=[i.company_code,i.company_name,i.share_quntity]
        total_in_actual+=float(b.getQuote(i.company_code)['currentValue'])*i.share_quntity
        total_in_table=total_in_table+i.total
    total_profit=int(total_in_actual-total_in_table)
    gmail=request.session['gmail']
    data_owner=share_owner.objects.filter(user_gmail=gmail,company_code=code)
    for i in data_owner:
        i.date=str(i.date)
    return render(request,'admin_Homepage.html',{'details':details,'data':dictionary_items,'data_owner':data_owner,'profit':total_profit})

@csrf_exempt
def sell_items(request,code):
    gamil=request.session['gmail']
    sell_quantity=request.POST['sell_quentity']
    sell_date=request.POST['sell_date']
    sell_price=request.POST['sell_price']
    data=share_owner.objects.filter(id=code)
    buy_price=data[0].share_price
    sell_profit=(int(sell_price)*int(sell_quantity))-(int(buy_price)*int(sell_quantity))
    total_sell=int(sell_quantity)*int(sell_price)

    sell_data_table.objects.create(user_gmail=gamil,company_code=data[0].company_code,company_name=data[0].company_name,buy_date=data[0].date,sell_date=sell_date,buy_price=data[0].share_price,sell_price=int(sell_price),total_sell_price=total_sell,total_profit=sell_profit,sell_quntity=int(sell_quantity)).save()

    if(data[0].share_quntity==int(sell_quantity)):
        share_owner.objects.filter(id=code).delete()
    else:
        ob=share_owner.objects.get(id=code)
        ob.share_quntity=ob.share_quntity-int(sell_quantity)
        ob.save()

    email=request.session['gmail']
    details=users.objects.get(gmail=email)
    data=share_owner.objects.filter(user_gmail=email)
    b=BSE()
    total_in_table=0
    total_in_actual=0
    dictionary_items={}
    for i in data:
        if(i.company_code in dictionary_items.keys()):
            dictionary_items[i.company_code][2]=dictionary_items[i.company_code][2]+i.share_quntity
        else:
            dictionary_items[i.company_code]=[i.company_code,i.company_name,i.share_quntity]
        total_in_actual+=float(b.getQuote(i.company_code)['currentValue'])*i.share_quntity
        total_in_table=total_in_table+i.total
    total_profit=int(total_in_actual-total_in_table)
    return render(request,'admin_Homepage.html',{'details':details,'data':dictionary_items,'profit':total_profit})

@csrf_exempt
def detail(request):
    gmail=request.session['gmail']
    data=sell_data_table.objects.filter(user_gmail=gmail)
    return render(request,'details.html',{'data':data})