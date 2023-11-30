def is_valid(coord_points):
    for coord in coord_points:
        if len(coord_points[coord]) > 1:
            return False
    return True
def delete_old_point(x, y, ac_to_shunt):
    coord_points[str(x) + "_" + str(y)].remove(ac_to_shunt)
    x_coords_points[x].remove(ac_to_shunt)
    y_coords_points[y].remove(ac_to_shunt)
    return
def update_new_point(x, y, ac_to_shunt):
    point_position[ac_to_shunt] = {"x_bin": x, "y_bin": y}
    if str(x) + "_" + str(y) not in coord_points:
        coord_points[str(x) + "_" + str(y)] = []
    coord_points[str(x) + "_" + str(y)].append(ac_to_shunt)
    if x not in x_coords_points:
        x_coords_points[x] = []
    x_coords_points[x].append(ac_to_shunt)

    if y not in y_coords_points:
        y_coords_points[y] = []
    y_coords_points[y].append(ac_to_shunt)
    return
def shunt_point(coord):
    x, y = coord.split('_')
    ac_to_shunt = coord_points[coord][1]
    x = int(x)
    y = int(y)

    #check if a neighbouring bin is empty and move to neighbouring bin
    for point in [(min(x+1, num_x_grid), y), (min(x+1, num_x_grid), min(y+1, num_y_grid)), (min(x+1, num_x_grid), max(0, y-1)),
                  (max(0, x-1), y), (max(0, x-1), min(y+1, num_y_grid)), (max(0, x-1), max(0, y-1)),
                  (x, min(y+1, num_y_grid)), (x, max(0, y-1))]:
        if len(coord_points.get(str(point[0]) + "_" + str(point[1]), [])) == 0:
            #delete old point
            delete_old_point(x, y, ac_to_shunt)

            #add new point
            update_new_point(point[0], point[1], ac_to_shunt)
            return

    #move to a neighbouring bin in the direction that is most sparse
    prop_x_plus_empty = 1.*len([i for i in range(x+1, 51) if len(coord_points.get(str(i) + "_%d"%y, [])) == 0])/(num_x_grid-x) if x != num_x_grid else 0
    prop_x_minus_empty = 1.*len([i for i in range(x-1, -1, -1) if len(coord_points.get(str(i) + "_%d"%y, [])) == 0])/(x) if x != 0 else 0

    prop_y_plus_empty = 1.*len([i for i in range(y+1, 41) if len(coord_points.get("%d_"%x + str(i), [])) == 0])/(num_y_grid-y) if y != num_y_grid else 0
    prop_y_minus_empty = 1.*len([i for i in range(y-1, -1, -1) if len(coord_points.get("%d_"%x + str(i), [])) == 0])/(y) if y != 0 else 0

    delete_old_point(x, y, ac_to_shunt)
    if prop_x_plus_empty is max(prop_x_plus_empty, prop_x_minus_empty, prop_y_plus_empty, prop_y_minus_empty):
        for idx in range(x+1, 51)[::-1]:
            if str(idx) + "_" + str(y) in coord_points:
                for ac in coord_points[str(idx) + "_" + str(y)]:
                    delete_old_point(idx, y, ac)
                    update_new_point(min(idx+1, num_x_grid), y, ac)

        update_new_point(min(x+1, num_x_grid), y, ac_to_shunt)
        return
    if prop_x_minus_empty is max(prop_x_plus_empty, prop_x_minus_empty, prop_y_plus_empty, prop_y_minus_empty):
        for idx in range(x-1, -1, -1)[::-1]:
            if str(idx) + "_" + str(y) in coord_points:
                for ac in coord_points[str(idx) + "_" + str(y)]:
                    delete_old_point(idx, y, ac)
                    update_new_point(max(idx-1, 0), y, ac)

        update_new_point(max(x-1, 0), y, ac_to_shunt)
        return
    if prop_y_plus_empty is max(prop_x_plus_empty, prop_x_minus_empty, prop_y_plus_empty, prop_y_minus_empty):
        for idx in range(y+1, 41)[::-1]:
            if str(x) + "_" + str(idx) in coord_points:
                for ac in coord_points[str(x) + "_" + str(idx)]:
                    delete_old_point(x, idx, ac)
                    update_new_point(x, min(idx+1, num_y_grid), ac)

        update_new_point(x, min(y+1, num_y_grid), ac_to_shunt)
        return
    if prop_y_minus_empty is max(prop_x_plus_empty, prop_x_minus_empty, prop_y_plus_empty, prop_y_minus_empty):
        for idx in range(y-1, -1, -1)[::-1]:
            if str(x) + "_" + str(idx) in coord_points:
                for ac in coord_points[str(x) + "_" + str(idx)]:
                    delete_old_point(x, idx, ac)
                    update_new_point(x, max(idx-1, 0), ac)

        update_new_point(x, max(y-1, 0), ac_to_shunt)
        return
