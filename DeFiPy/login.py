'''login

semi gui login screen to add to scripts, usage: 

    session_info = login("./networks.json","./accounts.txt")

the session_info dict it returns will include your w3 and account object.

the networks.json file should look like this: 

{"network1": "RPC_FOR_NETWORK_1", etc... }

the accounts.txt file is AES encrypted by PwAES. Unencrypted it should look like this: 

{"wallet1":"PRIVATE_KEY_FOR_WALLET_1", etc... }

'''

from CursedUi import * 
from DeFiPy import * 
import curses 
import json

def login(networks_json,accounts_json):
    session_info = {}
    with open(networks_json) as infile:
        session_info["networks"] = json.load(infile)
    session_info["accounts_json"] = accounts_json
    session_info["tx_data"] = []
    session_info["connected"] = False
    def login_session_info (stdscr):
        login_ui(stdscr,session_info)
    curses.wrapper(login_session_info)
    return session_info


def login_onclick(menu,hint_box,menu_area,session_info,disp_area):
    def onclick () :
        logged_in = False
        try: 
            pw = menu.returnChoicesObject()["password"]
            wallets = aes_load_wallets(session_info["accounts_json"],False,False,pw)
            hint_box.addstr(0,1,"Login successful")
            logged_in = True 
        except:
            error_message = "incorrect password, press LEFT arrow and re-enter password."
            hint_box.clear()
            hint_box.addstr(0,1,error_message)
            hint_box.refresh()
        if logged_in:
            session_info["wallets"] = wallets
            menu.remove_items(["password","login_button"])
            menu.add_items([
                SelectItem(menu_area,"Account",list(wallets.keys()),1,1,"account_choice",label_width=8,item_width =15,hint_box=hint_box,parent_menu=menu),
                SelectItem(menu_area,"Network",list(session_info["networks"].keys()),2,1,"network_choice",label_width=8,item_width =15,hint_box=hint_box,parent_menu=menu),
                Button(menu_area,"connect","CONNECT","wait...",3,1,"connect_button",onClick= connect_onclick(menu,hint_box,menu_area,disp_area,session_info),onclick_finished_label = "connected",parent_menu=menu)
            ])
    return onclick
            
def connect_onclick (menu,hint_box,menu_area,disp_area,session_info):
    def onclick(): 
        choices = menu.returnChoicesObject() 
        hint_box.clear()
        hint_box.addstr(0,1,f"connecting {choices['account_choice']} on {choices['network_choice']}, please wait ...")
        hint_box.refresh()
        w3,account = connect_with_local_account(
            session_info["wallets"][choices["account_choice"]],
            rpc_url=session_info["networks"][choices["network_choice"]]["rpc"],
            POA=session_info["networks"][choices["network_choice"]]["POA"]
        )
        session_info["account"]=account
        session_info["network"]=choices["network_choice"]
        session_info["w3"]=w3
        
        hint_box.clear()
        hint_box.addstr(0,1,f"{choices['account_choice']} on {choices['network_choice']} (status = {'connected' if session_info['connected'] else 'disconnected'})")
        hint_box.refresh()

        connect_button = menu.getItemById("connect_button")
        connect_button.onclick_finished = True 
        connect_button.build()
        session_info["connected"] = w3.is_connected()
    return onclick
 
def mini_addr (addr) :
    return f"{addr[0:5]}...{addr[-4:]}"

def login_ui (stdscr, session_info):
    scr = setup_terminal(12,65)
    
    menu_area = CursedWindow(scr,5,64,0,0,title="Options",box=True,id="menu_area")
    disp_area = CursedWindow(scr,3,64,5,0,title="",box=True,id="disp_area")
    hint_box = CursedWindow(scr,1,64,8,0,"",False,False,id="hint_box")
    
    menu = SelectMenu(menu_area,[],hint_box=hint_box)
    
    menu.add_items([
        InputText(menu_area,"Password",1,1,26,"password",hint_box=hint_box,parent_menu=menu,hide_input=True),
        Button(menu_area,"LOGIN","LOGIN","LOADING",2,1,"login_button",login_onclick(menu,hint_box,menu_area,session_info,disp_area))
    ])

    disp_area.clear() 
    disp_area.addstr(1,1,"login and connect to chain")
    disp_area.refresh() 
    disp_area.box () 
    done = False 
    while not done: 
        menu_area.build()
        key = scr.getch()
        
        if key != curses.ERR:
            if chr(key) in ["q","Q"] and not menu.active_selector:
                done = True
            menu.get_choice(key)
        if session_info["connected"]:
            disp_area.addstr(1,1,f'{mini_addr(session_info["account"].address)} connected to {session_info["network"]}, accept? (hit y/n)')
            disp_area.refresh()
            disp_area.box()
            menu_area.build()
            done = chr(scr.getch()).lower() == "y"
            if not done: 
                disp_area.clear() 
                disp_area.addstr(1,1,"Select account and network")
                disp_area.refresh() 
                disp_area.box() 
                session_info["connected"] = False

    


    
    