import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
print("Matplotlib importé avec succès")

import numpy as np
import uuid
import hashlib
import re

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion Financière")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        self.current_user = None
        self.current_user_id = None
        self.current_role = None
        
        # Connexion à la base de données
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Remplacez par votre utilisateur
                password="root",  # Remplacez par votre mot de passe
                database="gestion_financiere1"
            )
            self.cursor = self.conn.cursor()
            print("Connexion à la base de données réussie")
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur de connexion", f"Erreur: {err}")
            root.destroy()
            return
            
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Initialisation des frames
        self.login_frame = ttk.Frame(self.root, padding=20)
        self.register_frame = ttk.Frame(self.root, padding=20)
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.transaction_frame = ttk.Frame(self.root, padding=20)
        self.banker_frame = ttk.Frame(self.root, padding=20)
        
        # Initialisation des composants
        self.init_login_frame()
        self.init_register_frame()
        self.init_main_frame()
        self.init_transaction_frame()
        self.init_banker_frame()
        
        # Afficher le frame de connexion
        self.show_login()
    
    def init_login_frame(self):
        # Frame de connexion
        login_label = ttk.Label(self.login_frame, text="Connexion", font=('Arial', 16, 'bold'))
        login_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.login_frame, text="Email:").grid(row=1, column=0, sticky='w', pady=5)
        self.login_email = ttk.Entry(self.login_frame, width=30)
        self.login_email.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.login_frame, text="Mot de passe:").grid(row=2, column=0, sticky='w', pady=5)
        self.login_password = ttk.Entry(self.login_frame, width=30, show="*")
        self.login_password.grid(row=2, column=1, pady=5)
        
        login_btn = ttk.Button(self.login_frame, text="Se connecter", command=self.login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        register_link = ttk.Button(self.login_frame, text="Créer un compte", command=self.show_register)
        register_link.grid(row=4, column=0, columnspan=2, pady=5)
    
    def init_register_frame(self):
        # Frame d'inscription
        register_label = ttk.Label(self.register_frame, text="Créer un compte", font=('Arial', 16, 'bold'))
        register_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.register_frame, text="Nom:").grid(row=1, column=0, sticky='w', pady=5)
        self.reg_nom = ttk.Entry(self.register_frame, width=30)
        self.reg_nom.grid(row=1, column=1, pady=5)
        
        ttk.Label(self.register_frame, text="Prénom:").grid(row=2, column=0, sticky='w', pady=5)
        self.reg_prenom = ttk.Entry(self.register_frame, width=30)
        self.reg_prenom.grid(row=2, column=1, pady=5)
        
        ttk.Label(self.register_frame, text="Email:").grid(row=3, column=0, sticky='w', pady=5)
        self.reg_email = ttk.Entry(self.register_frame, width=30)
        self.reg_email.grid(row=3, column=1, pady=5)
        
        ttk.Label(self.register_frame, text="Mot de passe:").grid(row=4, column=0, sticky='w', pady=5)
        self.reg_password = ttk.Entry(self.register_frame, width=30, show="*")
        self.reg_password.grid(row=4, column=1, pady=5)
        
        ttk.Label(self.register_frame, text="Type de compte:").grid(row=5, column=0, sticky='w', pady=5)
        self.reg_role = ttk.Combobox(self.register_frame, values=["client", "banquier"], state="readonly")
        self.reg_role.current(0)
        self.reg_role.grid(row=5, column=1, pady=5)
        
        register_btn = ttk.Button(self.register_frame, text="S'inscrire", command=self.register)
        register_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
        back_btn = ttk.Button(self.register_frame, text="Retour", command=self.show_login)
        back_btn.grid(row=7, column=0, columnspan=2, pady=5)
    
    def init_main_frame(self):
        # Frame principal (après connexion)
        self.welcome_label = ttk.Label(self.main_frame, text="", font=('Arial', 16, 'bold'))
        self.welcome_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        self.balance_label = ttk.Label(self.main_frame, text="Solde: 0.00 €", font=('Arial', 14))
        self.balance_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        # Boutons pour les actions
        deposit_btn = ttk.Button(self.main_frame, text="Déposer de l'argent", command=self.deposit_money)
        deposit_btn.grid(row=2, column=0, pady=10, padx=5)
        
        withdraw_btn = ttk.Button(self.main_frame, text="Retirer de l'argent", command=self.withdraw_money)
        withdraw_btn.grid(row=2, column=1, pady=10, padx=5)
        
        transfer_btn = ttk.Button(self.main_frame, text="Transférer de l'argent", command=self.transfer_money)
        transfer_btn.grid(row=2, column=2, pady=10, padx=5)
        
        # Historique des transactions
        ttk.Label(self.main_frame, text="Historique des transactions", font=('Arial', 12, 'bold')).grid(row=3, column=0, columnspan=3, pady=5)
        
        # Tableau pour l'historique
        cols = ('Date', 'Type', 'Montant', 'Catégorie', 'Description')
        self.transaction_tree = ttk.Treeview(self.main_frame, columns=cols, show='headings', height=10)
        
        for col in cols:
            self.transaction_tree.heading(col, text=col)
            self.transaction_tree.column(col, width=120)
        
        self.transaction_tree.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Scrollbar pour le tableau
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.transaction_tree.yview)
        scrollbar.grid(row=4, column=3, sticky='ns')
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bouton pour afficher le graphique
        graph_btn = ttk.Button(self.main_frame, text="Voir Graphique", command=self.show_transaction_frame)
        graph_btn.grid(row=5, column=0, columnspan=3, pady=10)
        
        # Bouton de déconnexion
        logout_btn = ttk.Button(self.main_frame, text="Déconnexion", command=self.logout)
        logout_btn.grid(row=6, column=0, columnspan=3, pady=10)
    
    def init_transaction_frame(self):
        # Frame pour le graphique des transactions
        ttk.Label(self.transaction_frame, text="Graphique des Transactions", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Frame pour contenir le graphique
        self.graph_frame = ttk.Frame(self.transaction_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        back_btn = ttk.Button(self.transaction_frame, text="Retour", command=self.back_to_main)
        back_btn.pack(pady=10)
    
    def init_banker_frame(self):
        # Frame pour les banquiers
        ttk.Label(self.banker_frame, text="Vue Banquier - Toutes les Transactions", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Liste déroulante pour sélectionner un client
        ttk.Label(self.banker_frame, text="Sélectionner un client:").grid(row=1, column=0, sticky='w', pady=5)
        self.client_combo = ttk.Combobox(self.banker_frame, state="readonly", width=40)
        self.client_combo.grid(row=1, column=1, pady=5)
        self.client_combo.bind("<<ComboboxSelected>>", self.load_client_transactions)
        
        # Tableau pour les transactions des clients
        cols = ('Date', 'Client', 'Type', 'Montant', 'Catégorie', 'Description')
        self.banker_tree = ttk.Treeview(self.banker_frame, columns=cols, show='headings', height=15)
        
        for col in cols:
            self.banker_tree.heading(col, text=col)
            self.banker_tree.column(col, width=120)
        
        self.banker_tree.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Scrollbar pour le tableau
        scrollbar = ttk.Scrollbar(self.banker_frame, orient="vertical", command=self.banker_tree.yview)
        scrollbar.grid(row=2, column=2, sticky='ns')
        self.banker_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bouton pour afficher le graphique de tous les clients
        graph_all_btn = ttk.Button(self.banker_frame, text="Graphique Global", command=self.show_all_transactions_graph)
        graph_all_btn.grid(row=3, column=0, pady=10)
        
        # Bouton de déconnexion
        logout_btn = ttk.Button(self.banker_frame, text="Déconnexion", command=self.logout)
        logout_btn.grid(row=3, column=1, pady=10)
    
    def show_login(self):
        self.register_frame.pack_forget()
        self.main_frame.pack_forget()
        self.transaction_frame.pack_forget()
        self.banker_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)
    
    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack(fill='both', expand=True)
    
    def show_main(self):
        self.login_frame.pack_forget()
        self.transaction_frame.pack_forget()
        self.banker_frame.pack_forget()
        self.main_frame.pack(fill='both', expand=True)
        self.update_balance()
        self.load_transactions()
    
    def show_transaction_frame(self):
        self.main_frame.pack_forget()
        self.transaction_frame.pack(fill='both', expand=True)
        self.generate_transaction_graph()
    
    def show_banker_view(self):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        self.banker_frame.pack(fill='both', expand=True)
        self.load_clients()
        self.load_all_transactions()
    
    def back_to_main(self):
        self.transaction_frame.pack_forget()
        self.show_main()
    
    def hash_password(self, password):
        # Hashage simple du mot de passe (en production, utilisez bcrypt)
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        email = self.login_email.get()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Vérifier si l'utilisateur existe
        self.cursor.execute("SELECT id_utilisateur, nom, prenom, email, mot_de_passe, role FROM utilisateurs WHERE email = %s", (email,))
        user = self.cursor.fetchone()
        
        if not user or user[4] != self.hash_password(password):
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect")
            return
        
        # Mettre à jour la dernière connexion
        self.cursor.execute("UPDATE utilisateurs SET derniere_connexion = %s WHERE id_utilisateur = %s", 
                           (datetime.now(), user[0]))
        self.conn.commit()
        
        # Enregistrer les informations de l'utilisateur
        self.current_user_id = user[0]
        self.current_user = f"{user[1]} {user[2]}"
        self.current_role = user[5]
        
        if self.current_role == 'banquier':
            self.show_banker_view()
        else:
            # Vérifier si l'utilisateur a un compte
            self.cursor.execute("SELECT id_compte FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
            account = self.cursor.fetchone()
            
            if not account:
                # Créer un compte pour l'utilisateur
                self.cursor.execute("INSERT INTO comptes (id_utilisateur) VALUES (%s)", (self.current_user_id,))
                self.conn.commit()
            
            self.welcome_label.config(text=f"Bienvenue, {self.current_user}")
            self.show_main()
    
    def register(self):
        nom = self.reg_nom.get()
        prenom = self.reg_prenom.get()
        email = self.reg_email.get()
        password = self.reg_password.get()
        role = self.reg_role.get()
        
        if not nom or not prenom or not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Validation simple de l'email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erreur", "Format d'email invalide")
            return
        
        # Vérifier si l'email existe déjà
        self.cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE email = %s", (email,))
        if self.cursor.fetchone():
            messagebox.showerror("Erreur", "Cet email est déjà utilisé")
            return
        
        # Enregistrer l'utilisateur
        try:
            hashed_password = self.hash_password(password)
            self.cursor.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s)",
                (nom, prenom, email, hashed_password, role)
            )
            self.conn.commit()
            
            # Récupérer l'ID de l'utilisateur créé
            self.cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE email = %s", (email,))
            user_id = self.cursor.fetchone()[0]
            
            # Si c'est un client, créer un compte
            if role == 'client':
                self.cursor.execute("INSERT INTO comptes (id_utilisateur) VALUES (%s)", (user_id,))
                self.conn.commit()
            
            messagebox.showinfo("Succès", "Compte créé avec succès")
            self.show_login()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors de l'inscription: {err}")
    
    def update_balance(self):
        # Mettre à jour le solde affiché
        if self.current_user_id and self.current_role == 'client':
            self.cursor.execute("SELECT solde FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
            balance = self.cursor.fetchone()[0]
            self.balance_label.config(text=f"Solde: {balance:.2f} €")
    
    def load_transactions(self):
        # Charger les transactions de l'utilisateur
        if self.current_user_id and self.current_role == 'client':
            # Récupérer l'ID du compte
            self.cursor.execute("SELECT id_compte FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
            account_id = self.cursor.fetchone()[0]
            
            # Récupérer les transactions
            self.cursor.execute("""
                SELECT t.date_transaction, t.type_transaction, t.montant, c.nom, t.description
                FROM transactions t
                JOIN categories c ON t.id_categorie = c.id_categorie
                WHERE t.id_compte = %s
                ORDER BY t.date_transaction DESC
            """, (account_id,))
            
            # Effacer les anciennes transactions
            for item in self.transaction_tree.get_children():
                self.transaction_tree.delete(item)
            
            # Ajouter les nouvelles transactions
            for transaction in self.cursor.fetchall():
                date = transaction[0].strftime("%Y-%m-%d %H:%M")
                type_trans = transaction[1]
                montant = f"{transaction[2]:.2f} €"
                categorie = transaction[3]
                description = transaction[4] or ""
                
                self.transaction_tree.insert("", "end", values=(date, type_trans, montant, categorie, description))
    
    def generate_transaction_graph(self):
        if not self.current_user_id or self.current_role != 'client':
            return
        
        # Récupérer l'ID du compte
        self.cursor.execute("SELECT id_compte FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
        account_id = self.cursor.fetchone()[0]
        
        # Récupérer les transactions des derniers mois
        self.cursor.execute("""
            SELECT DATE_FORMAT(date_transaction, '%Y-%m') as month, 
                   SUM(CASE WHEN type_transaction = 'depot' THEN montant ELSE 0 END) as deposits,
                   SUM(CASE WHEN type_transaction = 'retrait' THEN montant ELSE 0 END) as withdrawals
            FROM transactions
            WHERE id_compte = %s
            GROUP BY DATE_FORMAT(date_transaction, '%Y-%m')
            ORDER BY month
        """, (account_id,))
        
        data = self.cursor.fetchall()
        
        if not data:
            messagebox.showinfo("Info", "Pas assez de données pour générer un graphique")
            return
        
        # Préparer les données pour le graphique
        months = [row[0] for row in data]
        deposits = [float(row[1]) for row in data]
        withdrawals = [float(row[2]) for row in data]
        
        # Créer la figure
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Créer le graphique à barres
        x = np.arange(len(months))
        width = 0.35
        
        ax.bar(x - width/2, deposits, width, label='Dépôts')
        ax.bar(x + width/2, withdrawals, width, label='Retraits')
        
        ax.set_title('Activité du compte par mois')
        ax.set_xlabel('Mois')
        ax.set_ylabel('Montant (€)')
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()
        
        # Intégrer le graphique dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def deposit_money(self):
        if not self.current_user_id or self.current_role != 'client':
            return
            
        amount = simpledialog.askfloat("Dépôt", "Montant à déposer:", minvalue=0.01)
        if not amount:
            return
            
        # Récupérer l'ID de la catégorie et du compte
        self.cursor.execute("SELECT id_categorie FROM categories WHERE nom = 'Autres'")
        category_id = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT id_compte FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
        account_id = self.cursor.fetchone()[0]
        
        # Créer une référence unique
        reference = str(uuid.uuid4()).replace("-", "")[:10]
        
        # Créer la transaction
        try:
            # Mettre à jour le solde
            self.cursor.execute("UPDATE comptes SET solde = solde + %s WHERE id_compte = %s", 
                               (amount, account_id))
            
            # Enregistrer la transaction
            self.cursor.execute("""
                INSERT INTO transactions 
                (reference, description, montant, type_transaction, id_compte, id_categorie) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (reference, "Dépôt d'argent", amount, "depot", account_id, category_id))
            
            self.conn.commit()
            messagebox.showinfo("Succès", f"{amount:.2f} € déposés avec succès")
            self.update_balance()
            self.load_transactions()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors du dépôt: {err}")
    
    def withdraw_money(self):
        if not self.current_user_id or self.current_role != 'client':
            return
            
        # Récupérer le solde actuel
        self.cursor.execute("SELECT solde FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
        balance = self.cursor.fetchone()[0]
        
        amount = simpledialog.askfloat("Retrait", "Montant à retirer:", minvalue=0.01, maxvalue=float(balance))
        if not amount:
            return
        
        # Boîte de dialogue pour choisir la catégorie
        self.cursor.execute("SELECT id_categorie, nom FROM categories")
        categories = {cat[1]: cat[0] for cat in self.cursor.fetchall()}
        
        category = simpledialog.askstring(
            "Catégorie", 
            "Choisissez une catégorie pour cette transaction:",
            initialvalue="Autres"
        )
        
        if not category or category not in categories:
            category = "Autres"
        
        category_id = categories[category]
        
        # Demander une description
        description = simpledialog.askstring("Description", "Description (optionnelle):")
        
        # Récupérer l'ID du compte
        self.cursor.execute("SELECT id_compte FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
        account_id = self.cursor.fetchone()[0]
        
        # Créer une référence unique
        reference = str(uuid.uuid4()).replace("-", "")[:10]
        
        # Créer la transaction
        try:
            # Mettre à jour le solde
            self.cursor.execute("UPDATE comptes SET solde = solde - %s WHERE id_compte = %s", 
                               (amount, account_id))
            
            # Enregistrer la transaction
            self.cursor.execute("""
                INSERT INTO transactions 
                (reference, description, montant, type_transaction, id_compte, id_categorie) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (reference, description or "Retrait d'argent", amount, "retrait", account_id, category_id))
            
            self.conn.commit()
            messagebox.showinfo("Succès", f"{amount:.2f} € retirés avec succès")
            self.update_balance()
            self.load_transactions()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors du retrait: {err}")
    
    def transfer_money(self):
        if not self.current_user_id or self.current_role != 'client':
            return
            
        # Récupérer le solde actuel
        self.cursor.execute("SELECT solde FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
        balance = self.cursor.fetchone()[0]
        
        # Récupérer l'ID du compte source
        self.cursor.execute("SELECT id_compte FROM comptes WHERE id_utilisateur = %s", (self.current_user_id,))
        source_account_id = self.cursor.fetchone()[0]
        
        # Demander l'email du destinataire
        recipient_email = simpledialog.askstring("Destinataire", "Email du destinataire:")
        if not recipient_email:
            return
            
        # Vérifier si le destinataire existe
        self.cursor.execute("""
            SELECT c.id_compte 
            FROM comptes c
            JOIN utilisateurs u ON c.id_utilisateur = u.id_utilisateur
            WHERE u.email = %s
        """, (recipient_email,))
        
        recipient = self.cursor.fetchone()
        if not recipient:
            messagebox.showerror("Erreur", "Destinataire introuvable")
            return
            
        recipient_account_id = recipient[0]
        
        # Vérifier que le destinataire n'est pas le même que l'expéditeur
        if recipient_account_id == source_account_id:
            messagebox.showerror("Erreur", "Vous ne pouvez pas transférer de l'argent à vous-même")
            return
            
        # Demander le montant
        amount = simpledialog.askfloat("Transfert", "Montant à transférer:", minvalue=0.01, maxvalue=float(balance))
        if not amount:
            return
            
        # Demander une description
        description = simpledialog.askstring("Description", "Description (optionnelle):")
        
        # Récupérer l'ID de la catégorie
        self.cursor.execute("SELECT id_categorie FROM categories WHERE nom = 'Autres'")
        category_id = self.cursor.fetchone()[0]
        
        # Créer une référence unique
        reference = str(uuid.uuid4()).replace("-", "")[:10]
        
        # Effectuer le transfert
        try:
            # Déduire du compte source
            self.cursor.execute("UPDATE comptes SET solde = solde - %s WHERE id_compte = %s", 
                               (amount, source_account_id))
            
            # Ajouter au compte destinataire
            self.cursor.execute("UPDATE comptes SET solde = solde + %s WHERE id_compte = %s", 
                               (amount, recipient_account_id))
            
            # Enregistrer la transaction source
            self.cursor.execute("""
                INSERT INTO transactions 
                (reference, description, montant, type_transaction, id_compte, id_compte_destination, id_categorie) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (reference, description or "Transfert d'argent", amount, "transfert", 
                  source_account_id, recipient_account_id, category_id))
            
            self.conn.commit()
            messagebox.showinfo("Succès", f"{amount:.2f} € transférés avec succès")
            self.update_balance()
            self.load_transactions()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur lors du transfert: {err}")
    
    def load_clients(self):
        # Charger la liste des clients pour le banquier
            self.cursor.execute("""
                SELECT u.id_utilisateur, u.nom, u.prenom, u.email 
                FROM utilisateurs u
                JOIN comptes c ON u.id_utilisateur = c.id_utilisateur
                WHERE u.role = 'client'
                ORDER BY u.nom, u.prenom
            """)
            
            clients = self.cursor.fetchall()
            client_list = ["Tous les clients"]
            client_list.extend([f"{client[1]} {client[2]} ({client[3]})" for client in clients])
            
            self.client_combo['values'] = client_list
            self.client_combo.current(0)
    
    def load_all_transactions(self):
        # Charger toutes les transactions pour le banquier
        self.cursor.execute("""
            SELECT t.date_transaction, CONCAT(u.nom, ' ', u.prenom), 
                   t.type_transaction, t.montant, c.nom, t.description
            FROM transactions t
            JOIN comptes cpt ON t.id_compte = cpt.id_compte
            JOIN utilisateurs u ON cpt.id_utilisateur = u.id_utilisateur
            JOIN categories c ON t.id_categorie = c.id_categorie
            ORDER BY t.date_transaction DESC
        """)
        
        # Effacer les anciennes transactions
        for item in self.banker_tree.get_children():
            self.banker_tree.delete(item)
        
        # Ajouter les nouvelles transactions
        for transaction in self.cursor.fetchall():
            date = transaction[0].strftime("%Y-%m-%d %H:%M")
            client = transaction[1]
            type_trans = transaction[2]
            montant = f"{transaction[3]:.2f} €"
            categorie = transaction[4]
            description = transaction[5] or ""
            
            self.banker_tree.insert("", "end", values=(date, client, type_trans, montant, categorie, description))
    
    def load_client_transactions(self, event):
        # Charger les transactions d'un client spécifique
        selected_client = self.client_combo.get()
        
        # Effacer les anciennes transactions
        for item in self.banker_tree.get_children():
            self.banker_tree.delete(item)
        
        if selected_client == "Tous les clients":
            self.load_all_transactions()
            return
        
        # Extraire l'email du client
        email = selected_client.split('(')[1].split(')')[0]
        
        # Charger les transactions du client
        self.cursor.execute("""
            SELECT t.date_transaction, CONCAT(u.nom, ' ', u.prenom), 
                   t.type_transaction, t.montant, c.nom, t.description
            FROM transactions t
            JOIN comptes cpt ON t.id_compte = cpt.id_compte
            JOIN utilisateurs u ON cpt.id_utilisateur = u.id_utilisateur
            JOIN categories c ON t.id_categorie = c.id_categorie
            WHERE u.email = %s
            ORDER BY t.date_transaction DESC
        """, (email,))
        
        # Ajouter les nouvelles transactions
        for transaction in self.cursor.fetchall():
            date = transaction[0].strftime("%Y-%m-%d %H:%M")
            client = transaction[1]
            type_trans = transaction[2]
            montant = f"{transaction[3]:.2f} €"
            categorie = transaction[4]
            description = transaction[5] or ""
            
            self.banker_tree.insert("", "end", values=(date, client, type_trans, montant, categorie, description))
    
    def show_all_transactions_graph(self):
        # Générer un graphique de toutes les transactions pour le banquier
        # Récupérer les données des transactions par catégorie
        self.cursor.execute("""
            SELECT c.nom, SUM(t.montant)
            FROM transactions t
            JOIN categories c ON t.id_categorie = c.id_categorie
            WHERE t.type_transaction = 'retrait'
            GROUP BY c.nom
            ORDER BY SUM(t.montant) DESC
        """)
        
        categories_data = self.cursor.fetchall()
        
        if not categories_data:
            messagebox.showinfo("Info", "Pas assez de données pour générer un graphique")
            return
            
        # Créer une fenêtre pour le graphique
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Graphique Global des Transactions")
        graph_window.geometry("800x600")
        
        # Créer le cadre pour le graphique
        graph_frame = ttk.Frame(graph_window)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Créer les onglets pour différents graphiques
        notebook = ttk.Notebook(graph_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Onglet 1: Répartition des dépenses par catégorie
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Répartition par Catégorie")
        
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        categories = [cat[0] for cat in categories_data]
        amounts = [float(cat[1]) for cat in categories_data]
        
        ax1.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, shadow=True)
        ax1.axis('equal')
        ax1.set_title('Répartition des dépenses par catégorie')
        
        canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Onglet 2: Évolution des transactions dans le temps
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Évolution Temporelle")
        
        # Récupérer les données des transactions par mois
        self.cursor.execute("""
            SELECT DATE_FORMAT(date_transaction, '%Y-%m') as month, 
                   SUM(CASE WHEN type_transaction = 'depot' THEN montant ELSE 0 END) as deposits,
                   SUM(CASE WHEN type_transaction = 'retrait' THEN montant ELSE 0 END) as withdrawals
            FROM transactions
            GROUP BY DATE_FORMAT(date_transaction, '%Y-%m')
            ORDER BY month
        """)
        
        time_data = self.cursor.fetchall()
        
        if time_data:
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            
            months = [data[0] for data in time_data]
            deposits = [float(data[1]) for data in time_data]
            withdrawals = [float(data[2]) for data in time_data]
            
            ax2.plot(months, deposits, 'b-', label='Dépôts')
            ax2.plot(months, withdrawals, 'r-', label='Retraits')
            
            ax2.set_title('Évolution des transactions dans le temps')
            ax2.set_xlabel('Mois')
            ax2.set_ylabel('Montant (€)')
            ax2.legend()
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bouton pour fermer la fenêtre
        ttk.Button(graph_window, text="Fermer", command=graph_window.destroy).pack(pady=10)
    
    def logout(self):
        # Déconnexion
        self.current_user = None
        self.current_user_id = None
        self.current_role = None
        
        # Effacer les champs de connexion
        self.login_email.delete(0, tk.END)
        self.login_password.delete(0, tk.END)
        
        self.show_login()

# Fonction principale
def main():
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()