#Question 1:
class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.dependencies = []
        self.EST = 0  
        self.EFT = 0  
        self.LST = float('inf')  
        self.LFT = float('inf')  

def topological_sort(tasks):
    visited = set()
    stack = []

    def visit(task):
        if task not in visited:
            visited.add(task)
            for dep in task.dependencies:
                visit(dep)
            stack.append(task)

    for task in tasks:
        visit(task)

    stack.reverse()
    return stack

def calculate_times(tasks):
    sorted_tasks = topological_sort(tasks)

    for task in sorted_tasks:
        task.EFT = task.EST + task.duration
        for dep in task.dependencies:
            dep.EST = max(dep.EST, task.EFT)

    for task in reversed(sorted_tasks):
        if task.LFT == float('inf'):
            task.LFT = task.EFT
        task.LST = task.LFT - task.duration
        for dep in task.dependencies:
            dep.LFT = min(dep.LFT, task.LST)

def get_completion_times(tasks):
    latest_completion = max(task.EFT for task in tasks)
    earliest_completion = max(task.LFT for task in tasks)
    return earliest_completion, latest_completion

def main():
    task_data = [
        ('T_START', 0, []),
        ('A', 3, ['T_START']),
        ('B', 2, ['A']),
        ('C', 1, ['A']),
        ('D', 4, ['B', 'C']),
        ('E', 1, ['D'])
    ]

    tasks = {}
    for name, duration, deps in task_data:
        tasks[name] = Task(name, duration)
    
    for name, duration, deps in task_data:
        tasks[name].dependencies = [tasks[dep] for dep in deps]

    task_list = list(tasks.values())
    calculate_times(task_list)
    
    earliest_completion, latest_completion = get_completion_times(task_list)
    print(f"Earliest completion time: {earliest_completion}")
    print(f"Latest completion time: {latest_completion}")

if __name__ == "__main__":
    main()


#Question 2:

from collections import deque

class FriendshipGraph:
    def __init__(self):
        self.graph = {}

    def add_friendship(self, person, friend):
        if person not in self.graph:
            self.graph[person] = set()
        if friend not in self.graph:
            self.graph[friend] = set()
        self.graph[person].add(friend)
        self.graph[friend].add(person)

    def get_friends(self, person):
        return self.graph.get(person, set())

    def common_friends(self, person1, person2):
        return self.get_friends(person1) & self.get_friends(person2)

    def find_connection(self, start, end):
        if start not in self.graph or end not in self.graph:
            return -1
        if start == end:
            return 0

        visited = set()
        queue = deque([(start, 0)])

        while queue:
            current, level = queue.popleft()
            if current == end:
                return level
            visited.add(current)
            for friend in self.graph[current]:
                if friend not in visited:
                    queue.append((friend, level + 1))
                    visited.add(friend)
        return -1

def main():
    friendships = [
        ("Alice", "Bob"),
        ("Alice", "Carol"),
        ("Bob", "David"),
        ("David", "Eve"),
        ("Carol", "Eve"),
        ("Eve", "Frank"),
        ("Frank", "Grace"),
        ("Grace", "Heidi"),
        ("Heidi", "Ivan"),
        ("Ivan", "Judy")
    ]

    fg = FriendshipGraph()

    for person, friend in friendships:
        fg.add_friendship(person, friend)

    alice_friends = fg.get_friends("Alice")
    bob_friends = fg.get_friends("Bob")
    common_friends = fg.common_friends("Alice", "Bob")
    alice_janice_connection = fg.find_connection("Alice", "Janice")
    alice_bob_connection = fg.find_connection("Alice", "Bob")

    print("Alice's friends:", alice_friends)
    print("Bob's friends:", bob_friends)
    print("Common friends of Alice and Bob:", common_friends)
    print("Connection between Alice and Janice:", alice_janice_connection)
    print("Connection between Alice and Bob:", alice_bob_connection)

if __name__ == "__main__":
    main()

