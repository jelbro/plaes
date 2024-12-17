class Menu:
    def display_main_menu(self):
        print(
            "   Plaes   ",
            "Select an option",
            "i: Ingredients r: Recipes p: Prep List"
            )
        choice = self.get_menu_choice(['i', 'r', 'p'])
        match choice:
            case 'i':
                self.display_ingredient_menu()
            case 'r':
                self.display_recipe_menu()
            case 'p':
                self.display_prep_list_menu()

    
    def display_ingredient_menu(self):
        ...

    
    def display_recipe_menu(self):
        ...

    
    def display_prep_list_menu(self):
        ...


    def get_menu_choice(self, options):
        while True:
            user_input = input().lower().strip()
            if user_input in options:
                return user_input
            else:
                print('Invalid Input')
                pass
