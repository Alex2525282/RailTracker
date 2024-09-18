import pandas as pd

# 读取数据
results_df = pd.read_csv('第二问结果.csv', encoding='gbk')
railway_df = pd.read_csv('五十城市铁路数据.csv', encoding='utf-8')
attractions_df = pd.read_csv('五十城景点数据.csv', encoding='gbk')

# 数据预处理
attractions_df.rename(columns={'Unnamed: 0': '城市'}, inplace=True)
cities = attractions_df['城市'].tolist()

# 创建高铁线路字典
railway_dict = {}
for _, row in railway_df.iterrows():
    from_city, to_city = row['出发城市'], row['到达城市']
    if from_city not in railway_dict:
        railway_dict[from_city] = {}
    railway_dict[from_city][to_city] = {
        '最低票价': row['最低票价'],
        '路程时间（小时）': row['对应持续时间']
    }


# Recursively search all possible routes and calculate total cost for each
max_time = 144
all_routes_with_cost = []
max_cities = 0
max_routes_to_find = 101000
routes_count = 0

def search_route_with_cost(current_city, current_time, visited_cities, current_cost):
    global all_routes_with_cost, max_cities, routes_count
    
    if current_time > max_time or routes_count >= max_routes_to_find:
        routes_count += 1
        return
    
    if len(visited_cities) > max_cities:
        all_routes_with_cost = []
        max_cities = len(visited_cities)
        all_routes_with_cost = [(visited_cities[:], current_cost)]
        print('当前城市数量：', max_cities)
        print('预览总分数（调试输出）：', current_cost)
    elif len(visited_cities) == max_cities:
        all_routes_with_cost.append((visited_cities[:], current_cost))
        routes_count += 1
    #print(f"路径 {all_routes_with_cost} = [(visited_cities[:], current_cost)], 总时间：{current_time}")
    for next_city in cities:
        if next_city not in visited_cities:
            if next_city in railway_dict.get(current_city, {}):
                travel_time = railway_dict[current_city][next_city]['路程时间（小时）']
                next_time = current_time + travel_time + attractions_df[attractions_df['城市'] == next_city]['建议游玩时长'].values[0]
                
                visited_cities.append(next_city)
                next_city_cost = results_df[results_df['索引'] == next_city]['综合得分指数'].values[0]
                next_cost = current_cost + next_city_cost
                search_route_with_cost(next_city, next_time, visited_cities, next_cost)
                visited_cities.pop()

# Starting the search from '广州' as specified
start_city='广州'
initial_time = attractions_df[attractions_df['城市'] == start_city]['建议游玩时长'].values[0]
initial_cost = results_df[results_df['索引'] == start_city]['综合得分指数'].values[0]
search_route_with_cost(start_city, initial_time, [start_city], initial_cost)

# Sorting routes by total cost
all_routes_with_cost.sort(key=lambda x: x[1])

# Extracting routes and costs for output
sorted_routes = [route for route, cost in all_routes_with_cost]
sorted_costs = [cost for route, cost in all_routes_with_cost]

# Outputting the results
max_cities_count = len(sorted_routes[0])
print(f"最多访问城市数量: {max_cities_count}")
print("所有符合条件的路径和总分数:")
for i, route in enumerate(sorted_routes):
    total_cost = sorted_costs[i]
    print(f"路径 {i+1}: {' -> '.join(route)}, 总得分: {total_cost} ")
