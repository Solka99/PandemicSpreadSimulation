class Agent:
    def __init__(self, id, x, y, age, health_state):
        self.id = id
        self.x = x
        self.y = y
        self.position = (x, y)
        # self.direction = direction
        self.age = age
        self.health_state = health_state

