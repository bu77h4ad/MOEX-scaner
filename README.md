# MOEX-scaner
Сканирует топ акции ММВБ на техническую перепроданность(RSI<30).  Подаёт уведомление. Сигнал для рассмотрения к покупке акции.

@bu77h4ad по всем вопросам

crontab -l
```python 

# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
#1 * * * 1-5 python3 ~/parser2.py 3600
1 0 * * 1-5   python3 ~/parser2.py -forse -indices -stocks 86400 -disable_notification
0 18 * * 7 python3 ~/parser2.py -forse -indices -stocks week

```
