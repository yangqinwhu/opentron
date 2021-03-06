#http server
"""
Note:If you need to control gpios, first stop the robot server with systemctl stop opentrons-robot-server.
Until you restart the server with systemctl start opentrons-robot-server, you will be unable to control the robot using the Opentrons app.
"""
import socketserver
from http.server import BaseHTTPRequestHandler,HTTPServer

from threading import Thread
import sys,json,time
# import ams_protocols.saliva_to_dtt as saliva_to_dtt
# import ams_protocols.sample_to_lamp_96well as sample_to_lamp_96well
import ams_protocols.p200_aliquot_beta as p200_aliquot
# sys.path.append("/var/lib/jupyter/notebooks")
sys.path.append("/Users/chunxiao/Dropbox/python/aptitude_project/opentron")
# server_ip = "192.168.1.46"
server_ip = "127.0.0.1"
PORT = 8000
DEV=True if server_ip == "127.0.0.1" else False
# Status_reset_t




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
            if path =="init_robot":
                self.init_robot()
                self.sendData(f"*** Robot initializing *** \n",'text/html')
                # self.sendMAP(json.dumps(self.robot.deck_plan))
            elif path =="run_robot":
                self.run_robot()
                self.sendData("*** Run started *** \n",'text/html')
            elif path =="pause":
                self.pause_robot()
                self.sendData("*** Run paused *** \n",'text/html')
            elif path =="resume":
                self.pause_robot()
                self.sendData("*** Run paused *** \n",'text/html')
            elif path=="get_status":
                self.get_status()
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

    def run_robot(self):
        to_do="run"
        jsondata = self.json()
        self.Q.put(to_do)
        self.Q.put(jsondata)
        # self.robot.initialize(jsondata)
        # self.robot.run(jsondata)

    def init_robot(self):
        to_do="initialize"
        jsondata = self.json()
        self.Q.put(to_do)
        self.Q.put(jsondata)
        # self.robot.initialize(jsondata)
        # self.robot.run(jsondata)

    def pause_robot(self):
        to_do="pause"
        jsondata = self.json()
        self.Q.put(to_do)
        self.Q.put(jsondata)
        # self.robot.initialize(jsondata)
        # self.robot.run(jsondata)
    def resume_robot(self):
        to_do="resume"
        jsondata = self.json()
        self.Q.put(to_do)
        self.Q.put(jsondata)

    def get_status(self):
        self.send_response(300)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.robot.status.encode())

class RunRobot:
    def __init__(self):
        self.prot=""
        self.status="IDLE"
        self.deck_plan={1:"Deck not initialized"}
    def sele(self,name):
        self.prot = name
    def initialize(self,jsondata):
        if jsondata["protocol"]["file"]=="p200_aliquot":
            self.prot=p200_aliquot
            self.prot.initialize_robot(**jsondata)

    def run(self,jsondata):
        if jsondata["robot_status"]["to_run"]:
            # self.status = "Running"
            self.prot.run(**jsondata)
            # self.status = "Run FINISHED"
            # time.sleep(1)
            # self.status = "Run done" # This is to remove the FINISHED, which is used in opentron APP
    def pause(self):
        self.prot.pause_robot()
        self.status = "Run Paused"
    def resume(self):
        self.prot.resume_robot()



def startserver():
    with HTTPServer((server_ip, PORT), SimpleHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()



from queue import Queue
msq = Queue()
robot = RunRobot()
SimpleHandler.robot=robot
SimpleHandler.Q=msq

Thread(target=startserver).start()

while True:
    if msq.empty():
        time.sleep(0.1)
        continue
    to_do= msq.get()
    jsondata =msq.get()
    if to_do =="initialize":
        robot.status="BUSY"
        try:
            robot.initialize(jsondata)
            robot.status="IDLE"
        except Exception as e:
            print (e)
            robot.status="Robot Error"
    elif to_do =="run":
        robot.status="BUSY"
        try:
            robot.run(jsondata)
            robot.status="IDLE"
        except Exception as e:
            print (e)
            robot.status="Robot Error"
    elif to_do=="pause":
        robot.pause()
    elif to_do=="resume":
        robot.resume()
