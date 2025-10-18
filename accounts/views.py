from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required, user_passes_test 

from .models import Account 

 

# --- Role Checks --- 

def is_admin(user): 

    return user.groups.filter(name="Admin").exists() 

 

def is_customer(user): 

    return user.groups.filter(name="Customer").exists() 

 

# --- Dashboards --- 

@login_required 

def dashboard(request): 
    """Redirect user to correct dashboard based on role"""
    if is_admin(request.user):
        return redirect('admin_dashboard')  # ✅ changes URL to /admin-dashboard/
    elif is_customer(request.user):
        return redirect('customer_dashboard')  # ✅ changes URL to /customer-dashboard/
    else:
        return render(request, 'accounts/no_role.html')  # ✅ stays on /dashboard/ 

 

@login_required 
@user_passes_test(is_admin) 
def admin_dashboard(request): 
    customers = Account.objects.all() 
    return render(request, 'accounts/admin_dashboard.html', {'customers': customers}) 

@login_required 
@user_passes_test(is_customer) 
def customer_dashboard(request): 
    account = Account.objects.get(user=request.user) 
    return render(request, 'accounts/customer_dashboard.html', {'account': account}) 