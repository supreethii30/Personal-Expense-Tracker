from expense import Expense
import calendar
import datetime


def main():
    print(f"Running Expense Tracker!")
    expense_file_path = "expense.csv"
    budget = 10000
    
    # Get User input for expense.
    expense =  get_user_expense()
    
    #Write their expense to a file.
    save_expense_to_file(expense, expense_file_path)
    #Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)
   

def get_user_expense():
    print(f"Getting User Expense")
    expense_name = input("Enter Expense Name: ")
    expense_amount = float(input("Enter Expense amount: "))
    #print(f"You've Entered {expense_name}, {expense_amount}")
    
    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "🏙️ Work", 
        "🎉 Entertainment", 
        "😃 Beauty Expenses",
    ]
    
    while True:
        print("Select a Category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")
        
        value_range = f"[1-{len(expense_categories)}]"
        selected_index = int(input(f"Enter a Category Number {value_range}: ")) - 1
       
        if selected_index in range(len(expense_categories)):  
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount
                                  )
            return new_expense
        else:
            print("❌ Invalid category. Please Try Again!")

        

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")
   


#how much i left in my budget {the budget calculates}
def summarize_expenses(expense_file_path, budget):
    print(f"Summarizing User Expense")
    expenses: list[Expense] = []
    with open(expense_file_path, "r", encoding="utf-8") as f:
       lines = f.readlines()
       for line in lines:
            expense_name, expense_category, expense_amount =  line.strip().split(",")  #this can/will be the list or tuples
            line_expense = Expense(
                name=expense_name, category=expense_category, amount=float(expense_amount)
                )
            expenses.append(line_expense)
            
       
            amount_by_category = {}
            for expense in expenses:
                key = expense.category
                if key in amount_by_category:
                    amount_by_category[key]  += expense.amount   #adding to the expense
                else:
                    amount_by_category[key] = expense.amount
            print("Expenses By Category:  ")        
            for key, amount in amount_by_category.items():
                print(f"    {key}: ₹{amount:.2f}") 
            
            total_spent = sum([ex.amount for ex in expenses])   #Sum takes list as argument{this line just becomes a list of just the dollar value of each expense}
            print(f"Youu've Spent: ₹{total_spent:.2f} this month!")
            
            remaining_budget = budget - total_spent
            print(f"The Remaining Budget:  ₹{remaining_budget:.2f}")
            
            #Get the Current dat
            now = datetime.datetime.now()
            
        #Get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    
    #calculate the remaining number of days in the current month
    remaining_days = days_in_month - now.day
    
    print("Remaining days in the current month: ", remaining_days)
    
    daily_budget = remaining_budget / remaining_days
    print(green(f"Budget Per Day: ₹{daily_budget:.2f}"))   
    
    
def green(text):
    return f"\033[92m{text}\033[0m"
    
if __name__ == "__main__":   #special variable
    main()