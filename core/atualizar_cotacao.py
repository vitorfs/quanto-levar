import urllib2
from datetime import datetime, timedelta
from models import Cotacao

def atualizar_cotacao():
    now = datetime.now() - timedelta(days=1)
    data = now.strftime('%Y%m%d')
    url = u'http://www4.bcb.gov.br/Download/fechamento/{0}.csv'.format(data)
    response = urllib2.urlopen(url)
    csv = response.read()
    rows = csv.split('\n')

    for row in rows:
        cols = row.split(';')
        for col in cols:
            print col

atualizar_cotacao()
