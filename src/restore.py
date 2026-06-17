from src.hidpp import get_all_cids, set_divert


def restore(handle, idx):
    for c in get_all_cids(handle, idx):
        set_divert(handle, idx, c, False)
    print("All controls undiverted.")
