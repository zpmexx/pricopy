from .models import VisitStatistics
import datetime
from django.shortcuts import redirect

#parametry: site_name - nazwa strony odwiedzanej, time - czas do odswieżenia zapisu do bazu (domyślnie 15 minut)
def visit_statistic(request,site_name,time = 15): 
    time_to_next_db_add = time # czas w minutach do ponownego dodadani do bazy
    user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    if user_ip == "192.168.88.1":
        user_ip = "85.221.199.178"
    date = datetime.date.today()
    stat = VisitStatistics.objects.filter(ip = user_ip, visited_site = site_name, date = date).last()
    osversion = ""
    browserversion = ""
    try:
        osversion = request.user_agent.os.version_string
        browserversion = request.user_agent.browser.version_string
    except:
        pass

    if stat is None:
        VisitStatistics.objects.create(visited_site = site_name, ip = user_ip, system = request.user_agent.os.family+" "+osversion, browser = request.user_agent.browser.family+" "+browserversion)
    else:
        time_counter = time_to_next_db_add
        compare_time = (datetime.datetime.now() - datetime.timedelta(minutes=time_counter)).time()
        if stat.time <= compare_time:
            VisitStatistics.objects.create(visited_site = site_name, ip = user_ip, system = request.user_agent.os.family+" "+osversion, browser = request.user_agent.browser.family+" "+browserversion)
        else:
            pass
   
   
   
   
   
    # name = site_name #nazwa strony dodawana do statystyk
    # print("wcjpdze")
    # user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    # if testcookie == None:
    #     print('nie ma cookie tworze')
    #     response = redirect(redirect_site)
    #     response.set_cookie('last_sushi_visit','cookie zapisany',max_age=time * 60)
    #     VisitStatistics.objects.create(visited_site = name, ip = user_ip, system = request.user_agent.os.family, browser = request.user_agent.browser.family)
    #     return response
    # else:
    #     print('jest cookie')
    #     # print(request.COOKIES.get('test_cookie'))
    #     date = datetime.date.today()
    #     stat = VisitStatistics.objects.filter(ip = user_ip, visited_site = name, date = date).last()
    #     if stat is None:
    #         VisitStatistics.objects.create(visited_site = name, ip = user_ip, system = request.user_agent.os.family, browser = request.user_agent.browser.family)
    #         print('stworzone z braku znalezienia w bazie')
    #     else:
    #         print('sprawdzamy czasy')
    #         print(stat.time) 
    #         time_counter = time
    #         compare_time = (datetime.datetime.now() - datetime.timedelta(minutes=time_counter)).time()
    #         print(compare_time)
    #         if stat.time <= compare_time:
    #             # print('dodaje do bazy')
    #             VisitStatistics.objects.create(visited_site = name, ip = user_ip, system = request.user_agent.os.family, browser = request.user_agent.browser.family)
    #         else:
    #             pass
    #             print('nie dodaje bo czas')