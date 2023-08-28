from tkinter import *
from tkinter import messagebox
import random
import hashlib

# User class to represent a chat user
class User:
    def __init__(self, name):
        self.name = name
        self.private_chats = []

    def create_private_chat(self, recipient):
        private_chat = PrivateChat(self, recipient)
        self.private_chats.append(private_chat)
        recipient.private_chats.append(private_chat)

    def send_message(self, recipient, message):
        private_chat = self.get_private_chat(recipient)
        if private_chat:
            private_chat.send_message(self, message)

    def get_private_chat(self, recipient):
        for private_chat in self.private_chats:
            if private_chat.user1 == recipient or private_chat.user2 == recipient:
                return private_chat
        return None

# PrivateChat class to represent a private chat room between two users
class PrivateChat:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.messages = []

    def send_message(self, sender, message):
        self.messages.append((sender, message))

# ChatApp class to handle the chat application UI
class ChatApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Chat App")
        self.root.configure(bg="#F0F0F0")  # Set background color

        # User list
        self.user_list = Listbox(self.root, bg="#FFFFFF")  # Set background color
        self.user_list.pack(side=LEFT, fill=Y)

        # Message box
        self.message_box = Text(self.root, bg="#FFFFFF", state=DISABLED)  # Set background color and disable editing
        self.message_box.pack(fill=BOTH, expand=True)

        # Message entry
        self.message_entry = Entry(self.root)
        self.message_entry.pack(side=BOTTOM, fill=X)

        # Register frame
        self.register_frame = Frame(self.root, bg="#F0F0F0")  # Set background color
        self.register_frame.pack(side=TOP, fill=X)

        # Username entry
        self.username_entry = Entry(self.register_frame)
        self.username_entry.pack(side=LEFT)

        # Register button
        self.register_button = Button(self.register_frame, text="Register", command=self.register_user,
                                      bg="#A9A9A9", fg="#FFFFFF")  # Set button color and text color
        self.register_button.pack(side=LEFT)

        # Start private chat button
        self.start_chat_button = Button(self.root, text="Start Private Chat", command=self.create_private_chat,
                                        bg="#008080", fg="#FFFFFF")  # Set button color and text color
        self.start_chat_button.pack(side=TOP, fill=X)

        # Send message button
        self.send_button = Button(self.root, text="Send", command=self.send_message,
                                  bg="#008080", fg="#FFFFFF")  # Set button color and text color
        self.send_button.pack(side=BOTTOM, fill=X)

        self.users = []
        self.current_user = None

    def hash_name(self, name):
        hashed_name = hashlib.md5(name.encode()).hexdigest()
        return hashed_name

    def register_user(self):
        name = self.username_entry.get().strip()
        if name:
            hashed_name = self.hash_name(name)
            user = User(hashed_name)
            self.users.append(user)
            self.user_list.insert(END, hashed_name)
            self.username_entry.delete(0, END)
            self.current_user = user
        else:
            messagebox.showinfo("Error", "Please enter a username to register.")

    def create_private_chat(self):
        selected_user_index = self.user_list.curselection()
        if selected_user_index:
            selected_user = self.users[selected_user_index[0]]
            if selected_user != self.current_user:
                self.current_user.create_private_chat(selected_user)
                self.update_chat_box()

                # Display start message
                start_message = f"Private chat with {selected_user.name} started!"
                self.display_message(start_message)
            else:
                messagebox.showinfo("Error", "Cannot start a private chat with yourself.")
        else:
            messagebox.showinfo("Error", "Please select a user to start a private chat.")

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            selected_user_index = self.user_list.curselection()
            if selected_user_index:
                selected_user = self.users[selected_user_index[0]]
                self.current_user.send_message(selected_user, message)
                self.display_message(f"You: {message}")
                self.message_entry.delete(0, END)
            else:
                messagebox.showinfo("Error", "Please select a user to send a message to.")
        else:
            messagebox.showinfo("Error", "Please enter a message to send.")

    def update_chat_box(self):
        self.message_box.config(state=NORMAL)  # Enable editing
        self.message_box.delete(1.0, END)
        selected_user_index = self.user_list.curselection()
        if selected_user_index:
            selected_user = self.users[selected_user_index[0]]
            private_chat = self.current_user.get_private_chat(selected_user)
            if private_chat:
                for sender, message in private_chat.messages:
                    if sender == self.current_user:
                        self.display_message(f"You: {message}")
                    else:
                        self.display_message(f"{sender.name}: {message}")
        self.message_box.config(state=DISABLED)  # Disable editing

    def display_message(self, message):
        self.message_box.config(state=NORMAL)  # Enable editing
        self.message_box.insert(END, message + "\n")
        self.message_box.see(END)  # Scroll to the end of the message box
        self.message_box.config(state=DISABLED)  # Disable editing

    def run(self):
        self.root.mainloop()

# Create an instance of the ChatApp and run it
app = ChatApp()
app.run()
