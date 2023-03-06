
import time
import shutil

start = time.time()

filenames = [
    [
		"./output/10_left.jpeg",
		"./output/1444_left.jpeg",
		"./output/16_right_ly4JThy.jpeg",
		"./output/79_left.jpeg",
		"./output/1177_right.jpeg",
		"./output/1509_right.jpeg",
		"./output/30_left.jpeg",
		"./output/129_right.jpeg",
		"./output/16_right.jpeg",
		"./output/367_right.jpeg"
	],
	[
		"10_left.jpeg",
		"1444_left.jpeg",
		"16_right_ly4JThy.jpeg",
		"79_left.jpeg",
		"1177_right.jpeg",
		"1509_right.jpeg",
		"30_left.jpeg",
		"129_right.jpeg",
		"16_right.jpeg",
		"367_right.jpeg"
	]
]

for i in range(10):
    shutil.copy(filenames[0][i], filenames[1][i])

end = time.time()

print(f"{end-start} seconds")