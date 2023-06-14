# This code will be used generate some statistics about the players and how they perform
from playingPoker import simulate_game

stats = {0: 0, 1: 0, 2: 0}
for i in range(100):
    print(i)
    winner = simulate_game()
    stats[winner] += 1

for j in stats:
    stats[j] = round((stats[j] / 100) * 100, 2)

print(stats)

