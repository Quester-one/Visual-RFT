# import json
# import os
# import requests
# from tqdm import tqdm  # 用于显示进度条，可选
#
# # 输入和输出路径配置
# json_path = '/data/mentianyi/code/Visual-RFT/raw_data/coco_anno/instances_val2017.json'
# output_dir = '/data/mentianyi/code/Visual-RFT/raw_data/coco_anno/val2017_images/'  # 确保目录存在
#
# # 创建输出目录（如果不存在）
# os.makedirs(output_dir, exist_ok=True)
#
# # 读取JSON文件
# with open(json_path, 'r') as f:
#     data = json.load(f)
#
# # 遍历所有图片信息并下载
# for img_info in tqdm(data['images'], desc="Downloading Images"):
#     image_url = img_info['coco_url']
#     file_name = img_info['file_name']  # 直接使用标注中的文件名
#
#     # 构造图片保存路径
#     save_path = os.path.join(output_dir, file_name)
#
#     # 如果文件已存在，跳过下载
#     if os.path.exists(save_path):
#         continue
#
#     try:
#         # 发送HTTP GET请求下载图片
#         response = requests.get(image_url, stream=True)
#         response.raise_for_status()  # 检查请求是否成功
#
#         # 将图片内容写入文件
#         with open(save_path, 'wb') as f:
#             for chunk in response.iter_content(chunk_size=8192):
#                 f.write(chunk)
#     except Exception as e:
#         print(f"Failed to download {image_url}: {e}")
#
# print("所有图片下载完成！")
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed  # 修复导入
from tqdm import tqdm

# 配置参数
JSON_PATH = '/data/mentianyi/code/Visual-RFT/raw_data/coco_anno/instances_val2017.json'
OUTPUT_DIR = '/data/mentianyi/code/Visual-RFT/raw_data/coco_anno/val2017_images/'
THREADS = 8  # 根据网络带宽调整线程数

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 读取JSON文件
with open(JSON_PATH, 'r') as f:
    data = json.load(f)


# 下载单张图片的函数
def download_image(img_info):
    url = img_info['coco_url']
    file_name = img_info['file_name']
    save_path = os.path.join(OUTPUT_DIR, file_name)

    if os.path.exists(save_path):
        return None  # 跳过已存在的文件

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        return f"{url} failed: {str(e)}"


# 多线程下载
with ThreadPoolExecutor(max_workers=THREADS) as executor:
    futures = [executor.submit(download_image, img) for img in data['images']]

    # 修复：直接使用 as_completed（无需前缀）
    errors = []
    for future in tqdm(as_completed(futures), total=len(futures), desc="下载进度"):
        result = future.result()
        if result and "failed" in result:
            errors.append(result)

# 打印错误汇总（同上）
if errors:
    print("\n以下文件下载失败：")
    for error in errors[:10]:
        print(error)
    print(f"总失败数：{len(errors)}")

print("全部任务完成！")