#Importaciones
import tkinter
import mysql.connector
from datetime import date, datetime
import random

#App de Banco
class AppBanco:        
    
    #Constructor
    def __init__(self):
        
        #Conecxion con MySQL
        self.client = mysql.connector.connect(host='localhost',
                                              database='bank', 
                                              user='root', password='')
        
        query = "select ID from atm"
        cursor = self.client.cursor()
        cursor.execute(query)
        
        self.atms = cursor.fetchall()
        self.atm_num = len(self.atms)
        
        
        self.createdUser = False
        self.createdRepairman = False
        
        self.destroyedWindow = False
        
        self.createdWithdraw = False
        self.createdDeposit = False
        self.createdTransfer = False
        self.createdState = False
        
        #Iniciar ventana de inicio
        self.logIn()
    
    #--------------------------------------------------------------------------

#Ventanas     

    #Ventana inical
    def logIn(self):
        
        #Creación de la ventana
        self.principal = tkinter.Tk()
        self.principal.title("Inicio de sesión")
        self.principal.geometry("300x240+300+250")
        
        #Mensaje de bienvenida
        lbl01 = tkinter.Label(self.principal, text = "Bienvenido a Banco UP")
        lbl01.place(x = 80, y = 30)
        
        #Campo de entrada del usuario
        lbl02 = tkinter.Label(self.principal, text = "Usuario: ")
        lbl02.place(x = 20, y = 100)
        
        self.writeUser = tkinter.Entry(self.principal , bg = "lightgray", width = 25)
        self.writeUser.place(x = 100, y = 100)  
        
        
        #Campo de entrada de la contraseña
        lbl03 = tkinter.Label(self.principal, text = "Contrasena: ")
        lbl03.place(x = 20, y = 130)
    
        self.writePassword = tkinter.Entry(self.principal , bg = "lightgray", width = 25)
        self.writePassword.place(x = 100, y = 130)  
        
        #Boton de Iniciar sesión
        btn01 = tkinter.Button(self.principal, text = "Iniciar sesion", 
                               command = self.verification)
        btn01.place(x = 125, y = 190, width = 75)
        
        #Para que no se cierre la ventana
        self.principal.mainloop()
        return
        
    #Contraseña incorrecta
    def wrongPassword(self):
        tkinter.messagebox.showerror( title = "Accesso no autorizado", 
                                     message = "Contraseña incorrecta")
        return
        
    #Ventana del usuario
    def userPanel(self):
        self.destroyedWindow = False
        self.createdUser = True
        self.accounts = self.getAccounts()
        
        #Creacion de la ventana
        self.panel_usuario = tkinter.Tk()
        self.panel_usuario.title("Pagina principal")
        self.panel_usuario.geometry("300x{}+100+150".format(
            250+30*len(self.accounts)))
        
        #Mensaje de bienvenida
        lbl01 = tkinter.Label(self.panel_usuario, text="Bienvenido {}".format(
            self.user_name))
        lbl01.place( x = 90, y = 20 )
        
        #Instrucciones
        lbl02 = tkinter.Label(self.panel_usuario, 
                              text="Por favor seleccione una de sus cuentas")
        lbl02.place( x = 20, y = 80 )
        
        #Para que seleccione sus cuentas
        var = 0
        self.selected_account = tkinter.IntVar()
        for account in self.accounts:
            #Tipo de cuenta
            tempLabel = tkinter.Label(
                self.panel_usuario, 
                text = "{}".format(account[2])
            )
            tempLabel.place( x = 10, y = 130 + var*30 )
            
            #Boton de selección
            tempButton = tkinter.Radiobutton(
                self.panel_usuario,
                value = var,
                variable = self.selected_account
            )
            tempButton.place( x = 120, y = 125 + var*30 )
            
            var += 1
            
        #Seleccionar cuenta elegida
        btn01 = tkinter.Button(self.panel_usuario, text = "Seleccionar", 
                                    command = self.showAccount)
        btn01.place( x = 50, y = 135 + var*30 )
        
        #Cerrar sesion
        btn02 = tkinter.Button(self.panel_usuario, text = "Cerrar sesion", 
                                    command = self.logOut)
        btn02.place( x = 200, y = 200 + var*30 )
        
        self.panel_usuario.mainloop()
        return
            
    #Ventana del tecnico
    def repairmanPanel(self):
        self.createdRepairman = True
        result = self.getATMS()
        
        self.repairman_panel = tkinter.Tk()
        self.repairman_panel.title("Técnico")
        self.repairman_panel.geometry("300x250+100+150")
        
        welcome = tkinter.Label( 
            self.repairman_panel, 
            text="Bienvenido {}".format(self.user_name) )
        welcome.place( x = 100, y = 30 )
        
        if result[0][2] != 'OK' :
            message1 = tkinter.Label(
                self.repairman_panel, 
                text="Tienes que reparar el cajero \'{}\'".format( result[0][0] ))
            message1.place( x = 20, y = 90)
            message2 = tkinter.Label(
                self.repairman_panel, 
                text="Esta ubicado en {}".format( result[0][1] ))
            message2.place( x = 20, y = 110)
            message3 = tkinter.Label(
                self.repairman_panel, 
                text="Muestra el estatus de: \'{}\'".format( result[0][2] ))
            message3.place( x = 20, y = 130)
            
            repair = tkinter.Button( self.repairman_panel, text="ATM reparado",
                                   command = self.repairedATM)
            repair.place( x = 100, y = 200 )
            
        else:
            message1 = tkinter.Label(
                self.repairman_panel, 
                text="El banco te asignara tu siguiente cajero a reparar")
            message1.place( x = 20, y = 90)
            
        
        logOut = tkinter.Button( self.repairman_panel, text="Cerrar sesión",
                               command = self.logOut)
        logOut.place( x = 200, y = 200 )
        
        self.repairman_panel.mainloop()
        return
    
    #Mostrar informacion de las cuentas
    def showAccount(self):
        
        if (not self.destroyedWindow): 
            self.panel_usuario.destroy()
            self.destroyedWindow = True
            
        self.select = self.selected_account.get()
        
        self.getAccountInfo(self.select)
        
        self.account_window = tkinter.Tk()
        self.account_window.title('Cuenta {}'.format( self.select + 1 ))
        self.account_window.geometry("350x300+500+200")
        
        #Motrar el tipo de cuenta seleccionada
        account_type = tkinter.Label(
            self.account_window,
            text="Cuenta seleccionada: {}".format( self.result[0][2] ))
        account_type.place( x = 50, y = 20)
        
        #Mostrar numero de cuenta
        number = tkinter.Label(
            self.account_window, 
            text = "Numero de cuenta: {}".format( self.result[0][0] ))
        number.place( x = 10, y = 80 )
        
        #Mostrar dinero en la cuenta seleccionada
        balance = tkinter.Label(
            self.account_window, 
            text = "Saldo: ${}".format( self.result[0][3] ))
        balance.place( x = 10, y = 100 )
        
        #Realizar retiros
        retiros = tkinter.Button(
            self.account_window,
            text="Retirar efectivo", command=self.withdrawWindow)
        retiros.place( x = 30, y = 150 )
        
        #Realizar deposito 
        depositos = tkinter.Button(
            self.account_window,
            text="Depositar dinero", command=self.depositWindow)
        depositos.place( x = 180, y = 150 )
        
        #Realizar transferencias
        transferencias = tkinter.Button(
            self.account_window,
            text="Tranferir a otra cuenta", command=self.transferenceWindow)
        transferencias.place( x = 30, y = 190 )
        
        #Revisar estado de cuenta
        estado = tkinter.Button(
            self.account_window,
            text="Mostrar estado de cuenta", command=self.stateWindow)
        estado.place( x = 180, y = 190 )
        
        #Regresar al menu del usuario
        retorno = tkinter.Button(
            self.account_window,
            text="Regresar al menu principal", command=self.regresarMenuUsuario)
        retorno.place( x = 105, y = 260 )
        
        self.account_window.mainloop()
        return
    
    #Retirar dinero
    def withdrawWindow(self):
        self.account_window.destroy()
        self.createdWithdraw = True
        self.transType = 'withdraw'
        
        self.getAccountInfo(self.select)
        
        self.withdraw_panel = tkinter.Tk()
        self.withdraw_panel.title("Retiros")
        self.withdraw_panel.geometry("300x170+100+200")
        
        balance = tkinter.Label(
            self.withdraw_panel, 
            text="Saldo disponible: ${}".format( self.result[0][3] ))
        balance.place( x = 80, y = 10)
        
        pregunta = tkinter.Label(self.withdraw_panel,
                                 text="¿Cuanto quiere retirar?")
        pregunta.place( x = 10, y = 70 )
        
        self.money = tkinter.Entry(self.withdraw_panel, bg = "lightgray", 
                                   width = 20)
        self.money.place( x = 150, y = 70 )
        
        boton = tkinter.Button(self.withdraw_panel, text="Retirar",
                               command=self.authorizeWithdraw)
        boton.place( x = 50, y = 120 )
        
        salir = tkinter.Button(self.withdraw_panel, text="Regresar",
                               command=self.returnAccountMenu)
        salir.place( x = 220, y = 120 )
        
        self.withdraw_panel.mainloop()
        return
    
    #Si las entradas no son válidas
    def notValidInput(self):
        
        tkinter.messagebox.showwarning(title = "Error de lectura",
                                       message = "Introduzca un valor válido")
        
        return
    
    #Ventana de depositos
    def depositWindow(self):
        self.account_window.destroy()
        self.createdDeposit = True
        self.transType = 'deposit'
        
        self.deposit_window = tkinter.Tk()
        self.deposit_window.title("Depositos")
        self.deposit_window.geometry("305x170+100+200")
        
        pregunta = tkinter.Label(self.deposit_window,
                                 text="¿Cuanto quiere depositar?")
        pregunta.place( x = 10, y = 70 )
        
        self.money = tkinter.Entry(self.deposit_window, bg = "lightgray", 
                                   width = 20)
        self.money.place( x = 165, y = 70 )
        
        boton = tkinter.Button(self.deposit_window, text="Depositar",
                               command=self.authorizeDeposit)
        boton.place( x = 50, y = 120 )
        
        salir = tkinter.Button(self.deposit_window, text="Regresar",
                               command=self.returnAccountMenu)
        salir.place( x = 220, y = 120 )
        
        self.deposit_window.mainloop()
        
        return
    
    #Ventana de transferencias
    def transferenceWindow(self):
        self.account_window.destroy()
        self.createdTransfer = True
        self.transType = 'transference'
        
        self.transfer_window = tkinter.Tk()
        self.transfer_window.title("Transferencias")
        self.transfer_window.geometry("350x250+100+200")
        
        balance = tkinter.Label(
            self.transfer_window, 
            text="Saldo disponible: ${}".format( self.result[0][3] ))
        balance.place( x = 80, y = 10)
        
        pregunta = tkinter.Label(self.transfer_window,
                                 text="Dinero a transferir: ")
        pregunta.place( x = 61, y = 70 )
        
        self.money = tkinter.Entry(self.transfer_window, bg = "lightgray", 
                                   width = 20)
        self.money.place( x = 170, y = 70 )
        
        pregunta2 = tkinter.Label(self.transfer_window,
                                 text="Numero de cuenta destino: ")
        pregunta2.place( x = 10, y = 110 )
        
        self.second_account = tkinter.Entry(self.transfer_window, bg = "lightgray", 
                                   width = 20)
        self.second_account.place( x = 170, y = 110 )
        
        boton = tkinter.Button(self.transfer_window, text="Transferir",
                               command=self.authorizeTransfer)
        boton.place( x = 50, y = 200 )
        
        salir = tkinter.Button(self.transfer_window, text="Regresar",
                               command=self.returnAccountMenu)
        salir.place( x = 220, y = 200 )
        
        self.transfer_window.mainloop()
        
        return
    
    #Mostrar estado de cuenta
    def stateWindow(self):
        self.account_window.destroy()
        self.createdState = True
        
        transactions = self.getTransactions()
        lim = len(transactions)
        place = lim if lim <= 10 else 10
        
        self.state_window = tkinter.Tk()
        self.state_window.title("Estado de cuenta")
        
        size = lim if lim<11 else 10
        self.state_window.geometry("600x{}+100+200".format(200 + size*20))
        
        if lim == 0:
            estados = tkinter.Label( 
                self.state_window, 
                text = "No ha realizado transacciones con esta cuenta" )
            estados.place( x = 50, y = 75 )
            
        else:
            
            estados = tkinter.Label( self.state_window, 
                                    text = "Últimas 10 transacciones: " )
            estados.place( x = 20, y = 20 )    
            
            cuadricula = tkinter.Label(
                self.state_window, 
                text="Tipo \t           ID \t        Cuenta destino \t Fecha \t\tMonto \t           Lugar")
            cuadricula.place( x = 50, y = 70  ) 
             
            if lim > 10:  
                 
                start = lim
                for trans in range(10):
                    
                    query = "select atm_location from atm where ID={}".format(
                        transactions[start + trans][4])
                    cursor = self.client.cursor()
                    cursor.execute(query)
                    result_set = cursor.fetchall()
                    
                    space1 = '\t' if transactions[start+trans][3]=='deposit' else ''
                    space2 = '\t' if len(str(transactions[start+trans][5]))<5 else ''
                     
                    prueba = tkinter.Label(
                        self.state_window, 
                        text = "{0}\t{1}{2}\t     {3}\t\t    {4}\t       {5}\t{6}{7}".format(
                            transactions[start+trans][3], space1,
                            transactions[start+trans][0], transactions[start+trans][2], 
                            transactions[start+trans][6], transactions[start+trans][5], 
                            space2 ,result_set[0][0]))
                    prueba.place( x = 30, y = 100 + 20*trans)
         
            else:
                
                for trans in range(lim):
                    
                    query = "select atm_location from atm where ID={}".format(
                        transactions[trans][4])
                    cursor = self.client.cursor()
                    cursor.execute(query)
                    result_set = cursor.fetchall()
                    
                    space1 = '\t' if transactions[trans][3]=='deposit' else ''
                    space2 = '\t' if len(str(transactions[trans][5]))<5 else ''
                     
                    prueba = tkinter.Label(
                        self.state_window, 
                        text = "{0}\t{1}{2}\t     {3}\t\t    {4}\t        {5}\t{6}{7}".format(
                            transactions[trans][3], space1,
                            transactions[trans][0], transactions[trans][2], 
                            transactions[trans][6], transactions[trans][5], 
                            space2, result_set[0][0]))
                    prueba.place( x = 30, y = 100 + 20*trans)
        
        
        salir = tkinter.Button(self.state_window, text="Regresar",
                               command=self.returnAccountMenu)
        salir.place( x = 500, y = 150 + 20*place )
        
        self.state_window.mainloop()
        
        return
    
    #--------------------------------------------------------------------------
     
#Funciones internas:

    #Verificar usuario 
    def verification(self):
        
        #Conseguir usuario y contraseña
        self.user = self.writeUser.get()
        password = self.writePassword.get()
        
        #Si no tiene usuario o contraseña
        if (self.user == '' or password == ''):
            
            missingData = "usuario" if self.user=='' else "contraseña"
            
            tkinter.messagebox.showwarning(
                title="Error", 
                message="Por favor ingrese su {}".format(missingData)
            )
            return
        
        query = "select * from clients where ID=\'{}\'".format(self.user)
        
        cursor = self.client.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        
        if( len(result_set) == 0 ):
            
            #Buscar si es tecnico
            query = "select * from repairman where ID=\'{}\'".format(self.user)
            
            cursor = self.client.cursor()
            cursor.execute(query)
            result_set = cursor.fetchall()
            
            #Si no existe el cliente
            if( len(result_set) == 0 ):
                
                tkinter.messagebox.showerror(
                    title = "No encontrado", 
                    message="El usuario \"{}\" no existe".format(self.user)
                )
                return
                
            else:
                if(result_set[0][1] == password):
                    self.user_name = result_set[0][2]
                    self.assigned_atm = result_set[0][3]
                    self.principal.destroy()
                    self.repairmanPanel()
                else:
                    self.wrongPassword()
                    return
            
        else:
            
            if(result_set[0][1] == password):
                self.user_name = result_set[0][2]
                self.principal.destroy()
                self.accounts = self.getAccounts()
                self.userPanel()
            else:
                self.wrongPassword()
                return

    #Obtener cuentas       
    def getAccounts(self):
        
        query = "select * from accounts where user_ID=\'{}\'".format(self.user)
        
        cursor = self.client.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    #Sacar dinero
    def getAccountInfo(self, select):
        query = "select * from accounts where account_number=\'{}\'".format(
            self.accounts[select][0])
        
        cursor = self.client.cursor()
        cursor.execute(query)
        self.result = cursor.fetchall()
        return
    
    #Retiros de efectivo
    def authorizeWithdraw(self):
        
        self.desired_withdraw = self.validateInput()
        
        if self.desired_withdraw == False:
            return

        balance = float( self.result[0][3] )

        self.new_balance = balance - self.desired_withdraw
        
        if ( self.new_balance < 0 ):
            
            tkinter.messagebox.showerror(title = "Error", 
                                         message="Saldo insuficiente")
            
        else:
            
            tkinter.messagebox.showinfo(title="Retiro exitoso", 
                                        message="El retiro fue realizado con exito")
            
            #actualizar valor del saldo
            self.destiny_account = 'null'
            self.update_balance()
            self.recordTransaction()
            
            self.withdraw_panel.destroy()
            self.createdWithdraw = False
            self.destroyedWindow = True
            self.showAccount()
        
        return
    
    #Depositar dinero
    def authorizeDeposit(self):
        
        self.desired_withdraw = self.validateInput()
        
        if self.desired_withdraw == False:
            return

        balance = float( self.result[0][3] )
        self.new_balance = balance + self.desired_withdraw
        
        tkinter.messagebox.showinfo(title="Deposito exitoso", 
                                    message="El deposito fue realizado con exito")
        
        self.destiny_account = 'null'
        
        self.update_balance()
        self.recordTransaction()
        
        self.deposit_window.destroy()
        self.createdDeposit = False
        self.destroyedWindow = True
        self.showAccount()
        
        return
    
    #Transferir dinero
    def authorizeTransfer(self):
        
        self.desired_withdraw = self.validateInput()
        if self.desired_withdraw == False:
            return
        
        if self.validateAccount() == False:
            return
        
        
        if self.result[0][0] == self.destiny_account:
            tkinter.messagebox.showerror(
                title = "Error", 
                message="No se puede depositar a la misma cuenta")
            return
        

        balance = float( self.result[0][3] )
        self.new_balance = balance - self.desired_withdraw
        
        if ( self.new_balance < 0 ):
            
            tkinter.messagebox.showerror(title = "Error", 
                                         message="Saldo insuficiente")
            
        else:
            
            tkinter.messagebox.showinfo(title="Retiro exitoso", 
                                        message="La transferencia se realizo con exito")
            
            #actualizar valor del saldo
            self.recordTransaction()
            
            #Actualizar el valor de la cuenta 1
            self.update_balance()
            
            #acutalizar saldo de la cuenta 2
            account_1 = self.result[0][0]
            
            self.result[0] = list(self.result[0])
            self.result[0][0] = self.destiny_account
            self.result[0] = tuple(self.result[0])
            
            query = "select balance from accounts where account_number=\'{}\'".format(
                self.destiny_account)
            cursor = self.client.cursor()
            cursor.execute(query)
            balance = cursor.fetchall()[0][0]
            print(balance)
            
            self.new_balance = balance + self.desired_withdraw
            
            self.update_balance()
            
            self.result[0] = list( self.result[0] )
            self.result[0][0] = account_1
            self.result[0] = tuple( self.result[0] )
            
            self.transfer_window.destroy()
            self.createdTransfer = False
            self.destroyedWindow = True
            self.showAccount()
        
        return
    
    #Regresar al menu del usuario
    def regresarMenuUsuario(self):
        self.account_window.destroy()
        self.userPanel()
        return
    
    #Cerrar sesión
    def logOut(self):
        
        if self.createdUser:        self.panel_usuario.destroy()
        if self.createdRepairman:  self.repairman_panel.destroy()
        
        self.createdUser = False
        self.createdRepairman = False
        
        self.logIn()
        return
    
    #Actualizar el balance de la cuenta
    def update_balance(self):
        
        query = "update accounts set balance={0} where account_number=\'{1}\'".format(
            self.new_balance, self.result[0][0]);
    
        cursor = self.client.cursor()
        cursor.execute(query)
        self.client.commit()
        
        return

    #Regresar al menu de la cuenta
    def returnAccountMenu(self):
        
        if (self.createdWithdraw): self.withdraw_panel.destroy()
        if (self.createdDeposit): self.deposit_window.destroy()
        if (self.createdTransfer): self.transfer_window.destroy()
        if (self.createdState): self.state_window.destroy()
        
        self.createdWithdraw = False
        self.createdDeposit = False
        self.createdTransfer = False
        self.createdState = False
        
        self.showAccount()
        
        return
    
    #Actualizar las transacciones de la cuenta
    def recordTransaction(self):
        
        query = " select trans_ID from transactions"
        cursor = self.client.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        
        columna = [fila[0] for fila in result_set]
        
        flag = False
        while not flag: 
            trans_id = str (round( random.random() * 500 ) )
            
            if trans_id not in columna:
                flag = True
        
        query = """
            insert into transactions values(\'{0}\', \'{1}\', 
                            {2}, \'{3}\', \'{4}\', {5}, \'{6}\',\'{7}\');
        """.format(trans_id, self.result[0][0], self.destiny_account, 
        self.transType, self.atms[random.randint(0, self.atm_num - 1)][0],
        self.desired_withdraw, date.today(), 
        datetime.now().strftime("%H:%M:%S"))
            
        cursor = self.client.cursor()
        cursor.execute(query)
        
        self.client.commit()
        return
    
    #Checar que las entradas sean numericas
    def validateInput(self):
        if self.money.get() == '':
            tkinter.messagebox.showwarning(title='Error de entrada',
                                           message="Introduce un valor")
            return False
        
        cadena = self.money.get().split( sep = '.')
        
        if len(cadena) > 2:
            tkinter.messagebox.showwarning(title="Error de escritura",
                                           message="No uses tantos puntos")
            return False
        
        if len(cadena) == 1:
            
            if cadena[0].isdigit(): 
                cadena = cadena[0]
            else:
                self.notValidInput()
                return False
            
        else:
            if cadena[0].isdigit() and cadena[1].isdigit(): 
                cadena = cadena[0] + '.' + cadena[1]
            else:
                self.notValidInput()
                return False
        
        cadena= round( float( cadena ), 2)
        
        return cadena
    
    #Checar que la cuenta exista
    def validateAccount(self): 
        destiny_account = self.second_account.get()
        
        query = "select * from accounts where account_number=\'{}\'".format(
            destiny_account)
        
        cursor = self.client.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        
        if len(result_set) == 0:
            
            tkinter.messagebox.showerror(
                title = "No encontrado", 
                message="La cuenta \"{}\" no existe".format(destiny_account)
            )
            return False
        
        self.destiny_account = destiny_account
        return True
    
    #Obtener todas las transacciones de una cuenta
    def getTransactions(self):
        
        query = """select * from transactions where account1=\'{0}\' 
            or account2=\'{1}\' order by trans_date, trans_time""".format(self.result[0][0],
            self.result[0][0])
        
        cursor = self.client.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        
        return result_set
    
    #Obtener info del ATM a reparar:
    def getATMS(self):
        
        query = "select * from atm where ID=\'{}\'".format(self.assigned_atm);
    
        cursor = self.client.cursor()
        cursor.execute(query)
        result_set = cursor.fetchall()
        
        return result_set

    #Funcion auxiliar para 
    def repairedATM(self):

        self.repairman_panel.destroy()
        self.setStatusOK()
        self.repairmanPanel()
        
        return
    
    #Poner OK en el status de la BD
    def setStatusOK(self):
        
        query = "update atm set atm_status=\'OK\' where ID=\'{}\'".format(
            self.assigned_atm)
    
        cursor = self.client.cursor()
        cursor.execute(query)
        self.client.commit()
        
        return

    
#------------------------------------------------------------------------------    
    
#Iniciar app
if __name__ == '__main__':
    app = AppBanco()    