import random
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import argparse

frames = []


def update(stuff):
    frames.append(stuff)


def merge(ary: list, s, midpoint, e):
    ary1: list = ary[s:midpoint]
    ary2: list = ary[midpoint:e]
    index = s
    one_or_two = False
    while len(ary1) > 0 and len(ary2) > 0:
        if ary1[0] > ary2[0]:
            ary[index] = ary2.pop(0)
        else:
            ary[index] = ary1.pop(0)
        index += 1

    while len(ary1) > 0:
        ary[index] = ary1.pop(0)
        index += 1

    while len(ary2) > 0:
        ary[index] = ary2.pop(0)
        index += 1


def merge_sort(ary: list[int], s=0, length=-1):
    if -1 < length < 2:
        return
    elif length == 2:
        if ary[s] > ary[s+1]:
            ary[s], ary[s+1] = ary[s+1], ary[s]
    else:
        if length == -1:
            length = len(ary)
        midpoint = s + (length // 2) + 1
        merge_sort(ary, s, midpoint - s)
        merge_sort(ary, midpoint, length - (midpoint - s))
        merge(ary, s, midpoint, s+length)


def insertion_sort_frame(ary: list):
    for i in range(len(ary)+1):
        for j in range(1, i)[::-1]:
            if ary[j] < ary[j-1]:
                ary[j], ary[j-1] = ary[j-1], ary[j]
                return j-1
            else:
                break
    return 0


def _sorted(ary):
    for i in range(len(ary)-1):
        if ary[i] > ary[i+1]:
            return False
    return True


def main():
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
    merge_sort(counts)
    print(counts)

    while 1:
        pass
    bar_labels = [f'{i}' for i in range(length)]
    bar_colors = ['tab:red' for _ in range(length)]

    chart = ax.bar(indices, counts, color=bar_colors)

    ary_accs = 0
    counts2 = counts

    def animate_insert(_frame_number):
        index: int = insertion_sort_frame(counts)
        ax.cla()
        new_bar_colors = ['tab:red' for _ in range(length)]
        new_bar_colors[index] = 'tab:blue'
        if not _sorted(counts):
            fig.suptitle(f'ary accesses: { _frame_number}', fontsize=14)
            new_chart = ax.bar(indices, counts,
                               label=bar_labels, color=new_bar_colors)
            return new_chart
        else:
            new_chart = ax.bar(indices, counts, label=bar_labels, color=[
                               'tab:blue' for _ in range(length)])
            return new_chart

    anim = animation.FuncAnimation(fig, animate_insert, frames=length**2,
                                   interval=.01)
    writergif = animation.PillowWriter(fps=120)
    writervideo = animation.FFMpegWriter(fps=60)

    anim.save('insertion_sort.gif', writer=writergif)
    plt.close()


if __name__ == '__main__':
    main()
