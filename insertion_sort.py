import random
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    'integer', metavar='int', type=int,
    help='list length')
args = parser.parse_args()
length = args.integer

r = random.Random()
fig, ax = plt.subplots()
indices = [i for i in range(1, length+1)]
counts = [i for i in range(1, length+1)]
for i in range(length*10):
    x = r.randint(1, length-1)
    y = r.randint(1, length-1)
    counts[x], counts[y] = counts[y], counts[x]

bar_labels = [f'{i}' for i in range(length)]
bar_colors = ['tab:red' for _ in range(length)]

chart = ax.bar(indices, counts, color=bar_colors)

# ax.set_ylabel('value in list')
# ax.set_title('sorting algs in python gif ')


def insertion_sort_frame(ary: list):
    for i in range(len(ary)+1):
        for j in range(1, i)[::-1]:
            if ary[j] < ary[j-1]:
                ary[j], ary[j-1] = ary[j-1], ary[j]
                return j-1
            else:
                break
    return 0


ary_accs = 0
counts2 = counts


def _sorted(ary):
    for i in range(len(ary)-1):
        if ary[i] > ary[i+1]:
            return False
    return True


def animate_insert(_frame_number):
    index: int = insertion_sort_frame(counts)
    ax.cla()
    new_bar_colors = ['tab:red' for _ in range(length)]
    new_bar_colors[index] = 'tab:blue'
    if not _sorted(counts):
        fig.suptitle(f'ary accesses: {_frame_number}', fontsize=14)
        new_chart = ax.bar(indices, counts,
                           label=bar_labels, color=new_bar_colors)
        return new_chart
    else:
        new_chart = ax.bar(indices, counts,
                           label=bar_labels, color=['tab:blue' for i in range(length)])
        return new_chart


anim = animation.FuncAnimation(fig, animate_insert, frames=length**2,
                               interval=.01)

# saving to m4 using ffmpeg writer
writergif = animation.PillowWriter(fps=120)
writervideo = animation.FFMpegWriter(fps=60)

anim.save('insertion_sort.gif', writer=writergif)
# print(anim.to_html5_video(embed_limit=10000).strip(),
#       file=open("video.html", 'w'))
plt.close()
