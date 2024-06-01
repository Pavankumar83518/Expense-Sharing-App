
import sqlite3
import datetime

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

while True:
  print("Select an option:")
  print("1.Enter a new expense")
  print("2.View expenses summary")
  choice = int(input())
  if choice == 1:
    date = input("Enter the date of the expenses (YYYY-MM-DD): ")
    description = input("Enter the description of the expense: ")
    cur.execute("SELECT DISTINCT category FROM expenses")
    categories = cur.fetchall()
    print("Select a category by number:")
    for idx,category in enumerate(categories):
       print(f"{idx +1},{category[0]}")
    print(f"{len(categories) +1}.Create a new category")
    category_choice=int(input())
    if category_choice==len(categories)+1:
       category=input("enter the new category name: ")
    else:
       category=categories[category_choice-1][0]
    price=float(input("enter the price of the expense: "))

    tip = int(input("enter the percentage of tip? 10,12,15: "))
    people = int(input("how many people to split the bill: "))
    tip_as_percentage= tip/100
    total_tip=tip_as_percentage*price
    total_bill = price + total_tip
    bill_per_person = total_bill / people
    final_amount = round(bill_per_person, 2)
    print(f"each person has to pay:Rs {final_amount}")
    cur.execute("INSERT INTO expenses (Date,category,description,total_members,amount_for_each_member,actual_price,total_price_with_tip) VALUES (?,?,?,?,?,?,?)",(date,category,description,people,final_amount,price,total_bill))
    conn.commit()
  elif choice==2:
      table_name = ('expenses')

      # Check if the table is empty
      cur.execute(f"SELECT COUNT(*) FROM {table_name}")
      result = cur.fetchone()[0]

      if result == 0:
          print(f"The table '{table_name}' is empty.")
      else:
          print("Select an option:")
          print("1.View all expenses")
          print("2.View monthly expenses by category")
          view_choice=int(input())
          if view_choice==1:
              cur.execute("SELECT*FROM expenses")
              expenses=cur.fetchall()
              for expense in expenses:
                  print(expense)
          elif view_choice==2:
              month=input("enter the month (MM): ")
              year=input("enter the year (YYYY): ")
              cur.execute("""SELECT category,SUM(total_price_with_tip) FROM expenses
                             WHERE strftime('%m',Date)=? AND strftime('%Y',Date)=?
                             GROUP BY category""",(month,year))
              expenses=cur.fetchall()
              for expense in expenses:
                 print(f"Category:{expense[0]},Total:{expense[1]}")

          else:
           exit()
  else:
    exit()
  repeat = input("Would you like to do something else (yes/no)?\n")
  if repeat.lower() !="yes":
    break
conn.close()
