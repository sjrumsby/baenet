class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.label = ""
        
    def updateCell(self, image):
        self.label.configure(image=image)
        self.label.photo = image
