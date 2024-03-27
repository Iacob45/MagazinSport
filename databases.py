import sqlite3
import customtkinter
from PIL import Image, ImageTk

class Aplicatie:

    def __init__(self,id_cont="",parola="",admin=False):
        self.id_cont=id_cont
        self.parola=parola
        self.admin=admin
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()


    def login(self, frame, root, entry1, entry2):
        self.id_cont = entry1.get()
        self.parola = entry2.get()
        self.cursor.execute("""
        SELECT COUNT(id_cont) FROM conturi
        WHERE id_cont = '{}'
        """.format(self.id_cont))

        if(self.cursor.fetchall()[0][0] != 0):
            self.cursor.execute("""
            SELECT * FROM conturi
            WHERE id_cont = '{}'
            """.format(self.id_cont))
            results = self.cursor.fetchone()
            if(results[1] != '' and results[2] != ''):
                if(results[1] == self.parola and results[2] == False):
                    user = Aplicatie_User(self)
                    user.start2(root, frame)
                elif(results[1] == self.parola and results[2] == True):
                    print("Admin")
                else:
                    eroare = customtkinter.CTkLabel(master=frame, width=400, height=80, text="Date incorecte", text_color=("Red"),font=("Roboto", 14))
                    eroare.pack(pady=12, padx=10)
                    eroare.place(relx=0.5, rely=0.6, anchor='center')
            else:
                eroare = customtkinter.CTkLabel(master=frame, width=400, height=80, text="Date incorecte", text_color=("Red"),font=("Roboto", 14))
                eroare.pack(pady=12, padx=10)
                eroare.place(relx=0.5, rely=0.6, anchor='center')
        else:
            eroare = customtkinter.CTkLabel(master=frame, width=400, height=80, text="Date incorecte", text_color=("Red"),font=("Roboto", 14))
            eroare.pack(pady=12, padx=10)
            eroare.place(relx=0.5, rely=0.6, anchor='center')


    def register_user(self, frame, root, nume, parola):

        if(nume == '' or parola == ''):
            lipsa_date = customtkinter.CTkLabel(master=frame, width=400, height=80, text="Scrieti datele pentru inregistrare", text_color=("#FA86C4"),font=("Roboto", 12))
            lipsa_date.pack(pady=12, padx=10)
            lipsa_date.place(relx=0.5, rely=0.6, anchor='center')
        else:

            self.cursor.execute("""
            SELECT COUNT(id_cont) FROM conturi
            WHERE id_cont = '{}'
            """.format(nume))
            if(self.cursor.fetchall()[0][0] != 0):
                date_existente = customtkinter.CTkLabel(master=frame, width=400, height=80, text="Cont deja existent, apasati pe autentificare", text_color=("Green"), font=("Roboto", 12))
                date_existente.pack(pady=12, padx=10)
                date_existente.place(relx=0.5, rely=0.6, anchor='center')
            else:
                self.id_cont = nume
                self.parola = parola
                self.credit = 100

                self.cursor.execute("""
                INSERT INTO conturi VALUES
                ('{}','{}',False)
                """.format(self.id_cont, self.parola))
                self.connection.commit()

                self.cursor.execute("""
                INSERT INTO conturi_user VALUES
                ('{}', {})
                """.format(self.id_cont, self.credit))
                self.connection.commit()

                user = Aplicatie_User(self)
                user.start2(root, frame)



    def start(self, root=None, frame=None):
        if(frame != None):
            frame.destroy()
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")


        if(root == None):
            root = customtkinter.CTk()
            root.geometry("1000x600")

        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Autentificare", font=("Roboto", 24))
        label.pack(pady=32, padx=10)

        entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="ID utilizator")
        entry1.pack(pady=12, padx=10)
        entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Parola", show="*")
        entry2.pack(pady=12, padx=10)

        button_login = customtkinter.CTkButton(master=frame, text="Autentificare", command= lambda: self.login(frame,root,entry1,entry2))
        button_login.pack(pady=12, padx=10)

        button_register = customtkinter.CTkButton(master=frame, text="Inregistrare", command=lambda: self.register_user(frame, root,entry1.get(),entry2.get()))
        button_register.pack(pady=12, padx=10)

        root.mainloop()



class Aplicatie_User(Aplicatie):

    def __init__(self, cont):
        super(Aplicatie_User, self).__init__(cont.id_cont,cont.parola,cont.admin)
        self.cursor.execute("""
        SELECT credit FROM conturi_user
        WHERE id_cont = '{}'
        """.format(self.id_cont))


        self.credit = self.cursor.fetchone()[0]
        self.cos = CosCumparaturi()


    def start2(self, root, frame):
        frame.destroy()
        self.cursor.execute("""
        SELECT id_produs FROM produse
        """)
        results = [row[0] for row in self.cursor.fetchall()]
        produse = []
        categorii = []

        for x in results:
            p = Produs()
            p.load_produs(x)
            produse.append(p)

        for a in produse:
            k = 0
            for b in categorii:
                if a.categorie_produs == b:
                    k = 1
            if k == 0:
                categorii.append(a.categorie_produs)

        customtkinter.set_default_color_theme("green")
        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Shoppero", font=("Roboto", 24))
        label.pack(pady=32, padx=10)

        for a in categorii:
            button_categorie = customtkinter.CTkButton(master=frame, text="{}".format(a),command=lambda z = a: self.afisare_produse(frame, root, z, produse))
            button_categorie.pack(pady=12, padx=10)

        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        image_button = customtkinter.CTkButton(master=frame, fg_color='#9400D3', hover_color='#330066', width=66,height=26, text="", image=back_img,command=lambda: self.start(root, frame))
        image_button.pack()
        image_button.place(relx=0.07, rely=0.08, anchor='w')


    def afisare_produse(self, frame, root, a, produse):
        frame.destroy()
        customtkinter.set_default_color_theme("blue")
        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        label = customtkinter.CTkLabel(master=frame, text="Shoppero", font=("Roboto", 24))
        label.pack(pady=32, padx=10)
        for x in produse:
            if x.categorie_produs == a:
                button_produs = customtkinter.CTkButton(master=frame, text="{}\n{}".format(x.firma,x.descriere), command=lambda y = x: self.vizualizare_produs(frame, produse, root, y))
                button_produs.pack(pady=12, padx=10)
        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        image_button = customtkinter.CTkButton(master=frame, fg_color = '#BF0A30', hover_color = '#8B0000', width=66, height=26, text="", image=back_img,command=lambda: self.start2(root, frame))
        image_button.pack()
        image_button.place(relx=0.07, rely=0.08, anchor='w')

    def vizualizare_produs(self, frame, produse, root, x):

        frame.destroy()
        customtkinter.set_default_color_theme("dark-blue")
        frame = customtkinter.CTkFrame(master=root, fg_color="white")
        frame.pack(pady=20, padx=60, fill="both", expand=True)

        produs_img = customtkinter.CTkImage(Image.open("{}".format(x.link_img)), size=(500, 500))

        label7 = customtkinter.CTkLabel(master=frame ,image=produs_img, text="")
        label7.pack(pady=12, padx=10)
        label7.place(relx=0.9, rely=0.5, anchor='e')
        label1 = customtkinter.CTkLabel(master=frame, text="Shoppero", font=("Roboto", 24))
        label1.pack(pady=32, padx=10)
        label1.place(relx=0.8, rely=0.1, anchor='w')
        label2 = customtkinter.CTkLabel(master=frame, text="{}".format(x.firma), font=("Roboto", 35))
        label2.pack(pady=12, padx=10)
        label2.place(relx=0.1,rely=0.3,anchor='w')
        label3 = customtkinter.CTkLabel(master=frame, justify="left", wraplength=250, text="{}".format(x.descriere), font=("Roboto", 20))
        label3.pack(pady=12, padx=10)
        label3.place(relx=0.1, rely=0.45, anchor='w')
        label4 = customtkinter.CTkLabel(master=frame, text="stock {}".format(x.tip_stock), font=("Roboto", 16))
        label4.pack(pady=12, padx=10)
        label4.place(relx=0.8, rely=0.85, anchor='w')
        label5 = customtkinter.CTkLabel(master=frame, text="Produse in stock: {}".format(x.stock), font=("Roboto", 16))
        label5.pack(pady=12, padx=10)
        label5.place(relx=0.1, rely=0.85, anchor='w')
        label6 = customtkinter.CTkLabel(master=frame, text="{} lei".format(x.pret), font=("Roboto", 40))
        label6.pack(pady=12, padx=10)
        label6.place(relx=0.1, rely=0.6, anchor='w')

        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        back_button = customtkinter.CTkButton(master=frame, width=66, height=26, text="", image=back_img, command=lambda: self.afisare_produse(frame, root, x.categorie_produs, produse))
        back_button.pack()
        back_button.place(relx=0.07, rely=0.08, anchor='w')
        buy_entry = customtkinter.CTkEntry(master=frame, justify="center", width=40, height=46)
        buy_entry.insert(0,"1")
        buy_entry.pack()
        buy_entry.place(relx=0.1, rely=0.73, anchor='w')
        buy_button = customtkinter.CTkButton(master=frame, width=156, height=46, font=("Roboto", 26), text_color="white", fg_color="#AEF359", hover_color="#3A5311", text="Adauga in cos",command=lambda: self.cos.adauga(x,int(buy_entry.get())))
        buy_button.pack()
        buy_button.place(relx=0.15, rely=0.73, anchor='w')
        cos_img = customtkinter.CTkImage(Image.open("assets/coscumparaturi.png"), size=(30, 30))
        cos_button = customtkinter.CTkButton(master=frame, width=66, height=26, font=("Roboto", 16), text="{}".format(self.cos.produse), image=cos_img,command=lambda: self.cos_cumparaturi(root, frame, produse, x))
        cos_button.pack()
        cos_button.place(relx=0.17, rely=0.08, anchor='w')



    def cos_cumparaturi(self, root, frame, produse, x):

        frame.destroy()
        frame = customtkinter.CTkFrame(master=root)
        frame.pack(pady=20, padx=60, fill="both", expand=True)
        i = 0
        titlu = customtkinter.CTkLabel(master=frame, corner_radius=5, width=350, height=60, justify="left",text="Cos de cumparaturi", text_color="white", fg_color="#FEDC56", font=("Roboto", 36))
        titlu.pack(pady=12, padx=10)
        titlu.place(relx=0.1, rely=0.07, anchor='w')

        for a in self.cos.lista:
            label = customtkinter.CTkLabel(master=frame, corner_radius=10, justify="left", text_color="white", fg_color="#999999", text="{}.{}\n{}\nCantitate: {}".format(i+1,a[0].firma,a[0].descriere,a[1]), font=("Roboto", 16))
            label.pack(pady=12, padx=10)
            label.place(relx=0.1, rely=0.22 + 0.13*i, anchor='w')
            i = i + 1

        suma = customtkinter.CTkLabel(master=frame, corner_radius=5, width=250, height=40, justify="left",text="Total: {} Lei".format(self.cos.suma), text_color="white", fg_color="#F4C430",font=("Roboto", 26))
        suma.pack(pady=12, padx=10)
        suma.place(relx=0.1, rely=0.77, anchor='w')

        back_img = customtkinter.CTkImage(Image.open("assets/backarrow.png"), size=(30, 30))
        back_button = customtkinter.CTkButton(master=frame, width=66, height=26, text="", image=back_img, fg_color="#FFF700", hover_color="#FFA500", command=lambda: self.vizualizare_produs(frame, produse, root,x))
        back_button.pack()
        back_button.place(relx=0.07, rely=0.88, anchor='w')

        delete_img = customtkinter.CTkImage(Image.open("assets/delete.png"), size=(30, 30))
        delete_button = customtkinter.CTkButton(master=frame, width=66, height=46, text="", image=delete_img,fg_color="#FF0800", hover_color="#800000",command=self.sterge_cos)
        delete_button.pack()
        delete_button.place(relx=0.9, rely=0.074, anchor='w')

        purchase_button = customtkinter.CTkButton(master=frame, text_color="white", fg_color="#FFBF00", hover_color="#FFBF00", corner_radius=30, width=100, height=50, text="Cumpara", font=("Roboto", 46), command=lambda: self.cumpara_cos(root, frame))
        purchase_button.pack()
        purchase_button.place(relx=0.7, rely=0.8, anchor='w')
        credit_label = customtkinter.CTkLabel(master=frame, corner_radius=5, width=70, height=30, justify="center",text="(Credit: {})".format(self.credit), text_color="white", fg_color="#FFBF00",font=("Roboto", 16))
        credit_label.pack(pady=0, padx=0)
        credit_label.place(relx=0.782, rely=0.9, anchor='w')


    def sterge_cos(self):
        self.cos.lista = []
        self.cos.produse = 0
        self.cos.suma = 0


    def cumpara_cos(self, root, frame):
        if(self.credit >= self.cos.suma):
            self.credit = self.credit - self.cos.suma
            self.cursor.execute("UPDATE conturi_user SET credit = {} WHERE id_cont = '{}'".format(self.credit,self.id_cont))
            self.connection.commit()
            self.connection.close()
            self.update_produse()
            self.sterge_cos()

            self.connection = sqlite3.connect('mydata.db')
            self.cursor = self.connection.cursor()

            label = customtkinter.CTkLabel(master=frame, corner_radius=20, width=600, height=300, justify="center", text_color="#006400",fg_color="#98FB98",text="Produse achizitionate cu succes" , font=("Roboto", 46))
            label.pack(pady=12, padx=10)
            label.place(relx=0.5, rely=0.5, anchor='center')
            label.after(3000, lambda: self.start2(root,frame))

        else:
            label = customtkinter.CTkLabel(master=frame, corner_radius=20, width=650, height=300, justify="center", text_color="#8B0000",fg_color="#FF7F7F", text="Credit insuficient",font=("Roboto", 46))
            label.pack(pady=12, padx=10)
            label.place(relx=0.5, rely=0.5, anchor='center')
            label.after(2000,lambda: label.destroy())

    def update_produse(self):
        for a in self.cos.lista:
            a[0].update_stock(-a[1])



class CosCumparaturi:

    def __init__(self):
        self.lista = []
        self.produse = 0
        self.suma = 0


    def adauga(self,produs,cantitate):
        if(produs.stock < cantitate):
            cantitate = produs.stock
        k = 0
        self.produse = self.produse + cantitate
        self.suma = self.suma + produs.pret*cantitate
        for i in range(len(self.lista)):
            if(self.lista[i][0] == produs):
                self.lista[i][1] = self.lista[i][1] + cantitate
                k = 1
                break
        if(k == 0):
            self.lista.append([produs, cantitate])



class Produs:

    def __init__(self, id_produs=0, firma="", categorie_produs="", descriere="",tip_stock="", stock=0, pret=0, link_img=""):
        self.id_produs = id_produs
        self.firma = firma
        self.categorie_produs = categorie_produs
        self.descriere = descriere
        self.tip_stock = tip_stock
        self.stock = stock
        self.pret = pret
        self.link_img = link_img



    def load_produs(self, id_produs):
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        SELECT * FROM produse
        WHERE id_produs = {}
        """.format(id_produs))

        results = self.cursor.fetchone()

        self.id_produs = id_produs
        self.firma = results[1]
        self.categorie_produs = results[2]
        self.descriere = results[3]
        self.tip_stock = results[4]
        self.stock = results[5]
        self.pret = results[6]
        self.link_img = results[7]

        self.connection.close()

    def insert_produs(self):
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        INSERT INTO produse VALUES
        ({},'{}','{}','{}','{}',{},{},'{}')
        """.format(self.id_produs, self.firma, self.categorie_produs,self.descriere,self.tip_stock,self.stock,self.pret,self.link_img))

        self.connection.commit()
        self.connection.close()

    def update_stock(self,number):
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        UPDATE produse SET stock = (stock+{}) WHERE id_produs = {}
        """.format(number,self.id_produs))

        self.connection.commit()
        self.connection.close()

class Produs_Furnizor(Produs):

    def __init__(self,id_produs=0, firma="", categorie_produs="", descriere="",tip_stock="", stock=0, pret=0, link_img="",furnizor="", t_extra_livrare=0):
        super(Produs_Furnizor, self).__init__(id_produs, firma, categorie_produs, descriere,tip_stock, stock, pret, link_img)
        self.furnizor = furnizor
        self.t_extra_livrare = t_extra_livrare

    def load_produs(self, id_produs):
        super(Produs_Furnizor, self).load_produs(id_produs)
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        SELECT * FROM produse_furnizori
        WHERE id_produs = {}
        """.format(id_produs))

        results2 = self.cursor.fetchone()

        self.furnizor = results2[1]
        self.t_extra_livrare = results2[2]

        self.connection.close()

    def insert_produs(self):
        super(Produs_Furnizor, self).insert_produs()
        self.connection = sqlite3.connect('mydata.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
        INSERT INTO produse_furnizori VALUES
        ({},'{}',{})
        """.format(self.id_produs,self.furnizor,self.t_extra_livrare))

        self.connection.commit()
        self.connection.close()



connection = sqlite3.connect('mydata.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produse (
    id_produs INTEGER PRIMARY KEY,
    firma TEXT,
    categorie_produs TEXT,
    descriere TEXT,
    tip_stock TEXT,
    stock INTEGER,
    pret FLOAT,
    link_img TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produse_furnizori (
    id_produs INTEGER PRIMARY KEY,
    furnizor TEXT,
    t_extra_livrare INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS conturi (
    id_cont TEXT PRIMARY KEY,
    parola TEXT,
    admin BOOLEAN
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS conturi_user (
    id_cont TEXT PRIMARY KEY,
    credit FLOAT
)
""")


#p1 = Produs(13,"Adidas","Pantofi","Adidasi Campus Collegiate Green","propriu",4,150,"adidas-campus-00s-collegiate-green-id2048-64f9706f73bfa.jpg")
#p1 = Produs_Furnizor(2,"Nike","Tricou","Tricou verde cu uscare rapida","furnizor",10,60,"SC_Sportiv",3)
#p1.insert_produs()
#p1.load_produs(4)
#p1.update_stock(-1)
#cursor.execute("drop table produse")
#cursor.execute("UPDATE produse SET link_img = 'assets/adidas-campus-00s-collegiate-green-id2048-64f9706f73bfa.jpg' WHERE id_produs = 13")
#connection.commit()

connection.close()

MAIN = Aplicatie()
MAIN.start()

#connection1 = sqlite3.connect('mydata.db')
#cursor1 = connection1.cursor()

#cursor1.execute("SELECT * FROM produse")
#results = cursor1.fetchall()
#print(results)

#connection1.close()
