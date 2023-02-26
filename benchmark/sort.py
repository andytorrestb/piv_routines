import pandas as pd
import math
def nearestNeighbors(data1, data2):
    print(data1.shape, data2.shape)

    data2_sorted = pd.DataFrame(columns = data2.columns)
    print(data2_sorted)


    for index1, row1 in enumerate(data1.iterrows()):
        print(index1)
        # print(data1.iloc[[index]],'\n' ,data2.iloc[[index]])

        row1 = data1.iloc[[index1]]
        # row = row.iloc[[0]]
        # print('==========')
        # print('row\n', row)
        # print('==========')
        # print(type(row))

        # x = row['x']
        # x = float(row.to_list()[0])
        x1 = row1['x'].max()
        y1 = row1['y'].max()

        min_dis = 10000000.0

        for index2, row2 in enumerate(data2.iterrows()):
            row2 = data2.iloc[[index2]]
            x2 = row2['x'].max()
            y2 = row2['y'].max()

            dx = x2 - x1
            dy = y2 - y1

            distance = math.sqrt(dx**2 + dy**2)

            if distance < min_dis:
                min_dis = distance
                min_dis_index = index2
                # print(index1, index2, distance)
                
        data2_sorted = data2_sorted.append(data2.iloc[[min_dis_index]])
        data2.drop(axis = 0, index = min_dis_index)
        # print(data2_sorted)
                # input()
    print(data2_sorted.shape)
    input()
    return data2_sorted
        # print(x,y)
        # print(type(x))

    # for index1, series1, index2, series2 in data1.iterrows(), data2.iterrows():
    #     print(index, series)