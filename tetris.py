

# Initialize Pygame
pygame.init()

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# Screen dimensions
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * GRID_X_OFFSET + 200
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * GRID_Y_OFFSET

# Colors - Dark Mode
DARK_COLORS = {
    'BACKGROUND': (0, 0, 0),
    'TEXT': (255, 255, 255),
    'GRID_BG': (64, 64, 64),
    'GRID_LINE': (128, 128, 128),
    'OVERLAY': (0, 0, 0)
}

# Colors - Light Mode
LIGHT_COLORS = {
    'BACKGROUND': (240, 240, 240),
    'TEXT': (50, 50, 50),
    'GRID_BG': (200, 200, 200),
    'GRID_LINE': (150, 150, 150),
    'OVERLAY': (255, 255, 255)
}

# Tetromino colors (same for both modes)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Tetris pieces (tetrominoes)
TETROMINOES = {
    'I': [['.....',
           '..#..',
           '..#..',
           '..#..',
           '..#..'],
          ['.....',
           '.....',
           '####.',
           '.....',
           '.....']],
    
    'O': [['.....',
           '.....',
           '.##..',
           '.##..',
           '.....']],
    
    'T': [['.....',
           '.....',
           '.#...',
           '###..',
           '.....'],
          ['.....',
           '.....',
           '.#...',
           '.##..',
           '.#...'],
          ['.....',
           '.....',
           '.....',
           '###..',
           '.#...'],
          ['.....',
           '.....',
           '.#...',
           '##...',
           '.#...']],
    
    'S': [['.....',
           '.....',
           '.##..',
           '##...',
           '.....'],
          ['.....',
           '.#...',
           '.##..',
           '..#..',
           '.....']],
    
    'Z': [['.....',
           '.....',
           '##...',
           '.##..',
           '.....'],
          ['.....',
           '..#..',
           '.##..',
           '.#...',
           '.....']],
    
    'J': [['.....',
           '.#...',
           '.#...',
           '##...',
           '.....'],
          ['.....',
           '.....',
           '#....',
           '###..',
           '.....'],
          ['.....',
           '.##..',
           '.#...',
           '.#...',
           '.....'],
          ['.....',
           '.....',
           '###..',
           '..#..',
           '.....']],
    
    'L': [['.....',
           '..#..',
           '..#..',
           '.##..',
           '.....'],
          ['.....',
           '.....',
           '###..',
           '#....',
           '.....'],
          ['.....',
           '##...',
           '.#...',
           '.#...',
           '.....'],
          ['.....',
           '.....',
           '..#..',
           '###..',
           '.....']]
}

TETROMINO_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

class Tetromino:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = TETROMINO_COLORS[shape]
    
    def get_rotated_piece(self):
        return TETROMINOES[self.shape][self.rotation % len(TETROMINOES[self.shape])]
    
    def get_cells(self):
        cells = []
        piece = self.get_rotated_piece()
        for i, row in enumerate(piece):
            for j, cell in enumerate(row):
                if cell == '#':
                    cells.append((self.x + j, self.y + i))
        return cells

class TetrisGame:
    def __init__(self):
        self.grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.game_over = False
        self.dark_mode = True  # Toggle for dark/light mode
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
    
    def get_colors(self):
        """Get current color scheme based on mode"""
        return DARK_COLORS if self.dark_mode else LIGHT_COLORS
    
    def toggle_theme(self):
        """Toggle between dark and light mode"""
        self.dark_mode = not self.dark_mode
    
    def get_new_piece(self):
        shape = random.choice(list(TETROMINOES.keys()))
        return Tetromino(shape, GRID_WIDTH // 2 - 2, 0)
    
    def is_valid_position(self, piece, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = piece.rotation
        
        # Temporarily change piece position and rotation
        old_x, old_y, old_rotation = piece.x, piece.y, piece.rotation
        piece.x += dx
        piece.y += dy
        piece.rotation = rotation
        
        cells = piece.get_cells()
        
        # Check boundaries and collisions
        for x, y in cells:
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                piece.x, piece.y, piece.rotation = old_x, old_y, old_rotation
                return False
            if y >= 0 and self.grid[y][x] is not None:
                piece.x, piece.y, piece.rotation = old_x, old_y, old_rotation
                return False
        
        # Restore original position and rotation
        piece.x, piece.y, piece.rotation = old_x, old_y, old_rotation
        return True
    
    def place_piece(self, piece):
        cells = piece.get_cells()
        for x, y in cells:
            if y >= 0:
                self.grid[y][x] = piece.color
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(GRID_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        if lines_cleared > 0:
            # Scoring system
            points = [0, 100, 300, 500, 800][lines_cleared] * self.level
            self.score += points
            self.lines_cleared += lines_cleared
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
    
    def move_piece(self, dx, dy):
        if self.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def rotate_piece(self):
        new_rotation = (self.current_piece.rotation + 1) % len(TETROMINOES[self.current_piece.shape])
        if self.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece.rotation = new_rotation
    
    def drop_piece(self):
        if not self.move_piece(0, 1):
            self.place_piece(self.current_piece)
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.get_new_piece()
            
            # Check game over
            if not self.is_valid_position(self.current_piece):
                self.game_over = True
    
    def hard_drop(self):
        drop_distance = 0
        while self.move_piece(0, 1):
            drop_distance += 1
        self.score += drop_distance
        self.drop_piece()
    
    def update(self, dt):
        if not self.game_over:
            self.fall_time += dt
            if self.fall_time >= self.fall_speed:
                self.drop_piece()
                self.fall_time = 0
    
    def draw_grid(self, screen):
        colors = self.get_colors()
        
        # Draw grid background
        grid_rect = pygame.Rect(GRID_X_OFFSET, GRID_Y_OFFSET, 
                               GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
        pygame.draw.rect(screen, colors['GRID_BG'], grid_rect)
        
        # Draw grid lines
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(screen, colors['GRID_LINE'], 
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET),
                           (GRID_X_OFFSET + x * CELL_SIZE, GRID_Y_OFFSET + GRID_HEIGHT * CELL_SIZE))
        
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(screen, colors['GRID_LINE'],
                           (GRID_X_OFFSET, GRID_Y_OFFSET + y * CELL_SIZE),
                           (GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE, GRID_Y_OFFSET + y * CELL_SIZE))
    
    def draw_piece(self, screen, piece, offset_x=0, offset_y=0):
        colors = self.get_colors()
        cells = piece.get_cells()
        
        for x, y in cells:
            if y >= 0:
                rect = pygame.Rect((GRID_X_OFFSET + (x + offset_x) * CELL_SIZE,
                                  GRID_Y_OFFSET + (y + offset_y) * CELL_SIZE,
                                  CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, piece.color, rect)
                # Border color adapts to theme
                border_color = colors['TEXT'] if self.dark_mode else (255, 255, 255)
                pygame.draw.rect(screen, border_color, rect, 2)
    
    def draw_placed_pieces(self, screen):
        colors = self.get_colors()
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] is not None:
                    rect = pygame.Rect(GRID_X_OFFSET + x * CELL_SIZE,
                                     GRID_Y_OFFSET + y * CELL_SIZE,
                                     CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, self.grid[y][x], rect)
                    # Border color adapts to theme
                    border_color = colors['TEXT'] if self.dark_mode else (255, 255, 255)
                    pygame.draw.rect(screen, border_color, rect, 2)
    
    def draw_ui(self, screen):
        colors = self.get_colors()
        ui_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        
        # Theme indicator
        theme_text = "🌙 Dark" if self.dark_mode else "☀️ Light"
        theme_surface = self.font_medium.render(f"Theme: {theme_text}", True, colors['TEXT'])
        screen.blit(theme_surface, (ui_x, 20))
        
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, colors['TEXT'])
        screen.blit(score_text, (ui_x, 50))
        
        # Lines
        lines_text = self.font_medium.render(f"Lines: {self.lines_cleared}", True, colors['TEXT'])
        screen.blit(lines_text, (ui_x, 80))
        
        # Level
        level_text = self.font_medium.render(f"Level: {self.level}", True, colors['TEXT'])
        screen.blit(level_text, (ui_x, 110))
        
        # Next piece
        next_text = self.font_medium.render("Next:", True, colors['TEXT'])
        screen.blit(next_text, (ui_x, 150))
        
        # Draw next piece preview
        if self.next_piece:
            preview_x = ui_x // CELL_SIZE
            preview_y = 200 // CELL_SIZE
            temp_piece = Tetromino(self.next_piece.shape, preview_x, preview_y)
            self.draw_piece(screen, temp_piece, -preview_x, -preview_y)
        
        # Controls
        controls_y = 300
        controls = [
            "Controls:",
            "← → Move",
            "↓ Soft Drop",
            "Space Hard Drop",
            "↑ Rotate",
            "T Toggle Theme",
            "R Restart"
        ]
        
        for i, control in enumerate(controls):
            if i == 0:
                text = self.font_medium.render(control, True, colors['TEXT'])
            else:
                text = self.font_small.render(control, True, colors['TEXT'])
            screen.blit(text, (ui_x, controls_y + i * 25))
    
    def draw_game_over(self, screen):
        colors = self.get_colors()
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(colors['OVERLAY'])
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, colors['TEXT'])
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, colors['TEXT'])
        restart_text = self.font_medium.render("Press R to restart", True, colors['TEXT'])
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                   SCREEN_HEIGHT // 2 - 50))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 
                                     SCREEN_HEIGHT // 2))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 2 + 50))
    
    def restart(self):
        self.__init__()
    
    def draw(self, screen):
        colors = self.get_colors()
        screen.fill(colors['BACKGROUND'])
        self.draw_grid(screen)
        self.draw_placed_pieces(screen)
        
        if not self.game_over:
            self.draw_piece(screen, self.current_piece)
        
        self.draw_ui(screen)
        
        if self.game_over:
            self.draw_game_over(screen)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    
    game = TetrisGame()
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                
                # Theme toggle (works anytime)
                if event.key == pygame.K_t:
                    game.toggle_theme()
                
                if event.key == pygame.K_r:
                    game.restart()
        
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
