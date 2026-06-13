import pygame

# Buttons class (includes clickable buttons, and normal text features for UI)
class Buttons:
    def __init__(self, x, y, text, clickable, color = (255, 255, 255)):
        # coordinates given in main file while making the buttons
        self.x = x
        self.y = y
        
        # Text to be displayed on the button
        self.text = text
        # Takes True or False (non clickable buttons just act as a UI element to show text)
        self.clickable = clickable
        # status checks if the button is clicked
        self.status = False

        # color of the text and the rectangle
        self.text_color = color
        self.color = (49, 179, 255)

        # initialize rectangle 
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        

    def draw(self, screen):
        # Create another font variable instead of calling main file font to have different sizes
        font = pygame.font.SysFont("Courier", 20, True)

        # Width and height calculated based on text size
        text_width, text_height = font.size(self.text)

        # the rectangle dimensions modified based on text size
        self.rect = pygame.Rect(self.x, self.y, text_width + 40, text_height + 20)

        # Draw the rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        # Display text over the rectangle
        screen.blit(font.render(self.text, True, (self.text_color)), (self.x + self.rect.width//2 - len(self.text) * 6.5, self.y + self.rect.height//2 - 10))

        # Change the color when the mouse hovers over a clickable button
        mouse_pos = pygame.mouse.get_pos()
        if self.clickable:
            if self.rect.collidepoint(mouse_pos):
                self.color = (175, 210, 230)        
            else :
                self.color = (49, 179, 255)


    # Checks whether the button has been clicked, and changes its status to True
    def clickable_func(self, event):
        mouse_pos = pygame.mouse.get_pos()

        if self.clickable:
            if self.rect.collidepoint(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.status = True

