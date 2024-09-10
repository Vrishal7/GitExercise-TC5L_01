import tkinter as tk
from tkinter import messagebox

class KidsColouringApp:
    def __init__(self,root):
        self.root=root
        self.root.title('Kids Colouring App')

        #initial value of coins
        self.coins=0
        self.easy_level=["Level" +str(i+1)for i in range(15)]
        
        self.create_widgets()

    def create_widgets(self):
        self.coins_label=tk.Label(self.root,text=f'Coins:{self.coins}',font=('Arial',16))
        self.coins_label.pack(pady=10)

        #Select colouring page
        self.selected_page=tk.StringVar()

        tk.Label(self.root,text='Select Colouring Page:',font=('Arial',14)).pack(pady=5)
        
        #Easy Level
        self.level_var=tk.StringVar(value='easy')
        tk.Radiobutton(self.root,text="Easy Level",variable=self.level_var,value='easy',command=self.update_page_list).pack()

        self.page_listbox=tk.Listbox(self.root,width=30) #list the levels (example)
        self.page_listbox.pack(pady=10)

        # add button to redeem coins
        self.complete_button=tk.Button(self.root,text='Complete Colouring Page',command=self.complete_page)
        self.complete_button.pack(pady=5)

        self.update_page_list()

    def update_page_list(self):
        self.page_listbox.delete(0,tk.END)

        current_level=self.level_var.get()
        if current_level =='easy':
            for page in self.easy_level:
                self.page_listbox.insert(tk.END,page)

    def complete_page(self):
        current_level = self.level_var.get()
        if current_level == 'easy':
            self.coins +=2 
            messagebox.showinfo('Good job','You have completed an Easy colouring page') #display msg

            self.coins_label.config(text=f'Coins:{self.coins}')

if __name__ == "__main__":
     root=tk.Tk()
     app=KidsColouringApp(root)
     root.mainloop()            




        




        


