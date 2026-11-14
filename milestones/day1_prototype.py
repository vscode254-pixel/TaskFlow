"""TaskFlow Day 1 prototype: basic team task tracking."""


tasks = []
next_id = 1


while True:
    print("\n" + "=" * 45)
    print("         TASKFLOW - TEAM TASK TRACKER")
    print("=" * 45)
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Complete a task")
    print("0. Exit")
    
    
    choice = input("\nEnter your choice: ").strip()
    
    
    if choice == "1":
        print("\n--- ADD NEW TASK ---")
        
        title = input("Enter task title: ").strip().title()
        person = input("Enter assigned person's name: ").strip().capitalize()
        
        
        if not title or person:
            print("Error: Title and person name are required.")
            
        else:
            task = {
                "id": next_id,
                "title": title,
                "person": person,
                "done": False
            }
            
            
            tasks.append(task)
            next_id += 1
            
            
            print("Task added successfully!")
            
            
    elif choice == "2":
        print("\n--- ALL TASK ---")
        
        if not tasks:
            print("No tasks have been added yet.")
        else:
            for task in tasks:
                status = "COMPLETED" if task["done"] else "PENDING"
                
                
                print("-" * 45)
                print(f"Task ID: {task['id']}")
                print(f"Title: {task['title']}")
                print(f"Assigned to: {task['person']}")
                print(f"Status: {status}")
                
                
                
    elif choice == "3":
        print("\n--- COMPLETE TASK ---")
        
        
        task_id = input("Enter task ID: ").strip()
        found = False
        
        for task in tasks:
            if str(task["id"]) == task_id:
                task["done"] = True
                found = True
                print("Task completed successfully!")
                break
        
        
        
        if not found:
            print("Task not found.")
            
            
    elif choice == "0":
        print("\nThank you for using TaskFlow!")
        break
    
    
    else:
        print("Invalid choice. Please try again with (1, 2, 3 and 0).")
                
                         