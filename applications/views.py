from django.shortcuts import render, redirect, get_object_or_404
from .models import JobApplication


def home(request):
    applications = JobApplication.objects.all().order_by("-applied_date")

    search = request.GET.get("search", "")
    status = request.GET.get("status", "")

    if search:
        applications = applications.filter(
            company_name__icontains=search
        )

    if status:
        applications = applications.filter(status=status)

    total = JobApplication.objects.count()
    applied = JobApplication.objects.filter(status="Applied").count()
    interviews = JobApplication.objects.filter(status="Interview").count()
    selected = JobApplication.objects.filter(status="Selected").count()
    rejected = JobApplication.objects.filter(status="Rejected").count()

    return render(request, "applications/home.html", {
        "applications": applications,
        "total": total,
        "applied": applied,
        "interviews": interviews,
        "selected": selected,
        "rejected": rejected,
        "search": search,
        "status": status,
    })

def add_application(request):
    if request.method == "POST":
        company_name = request.POST["company_name"]
        job_position = request.POST["job_position"]
        applied_date = request.POST["applied_date"]
        status = request.POST["status"]

        JobApplication.objects.create(
            company_name=company_name,
            job_position=job_position,
            applied_date=applied_date,
            status=status
        )

        return redirect("home")

    return render(request, "applications/add_application.html")


def edit_application(request, id):
    application = get_object_or_404(JobApplication, id=id)

    if request.method == "POST":
        application.company_name = request.POST["company_name"]
        application.job_position = request.POST["job_position"]
        application.applied_date = request.POST["applied_date"]
        application.status = request.POST["status"]

        application.save()

        return redirect("home")

    return render(request, "applications/edit_application.html", {
        "application": application
    })


def delete_application(request, id):
    application = get_object_or_404(JobApplication, id=id)

    if request.method == "POST":
        application.delete()
        return redirect("home")

    return render(request, "applications/delete_application.html", {
        "application": application
    })