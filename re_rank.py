import os
import time

from .models import Link

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "steelrumours.settings")


def rank_all():
    for link in Link.with_votes.all():
        link.set_rank()


def show_all():
    print("\n".join("%10s %0.2f" % (link.title, link.rank_score)
                    for link in Link.with_votes.all()))
    print("----\n\n\n")


if __name__ == "__main__":
    while 1:
        print("---")
        rank_all()
        show_all()
        time.sleep(5)
