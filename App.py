if __name__ == '__main__':
    root = tk.Tk()
    root.title('Test Keyboard')

    label = tk.Label(root, text='Test Keyboard')
    label.grid(row=0, column=0, columnspan=2)

    entry1 = tk.Entry(root)
    entry1.grid(row=1, column=0, sticky='news')
    entry1.bind("<FocusIn>", lambda event: create(root, entry1))


    entry2 = tk.Entry(root)
    entry2.grid(row=2, column=0, sticky='news')
    entry2.bind("<FocusIn>", lambda event: create(root, entry2))
    
    text1 = tk.Text(root)
    text1.grid(row=3, column=0, sticky='news')
    text1.bind("<FocusIn>", lambda event: create(root, text1))
    
    root.mainloop()
