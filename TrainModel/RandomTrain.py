from learn import RLagent

# for i in range(6):
# 	savepath = 'data' + str(i+1)
# 	tr = RLagent(50, 0.6, hiddenSize=1000, perfix='Random')
# 	tr.epsilon = 0.3
# 	tr.epsilon_end = 0.05
# 	tr.epsilon_decay = 200
# 	tr.memory_size = 1
# 	tr.batch_size = 1
# 	tr.update_step = 1
# 	tr.max_epoch = 500
# 	tr.train(savePath=savepath)

alpha = 0.8

tr = RLagent(30, alpha, hiddenSize=60, perfix='Random')
tr.epsilon = 0.3
tr.epsilon_end = 0.05
tr.epsilon_decay = 200
tr.train()

# print(tr.dqn.count_parameters())
# print(tr.dqn.get_n_params())



# f = open('test.txt', 'w') # 若是'wb'就表示写二进制文件
# avgRwd = 0.999
# q = 0.3
# f.write(str(avgRwd) + ' ' + str(q) + '\n')
# f.write(str(avgRwd) + ' ' + str(q) + '\n')
# f.close()