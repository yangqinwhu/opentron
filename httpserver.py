#http server
import socketserver
from http.server import BaseHTTPRequestHandler,HTTPServer
from threading import Thread
import sys,json
# sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")
server_ip = "192.168.1.46"
server_ip = "127.0.0.1"
PORT = 8000



class DispatchMeta(type):
    """
    NOT USED ANYMORE
    enable dispatch class function to a new name using dispatch."""
    def __new__(meta,name,bases,dct):
        for k in list(dct.keys()):
            item = dct[k]
            if getattr(item,'isDispatchMethod',None):
                dct[item.__name__] = dct.pop(k)
        return super(DispatchMeta, meta).__new__(meta, name, bases, dct)


def dispatch(instance,path,):
    """
    NOT USED ANYMORE
    msg format: {
        action: methodName/tag1/tag2,
        other key:value pairs will also be passed to method.
    }
    route an action to instance dispatchers
    """
    methodName = path
    method = getattr(instance,methodName,None)
    if method==None:
        raise KeyError(f'Method <{methodName}> was not found on <{instance.__class__.__name__}>.')
    return method()



class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        print('got request')
        # do something here with another thread

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('hello world'.encode())

class SimpleHandler(BaseHTTPRequestHandler,):

    def json(self):
        "return json dict or empty dict"
        if self.headers['Content-Length']:
            return json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode())
        return {}

    def abort404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<h1>PAGE NOT FOUND.</h1>'.encode())

    def sendData(self,data,header,cache=True):
        self.send_response(200)
        self.send_header("Content-type", header)
        # FIXME: remove dev testing.
        self.end_headers()
        self.wfile.write(data.encode())

    def sendCSS(self,css):
        self.sendData(css,'text/css')
    def sendHTML(self,html):
        self.sendData(html,'text/html')
    def sendJS(self,js):
        self.sendData(js,'application/javascript')
    def sendMAP(self,js):
        self.sendData(js,'application/json')

    def do_GET(self):
        """Respond to a GET request."""
        try:
            # redirect / to /index
            path = self.path.strip('/') or 'index'
            print(path)
            jsondata = self.json()
            print(jsondata)
            # self.sendHTML('<h1>hello world</h1>')
            self.sendMAP(json.dumps(jsondata))
        except:
            # if not defined, try to look for raw html pate.
            self.sendFileOr404(path)

    def do_POST(self):
        "respond to post request"
        self.logger.main.peripheral.led.show('wifi',[50,1],1,)

        try:
            # redirect / to /index
            path = self.path.strip('/') or 'index'
            dispatch(self,path=path)
        except:
            # if not defined, try to look for raw html pate.
            self.sendFileOr404(path)

    def sendFileOr404(self,filePath,mode='html'):
       return self.abort404()




with HTTPServer((server_ip, PORT), SimpleHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
