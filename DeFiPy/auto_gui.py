'''Auto GUI 

Generate user graphical interface for smart contracts automatically given its address and abi

Script
======
Run as a script with:
  python -m DeFiPy.auto_gui arg1 arg2 arg3

takes 3 args: 
1. contracts_json : path to contracts file. A json formatted like this:
    [{'name':'contract1','abi':ABI,'address':'0xADDRESS'},{'name': etc.. }]
2. networks_json : path to networks file. A json formatted like this:
    {'network1':RPC1,'network2':RPC2}
3. accounts_txt : path to text file encrypted by PwAES, unencrypted it's a 
    json formatted like this:
    {'account1':PRIVATE_KEY_1,'account2':PRIVATE_KEY_2}


'''

import tkinter as tk
from tkinter import ttk
from DeFiPy import aes_load_wallets, attach, fix_args, get_functions, connect_with_local_account
import json
    

def fn_call_onclick(w3,fn,contract_info,args,value):
    cur_contrat = attach(w3,contract_info["address"],contract_info["abi"])
    callable = getattr(cur_contrat.functions, fn["name"])
    if fn["stateMutability"] == 'view':
        if fn["inputs"] != "":
            args = json.loads(f"[{args}]")
            print(args)
            args = fix_args(w3,args)
            tx = callable(*args).call()
        else: 
            tx = callable().call()
    else: 
        tx_data = f'{{"value":{value},"gasPrice":{w3.eth_gas_price} }}'
        if fn["inputs"] != "":
            args = json.loads(f"[{args}]")
            print(args)
            args = fix_args(w3,args)
            tx = callable(*args).trasnact(tx_data)
        else: 
            tx = callable().transact(tx_data)
    tx_out = tk.Text(window,width = 70,height = 4,background = "#44475a",foreground = "#ffb86c")

    tx_out.insert("end",chars = f"tx output:\n{tx}")
    tx_out.configure(state = "disabled")
    tx_out.pack(pady=5)
    

def select_fn_onclick(functions,functions_box,session_info,contract_info):
    fn = functions[functions_box.get()]
    fn_sig = tk.Text(window,width = 70,height = 4,background = "#44475a",foreground = "#ffb86c")
    fn_sig.insert("end",chars = f"function signature:\n{fn['name']}({fn['inputs']}) \nreturns({fn['outputs']}) \npayable: {str(fn['payable'])}")
    fn_sig.configure(state = "disabled")
    fn_sig.pack(pady=5)

    pay_label =tk.Label(window, text= 'Payable function, enter value (wei)',background="#282a36",foreground="#f8f8f2")
    pay_input = tk.Entry(window,width= 70,relief='flat',background = "#44475a",foreground = "#ffb86c")
    pay_input.insert("end","0")
    if fn["payable"]:
        pay_label.pack() 
        pay_input.pack()

    arg_label = tk.Label(window, text= 'Enter args with double quotes, separated by comma ( , )',background="#282a36",foreground="#f8f8f2")
    arg_label.pack() 
    fn_input_frame = tk.Frame(window,background='#282a36')
    fn_input = tk.Entry(fn_input_frame,width= 70,relief='flat',background = "#44475a",foreground = "#ffb86c")
    fn_input.grid(column=0,row=0)
    fn_call_button = tk.Button(fn_input_frame,text="execute",width = 10,pady=5,height=1,relief="flat",background="#6272a4",foreground="#50fa7b",activebackground="#6272a4",activeforeground="#f1fa8c",
        command = lambda : fn_call_onclick(session_info["w3"],fn,contract_info,fn_input.get(),pay_input.get()) )
    fn_call_button.grid(column=0,row=1)
    fn_input_frame.pack()



def contract_onclick (window,contracts,contract_box,contract_names,session_info):
    contract_info = contracts[contract_names[contract_box.get()]]
    functions = get_functions(contract_info["abi"])
    functions_frame = tk.Frame(window,background= "#282a36")
    functions_box = ttk.Combobox(functions_frame, state="readonly", values = list(functions.keys()))
    functions_box.grid(column=0,row=0)
    functions_button= tk.Button(functions_frame,text="select function",background="#6272a4",foreground="#50fa7b",
        command=lambda : select_fn_onclick(functions,functions_box,session_info,contract_info) )
    functions_button.grid(column=1,row =0,padx=5)
    functions_frame.pack() 

def delete_section (window,exclude_array):
    for w in window.winfo_children():
        if w not in exclude_array: w.destroy() 

def connect_onclick (window,wallets,wallet_box,net_box,session_info,contracts,autoui_title,login_message,connect_frame): 
    w3, account = connect_with_local_account(wallets[wallet_box.get()],networks[net_box.get()]["rpc"],networks[net_box.get()]["POA"],False)
    session_info["w3"] = w3
    session_info["account"] = account 
    if w3.is_connected(): 
        delete_section(window,[autoui_title,login_message,connect_frame])
        contract_message = tk.Label(window,text = "Contract",background="#282a36",foreground="#f1fa8c",font=heading_font)
        contract_message.pack() 

        contract_frame = tk.Frame(window,background= "#282a36")
        contract_names = {x["name"]:i for i,x in enumerate(contracts)}
        contract_box = ttk.Combobox(contract_frame, state="readonly", values = list(contract_names.keys()))
        contract_box.grid(column=0,row=0)
        contract_button= tk.Button(contract_frame,text="load contract",background="#6272a4",foreground="#50fa7b",
            command = lambda : contract_onclick (window,contracts,contract_box,contract_names,session_info))
        contract_button.grid(column=1,row =0, padx=5,pady = 10)
        contract_refresh = tk.Button(text="refresh",width = 10,height=1,relief="flat",
            command=lambda : delete_section(window,[autoui_title,login_message,connect_frame,contract_message,contract_refresh,contract_frame]),background="#6272a4",foreground="#50fa7b",activebackground="#6272a4",activeforeground="#f1fa8c")
        contract_refresh.pack()
        
        contract_frame.pack() 
    else: 
        woops = tk.Label(window,text = f"try again ... ")
        woops.pack() 



def login_onclick (window,accounts_path,networks,autoui_title):
    try : 
        wallets = aes_load_wallets(accounts_path,False,False,pw_entry.get())

        for w in window.winfo_children(): 
            if w != autoui_title:
                w.destroy() 

        login_message = tk.Label(window,text = "Connect to network",background="#282a36",foreground="#f1fa8c",font=heading_font)
        login_message.pack() 

        connect_frame = tk.Frame(window,background= "#282a36")
        #wallet_choose = tk.Label(connect_frame,text="Wallet",background="#282a36",foreground="#f8f8f2")
        #wallet_choose.grid(column=0,row =0)
        wallet_box = ttk.Combobox(connect_frame, state="readonly", values = list(wallets.keys()))
        wallet_box.grid(column=0,row=0,padx=5)
        #net_choose = tk.Label(connect_frame,text="Network",background="#282a36",foreground="#f8f8f2")
        #net_choose.grid(column=0,row =1)
        net_box = ttk.Combobox(connect_frame, state="readonly", values = list(networks.keys()))
        net_box.grid(column=1,row=0)
        connect_button = tk.Button(connect_frame,text = "connect",background="#6272a4",foreground="#50fa7b",
            command=lambda : connect_onclick (window,wallets,wallet_box,net_box,session_info,contracts,autoui_title,login_message,connect_frame))
        connect_button.grid(column=2,row=0,padx=5,pady=5)
        connect_frame.pack() 

    except Exception as e: 
        login_message.pack_forget()
        print(e)
        login_message = tk.Label(window,text = f"login failed {e}",background="#282a36",foreground="#f8f8f2")
        login_message.pack() 

if __name__ == '__main__': 
    
    import sys 

    if len(sys.argv) != 4 or sys.argv[1].lower in ["-h","--h","-help","--help"]:
        print(__doc__)
        input("hit return to exit .. ")
        exit() 

    contracts_json_path = sys.argv[1]
    networks_json_path = sys.argv[2]
    accounts_path = sys.argv[3]

    session_info = {} 
    title_font = ("courier",20,"bold") 
    heading_font = ("courier",15,"bold") 

    wallets = None 
    with open (networks_json_path,"r") as infile: 
        networks = json.load(infile)
    with open (contracts_json_path,"r") as infile: 
        contracts = json.load(infile)

    window = tk.Tk() 
    window.geometry("720x640")
    window.configure(bg="#282a36")

    autoui_title = tk.Label(window,text="Auto UI",
        font = title_font,background="#282a36",
        foreground="#f8f8f2")
    autoui_title.pack() 

    login_label = tk.Label(window,text = "Login",bg="#282a36",fg="#f1fa8c",font=heading_font)
    login_label.pack() 
    pw_entry = tk.Entry(window,show="*",width= 20,relief='flat',background = "#44475a",foreground = "#ffb86c")
    pw_entry.pack() 
    login_button = tk.Button(text="submit",width = 10,height=1,relief="flat",command=lambda : login_onclick(window,accounts_path,networks,autoui_title),background="#6272a4",foreground="#50fa7b",activebackground="#6272a4",activeforeground="#f1fa8c")
    login_button.pack(pady = 10)

    window.mainloop()