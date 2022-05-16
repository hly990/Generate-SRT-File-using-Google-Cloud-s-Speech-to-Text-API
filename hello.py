#To print hello world in python:
# print("Hello World")


dict_origin_list = []
dict_tmp_list = []
dict_target_list = []

empty_string = ''

flag = 1

#读到dict_origin_list
with open("subtitles.srt", "r") as txt_file:
	lines = txt_file.read().splitlines()
	dict1 = {}
	flag = 1

	for line in lines:

	
		if flag == 1:

			key = "id"
			value = line
			dict1[key] = value

		elif flag == 2:

			key = "timeline"
			value = line
			dict1[key] = value

		elif flag == 3:

			key = "content"
			value = line
			dict1[key] = value	
		
		elif flag == 4:

			flag = 1
			dict_origin_list.append(dict1)
			dict1 = {}

			continue
	

		flag+=1
		# print(line)
        	
	# print(dict_origin_list)

#进行转换
flag = 1

for dict_origin in dict_origin_list:

	dict2= {}

	timeline = dict_origin["timeline"]

	timeline_split = timeline.split(" --> ")

	# 处理begintime
	if flag == 1:
		begin_time_list = timeline_split[0].split(",")
		part1 = begin_time_list[0]
		part2 = begin_time_list[1]
		
		part1_int = int(part1[-2:])
		part2_int = int(part2)

		begin_time_float = float(str(part1_int)+'.'+str(part2_int))

	else:
		begin_time_float = tmp_time_float

	# 处理endtime
	end_time_list = timeline_split[1].split(",")
	part1 = end_time_list[0]
	part2 = end_time_list[1]

	part1_int = int(part1[-2:])
	part2_int = int(part2)

	end_time_float = float(str(part1_int)+'.'+str(part2_int))

	#分析content长度
	content = dict_origin["content"]
	if len(content) > 10 and len(content) < 15:
		end_time_float = begin_time_float + 3

	elif len(content) >= 15 and len(content) < 25:
		end_time_float = begin_time_float + 3.8

	elif len(content) >= 25 and len(content) < 30:
		end_time_float = begin_time_float + 4.3

	elif len(content) >= 30:
		end_time_float = begin_time_float + 4.6

	else:
		end_time_float = begin_time_float + 2

	#保存end_time_float替换下一个begin_time_float
	tmp_time_float = end_time_float

	#dict构造begintimeline,endtimeline
	dict2["begin_time"] = begin_time_float
	dict2["end_time"] = end_time_float

	dict_tmp_list.append(dict2)

	dict2 = {}

	#追加begin_time,end_time到origin list
	dict_origin["begin_time"] = round(begin_time_float,1)
	dict_origin["end_time"] = round(end_time_float,1)

	# print(begin_time_float)

	flag +=1

# print(dict_origin_list)

#把修改后的数据写到新的srt文件中
target_subtitles = open("target_subtitles.srt", "w") 
 
# target_subtitles.write("hello,world!") 
#遍历dict_origin_list
for dict_origin in dict_origin_list:

	# target_subtitles.write(dict_origin["id"]+"\n")
	# target_subtitles.write(dict_origin["timeline"]+"\n") 
	# target_subtitles.write(dict_origin["content"]+"\n") 
	# target_subtitles.write("\n") 

	#处理begin_time,end_time
	begin_time = dict_origin["begin_time"]
	end_time = dict_origin["end_time"]

	begin_time_split = str(begin_time).split(".")
	begin_time_part1 = begin_time_split[0]
	begin_time_part2 = begin_time_split[1]

	if int(begin_time_part1) < 10:
		begin_time_part1 = "0" + str(begin_time_part1)

	begin_time_part2 = str(begin_time_part2) + "00"

	end_time_split = str(end_time).split(".")
	end_time_part1 = end_time_split[0]
	end_time_part2 = end_time_split[1]

	if int(end_time_part1) < 10:
		end_time_part1 = "0" + str(end_time_part1)

	end_time_part2 = str(end_time_part2) + "00"

	#拼接字符串

	tmp_timeline = dict_origin["timeline"].split(" --> ")
	tmp_timeline_part1 = tmp_timeline[0]
	tmp_timeline_part2 = tmp_timeline[1]

	tmp_timeline_part1 = tmp_timeline_part1[0:6]
	tmp_timeline_part2 = tmp_timeline_part2[0:6]

	tmp_timeline_part1 = tmp_timeline_part1 + begin_time_part1 + "," + begin_time_part2
	tmp_timeline_part2 = tmp_timeline_part2 + end_time_part1 + "," + end_time_part2
	
	dict_origin["timeline"] = tmp_timeline_part1 + " --> " + tmp_timeline_part2


	# print(dict_origin["timeline"])
	# print(end_time_part1,end_time_part2)

	#输出到新的srt文件
	target_subtitles.write(dict_origin["id"]+"\n")
	target_subtitles.write(dict_origin["timeline"]+"\n") 
	target_subtitles.write(dict_origin["content"]+"\n") 
	target_subtitles.write("\n") 

 
target_subtitles.close() 












