def union_all(paths, to_union):
    union_all_paths = list()
    if len(to_union) == 1:
        return list(paths[to_union[0]])

    for path in to_union:
        union_all_paths = merge_two_lists(union_all_paths, list(paths[path]))

    return list(union_all_paths)


def merge_two_lists(first_list, second_list):
    if not first_list:
        return second_list
    first_list_start = first_list[0]
    first_list_end = first_list[-1]
    second_list_start = second_list[0]
    second_list_end = second_list[-1]
    merge = list()
    if first_list_end == second_list_start:
        second_list.pop(0)
        merge = first_list + second_list

    elif second_list_end == first_list_start:
        first_list.pop(0)
        merge = second_list + first_list

    elif second_list_start == first_list_start:
        second_list.pop(0)
        second_list.reverse()
        merge = second_list + first_list

    elif second_list_end == first_list_end:
        first_list.pop(-1)
        first_list.reverse()
        merge = second_list + first_list

    return merge
