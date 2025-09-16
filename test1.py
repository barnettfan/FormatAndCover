import os

base_dir = f"Z:\\BaiduNetdiskDownload\\小叶兽交日记\\小叶兽交日记22\\"  # 当前目录

# for item in os.listdir(base_dir):
#     if len(item) == 2:
#         continue
# item = '番外2临别前夜'
# for childrenItem in os.listdir(os.path.join(base_dir, item)):
#     list = os.listdir(os.path.join(base_dir, item,childrenItem))
#     for filename in list:
#         if '.jpg' not in filename:
#             continue
#         oldfilename = os.path.join(base_dir, item,childrenItem,filename)
#         newfilename = os.path.join(base_dir, item,childrenItem + '_' +filename)
#         os.rename(oldfilename, newfilename)

list = os.listdir(base_dir) 
for item in list:
    oldfilename = os.path.join(base_dir, item)
    newfilename = oldfilename.replace('txt', 'webp')
    os.rename(oldfilename, newfilename)


