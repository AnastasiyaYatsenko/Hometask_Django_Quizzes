from celery import shared_task
import csv

from quiz.models import TestrunStat
from pprint import pprint


@shared_task
def report():
    testrun_stat_qs = TestrunStat.objects.all()
    tr_stat = list(testrun_stat_qs.values("test_name", "full_answer", "percentage"))
    header = ['test_name', 'full_answer', 'percentage']
    pprint(header)
    keys = tr_stat[0].keys()
    with open('statistics.csv', 'w', encoding='UTF8', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tr_stat)
        stats = list(TestrunStat.objects.values_list('id', flat=True))
        for stat_id in stats:
            ts = TestrunStat.objects.get(pk=stat_id)
            ts.full_answer = 0
            ts.total_runs = 0
            ts.percentage = 0
            ts.save()
