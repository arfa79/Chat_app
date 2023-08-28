import unittest
from unittest.mock import patch, MagicMock
from tkinter import messagebox

# Import your classes here
from chat_app import User, PrivateChat, ChatApp

class TestChatApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = ChatApp()
        cls.app.root.attributes("-topmost", True)

    @classmethod
    def tearDownClass(cls):
        cls.app.root.destroy()

    @patch('tkinter.messagebox.showinfo')
    def test_register_user(self, mock_showinfo):
        self.app.username_entry.insert(0, 'Alice')
        self.app.register_user()
        self.assertEqual(len(self.app.users), 1)
        self.assertEqual(self.app.users[0].name, 'Alice')
        mock_showinfo.assert_not_called()

        self.app.username_entry.delete(0, 'end')
        self.app.register_user()
        mock_showinfo.assert_called_with("Error", "Please enter a username to register.")

    @patch('tkinter.messagebox.showinfo')
    def test_create_private_chat(self, mock_showinfo):
        user1 = User('Alice')
        user2 = User('Bob')
        self.app.users.append(user1)
        self.app.users.append(user2)
        self.app.current_user = user1

        # Valid private chat creation
        self.app.user_list.insert('end', 'Bob')
        self.app.create_private_chat()
        self.assertEqual(len(user1.private_chats), 1)
        self.assertEqual(len(user2.private_chats), 1)
        mock_showinfo.assert_not_called()

        # Trying to create private chat with self
        self.app.user_list.delete(0, 'end')
        self.app.user_list.insert('end', 'Alice')
        self.app.create_private_chat()
        mock_showinfo.assert_called_with("Error", "Cannot start a private chat with yourself.")

        # Trying to create private chat without selecting user
        self.app.user_list.delete(0, 'end')
        self.app.create_private_chat()
        mock_showinfo.assert_called_with("Error", "Please select a user to start a private chat.")

    @patch('tkinter.messagebox.showinfo')
    def test_send_message(self, mock_showinfo):
        user1 = User('Alice')
        user2 = User('Bob')
        self.app.users.append(user1)
        self.app.users.append(user2)
        self.app.current_user = user1

        self.app.user_list.insert('end', 'Bob')

        # Sending a message
        self.app.message_entry.insert(0, 'Hello, Bob!')
        self.app.send_message()
        self.assertEqual(len(user1.private_chats[0].messages), 1)
        self.assertEqual(user1.private_chats[0].messages[0][1], 'Hello, Bob!')
        mock_showinfo.assert_not_called()

        # Sending a message without selecting user
        self.app.user_list.delete(0, 'end')
        self.app.send_message()
        mock_showinfo.assert_called_with("Error", "Please select a user to send a message to.")

        # Sending an empty message
        self.app.user_list.insert('end', 'Bob')
        self.app.message_entry.delete(0, 'end')
        self.app.send_message()
        mock_showinfo.assert_called_with("Error", "Please enter a message to send.")

if __name__ == '__main__':
    unittest.main()
