import time

start_time = time.time()
for i in range (0,10000000):
    pass
end_time = time.time()
execution_time_seconds = end_time - start_time
#execution_time_minutes = execution_time_seconds / 60
print(f"代码运行时间: {execution_time_seconds}分钟")