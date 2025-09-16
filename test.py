import os
import shutil

# 所有原始文件夹的前缀数字范围
start_num = 1
end_num = 68

# 分组大小
group_size = 5

# 当前工作目录（可以根据需要修改）
base_dir = f"E:\\青楼风月1-86"  # 当前目录

# 获取所有原始文件夹名列表
folders = [f"{i:02d}" for i in range(start_num, end_num + 1)]

# 分组处理
for i in range(0, len(folders), group_size):
    group = folders[i:i+group_size]
    
    # 构造目标文件夹名
    start_group = group[0]
    end_group = group[-1]
    target_folder_name = f"{start_group}-{end_group}"
    target_path = os.path.join(base_dir, target_folder_name)
    
    # 创建目标文件夹
    os.makedirs(target_path, exist_ok=True)
    
    # 遍历每个源文件夹
    for folder in group:
        src_path = os.path.join(base_dir, folder)
        
        if not os.path.exists(src_path):
            print(f"警告：{src_path} 不存在")
            continue
        
        # 遍历源文件夹内的所有内容（包括文件和子文件夹）
        try:
            for item in os.listdir(src_path):
                item_path = os.path.join(src_path, item)
                dest_item_path = os.path.join(target_path, item)
                
                # 如果目标路径已存在同名文件或文件夹，先删除或跳过
                if os.path.exists(dest_item_path):
                    print(f"警告：{dest_item_path} 已存在，正在跳过...")
                    continue
                
                # 移动文件或文件夹
                shutil.move(item_path, dest_item_path)
            
            # 尝试删除源文件夹，但仅在其为空时
            if not os.listdir(src_path):  # 检查文件夹是否为空
                os.rmdir(src_path)  # 删除空文件夹
                print(f"已删除空文件夹: {src_path}")
            else:
                print(f"注意：{src_path} 不是空的，未删除。")
        except Exception as e:
            print(f"处理 {src_path} 出错：{e}")