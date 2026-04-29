import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change Colors
content = content.replace('--neon-green: #00ff88;', '--neon-primary: #00e5ff; --neon-green: #00e5ff;')
content = content.replace('--neon-yellow: #ffcc00;', '--neon-secondary: #ff0055; --neon-yellow: #ff0055;')
content = content.replace('--border-color: rgba(0, 255, 136, 0.3);', '--border-color: rgba(0, 229, 255, 0.3);')
content = content.replace('rgba(0, 255, 136', 'rgba(0, 229, 255')
content = content.replace('borderColor: \'#00ff88\'', 'borderColor: \'#00e5ff\'')
content = content.replace('0x00ff88, 0xffcc00, 0xff4444', '0x00e5ff, 0xff0055, 0xffaa00')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

