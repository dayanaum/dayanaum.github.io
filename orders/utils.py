def get_format(list_tuple):
    order_list = []
    for j in list_tuple:
        order_list.append((j[1].order_id, j[1].total_quantity, j[1].total_price))
    order_list = list(set(order_list))
    mylist = list()
    for x in range(0, len(order_list)):
        order_dict = dict()
        new_list = []
        bo_id = order_list[x][0]
        for i in list_tuple:
            if int(bo_id) == int(i[0].order_id):
                a = {
                    "book_id": i[2].book_id,
                    "quantity": i[0].quantity,
                    "book_name": i[2].book_name,
                }
                new_list.append(a)
        order_dict.update({
            "order_id": bo_id,
            "total_quantity": order_list[x][1],
            "total_price": order_list[x][2],
            "order_items": new_list
        })
        mylist.append(order_dict)
    return mylist
