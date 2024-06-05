from ursina import *


# Initialize the Ursina app
app = Ursina()

# Create the player entity with a collider
me = Animation('player', collider='box', y=5, x=-14)

# Set up the camera and sky
Sky()
camera.orthographic = True
camera.fov = 20

# Explosion animation setup
boom = Animation('boom', model='cube', texture='boom1.png', scale=3, x=25, y=25)

# Background setup
Entity(model='quad', texture='BG.png', scale=36, z=1)

# Fly (enemy) setup
fly = Entity(model='cube', texture='fly.png', collider='box', scale=3, x=20, y=-10)

# List to keep track of all fly entities
flies = []

# Function to create a new fly at regular intervals
def newFly():
    new = duplicate(fly, y=-5 + (10124 * time.dt) % 15)
    flies.append(new)
    invoke(newFly, delay=1)  # Schedule the next fly creation

newFly()  # Initial call to start creating flies

# Update function is called every frame
def update():
    # Player movement
    me.y += held_keys['w'] * 6 * time.dt    
    me.y -= held_keys['s'] * 6 * time.dt    
    
    # Adjust player rotation based on movement
    a = held_keys['w'] * -20   
    b = held_keys['s'] * 20  
    
    if a != 0:
        me.rotation_z = a
    else:
        me.rotation_z = b
    
    # Move flies and check for collisions
    for fly in flies:
        fly.x -= 4 * time.dt  # Move fly to the left
        touch = fly.intersects()
        if touch.hit:
            boom.x = fly.x - 2
            boom.y = fly.y
            flies.remove(fly)  # Remove fly from the list
            destroy(fly)  # Destroy fly entity
        elif held_keys['w'] or held_keys['s']:
            boom.x = 25
            boom.y = 35 
        
        # Check for collision between player and flies
        t = me.intersects()
        if t.hit and t.entity.scale == 2:
            invoke(destroy, me)
            quit()

# Handle input for shooting and quitting the game
def input(key):
    if key == 'q':
        quit()
        
    if key == 'enter':
        # Create a bullet entity when the player presses enter
        e = Entity(y=me.y, x=me.x + 2, model='cube', texture='Bullet.png', collider='cube')
        
        # Animate the bullet moving to the right
        e.animate_x(30, duration=2, curve=curve.linear)
        
        # Destroy the bullet after 1 second
        invoke(destroy, e, delay=1)

# Run the Ursina app
app.run()
