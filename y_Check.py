from bs4 import BeautifulSoup as bs
import requests,lxml,json,random,os,sys,urllib3
from pytube import YouTube as yt
from time import sleep
import pandas as pd

def starter(vurl,vlist):
    urll = "https://www.youtube.com/watch?v="
    vlurl = "https://www.youtube.com/channel/"
    vuerror = "Enter Proper URL"
    if urll in vurl:
        if len(vurl) == 43:
            str_id=vurl[32:43]
            print("\n[+] VIDEO URL ok !")
        else:
            print(vuerror)
            sys.exit(0)      
    else:
        print(vuerror)
        sys.exit(0)
    vlerror = "Enter Proper Video #List Link"   
    if  vlurl in vlist:
        if len(vlist) == 63:
            print("[+] VIDEO List URL ok !\n")
            checker(vlist,urll,str_id)
        else:
            print(vlerror)
            sys.exit(0)
    else:
        print(vlerror)
        sys.exit(0)    
        
def checker(source,urll,str_id):
    with open("{}/Video_Key.csv".format(os.getcwd()), "w") as fw:fw.write(str_id)    
    countnum = 0
    berror = "They Blocked Temporarily...Try_Again_Later"
    global sel
    while True:
        agent = {'User-Agent':"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"}
        urllib3.disable_warnings()
        try:
            req = requests.get(url=source,headers=agent,verify=False,timeout=6)
            req.close()
        except requests.exceptions.ConnectionError:
            print("CHECK internet Connection...!")
            None
        except requests.exceptions.ReadTimeout:
            print("Time_Out_{}".format(berror))
            sys.exit(0)
        soup = bs(req.content, 'lxml')
        try:
            aum =  soup.find_all("div", {'id': 'initial-data'})[0] 
            jsn = json.loads(aum.string)
        except Exception:
            print("No_Data_{}".format(berror))
            sys.exit(0)
        sle=jsn["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][1]
        itm =sle["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]
        holder=[]
        for tmp in range(30):
            try:
                con3 = itm["contents"][tmp]
                fil= [con3["compactVideoRenderer"]["title"]["runs"][0]["text"]]
                fi = con3["compactVideoRenderer"]["videoId"]
                holder.append(fi)
            except IndexError:pass
        newfile = pd.DataFrame({"chan":holder})
        with open("{}/Video_Key.csv".format(os.getcwd()), "r") as fl:
            fle=fl.readlines()
            chh = fle[0]
            sam = newfile[newfile["chan"].str.contains(chh)]
            ttt = sam.T
        try:
            amount=int(ttt.columns[0])
            countnum = countnum+1
            print("COUNT:[{}] | [{}]:Videos Found !".format(countnum,amount),end="\r")
            newlink = newfile.head(amount)
            linkss =[]
            unq=[]
            for f,lk in newlink.iterrows():
                unq.append(lk['chan'])
                linkss.append(urll+str(lk["chan"]))
            for tf in linkss:
                print("\n{}Plz wait it Downloading...".format("\t"*2),end="\r")
                try:
                    urls = yt(tf).streams.all()
                    sep = urls[0]
                    red = sep.default_filename[:35]
                    sep.download('{}'.format(os.getcwd()),filename=red)
                except pytube.exceptions.VideoUnavailable:
                    print("They Upload properly {}".format(tf))
                    None
                except pytube.exceptions.RegexMatchError:
                    print("URL pattern NOT fit...! {}".format(tf))
                    None
                print("{}DownLoaded!!!".format(" "*30))
                asc = unq[0]
                with open("{}/Video_Key.csv".format(os.getcwd()), "w") as fw:fw.write(asc)
        except IndexError:None
        sleep(int(random.randint(6,18)))
def banner():
    a = "\t"*5
    b = "CREATED by : நரேந்திரன் "
    c = "Videos_Continer"
    titl = """
▓██   ██▓       ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀
 ▒██  ██▒      ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ 
  ▒██ ██░      ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ 
  ░ ▐██▓░      ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ 
  ░ ██▒▓░      ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄
   ██▒▒▒       ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒
 ▓██ ░▒░         ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░
 ▒ ▒ ░░        ░         ░  ░░ ░   ░   ░        ░ ░░ ░ 
 ░ ░           ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░   
 ░ ░           ░                       ░               """
    print(titl,"\n",a,b)
    try:
        os.mkdir("{}/{}".format(os.getcwd(),c))
    except FileExistsError:None
    os.chdir(c)
    starter(input("\n[#] URL > "), input("[#] VIDEOS List Link > "))

if __name__ == "__main__":
    try:
        banner()
    except KeyboardInterrupt:
        print("{}நன்றி _/\_ வணக்கம்".format("\n\t"))
        sys.exit(0)
