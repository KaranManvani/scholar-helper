from flask_apscheduler import APScheduler


from website import app
from website.schedules import insert_into_db


scheduler = APScheduler()

scheduler.add_job(id = 'task1', func = insert_into_db, args = ['s4d_international'], trigger = 'cron', minute = 0, hour = 4)
scheduler.add_job(id = 'task2', func = insert_into_db, args = ['b4s_international_ao'], trigger = 'cron', minute = 30, hour = 4)
scheduler.add_job(id = 'task3', func = insert_into_db, args = ['b4s_international'], trigger = 'cron', minute = 0, hour = 5)
scheduler.add_job(id = 'task4', func = insert_into_db, args = ['b4s_girls_ao'], trigger = 'cron', minute = 30, hour = 5)
scheduler.add_job(id = 'task5', func = insert_into_db, args = ['b4s_girls'], trigger = 'cron', minute = 0, hour = 6)
scheduler.add_job(id = 'task6', func = insert_into_db, args = ['b4s_gov_uc'], trigger = 'cron', minute = 30, hour = 6)
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, use_reloader=False)
    # app.run(host='0.0.0.0', debug=True, use_reloader=False)
    # app.run()

    # app.run(host='0.0.0.0', debug=True)
    # app.run(host='0.0.0.0', debug=False)
