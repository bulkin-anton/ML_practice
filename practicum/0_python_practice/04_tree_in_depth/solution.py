def find_path_sums(tree):
    stack = [(0, tree)]
    while (stack):
        cur_sum, cur_node = stack.pop()
        if (cur_node is None):
            return
        else:
            cur_sum += cur_node[0]
            if not (cur_node[2] is None):
                stack.append((cur_sum, cur_node[2]))
            if not (cur_node[1] is None):
                stack.append((cur_sum, cur_node[1]))
            else:
                if (cur_node[2] is None):
                    print(cur_sum)
