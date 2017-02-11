import sys,argparse,os
from time import sleep 
from qlib.net import to
from qlib.log import LogControl as L
from qlib.asyn.daemon import run,restart, stop

host = 'fanyi.baidu.com/v2transapi'
data_tem = {
    'from': 'auto',
    'to': 'zh',
    'query': None,
    'transtype':'translang', 
    'simple_means_flag':'3',
}
old = ''
def read_msg():
    global old
    msg = os.popen("pbpaste").read()
    if msg != old:
        old = msg
        return msg


# msg = ' '.join(sys.argv[1:])


def brun():
    while True:
        sleep(1)
        msg = read_msg()
        if not msg:
            continue
        data_tem['query'] = msg
        res = to(host, method='post',data=data_tem)
        for data in res.json()['trans_result']['data']:
            L.i("\n",data['dst'])
            to("http://localhost:8080/",data=data,method='post')


def get_args():
    DOC = """
    a translation backend .
    """
    parser = argparse.ArgumentParser(usage="how to use this", description=DOC)
    parser.add_argument("-s", "--start", default=False, action="store_true",help="set start")
    parser.add_argument("-k", "--stop", default=False,  action="store_true",help="set stop")
    parser.add_argument("-r", "--restart", default=False, action="store_true", help="set restart")
    
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.start:
        run(brun)
    elif args.stop:
        stop(brun)
    elif args.restart:
        restart(brun)