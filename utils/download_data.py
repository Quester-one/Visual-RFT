import os
import sys
import argparse

sys.path.append('/home/mentianyi/code/AgentRewardBench')
from config_private import http_proxy, https_proxy

os.environ["http_proxy"] = http_proxy
os.environ["https_proxy"] = https_proxy
from huggingface_hub import snapshot_download
from time import sleep


def download_coco():
    while True:
        try:
            snapshot_download(repo_id='laolao77/ViRFT_COCO_base65',
                              repo_type="dataset",
                              local_dir='../raw_data/raw_coco',
                              resume_download=True)
        except Exception as e:
            print(e)
            sleep(10)


def do_download_qwen2vl2():
    while True:
        try:
            snapshot_download(repo_id='Qwen/Qwen2-VL-2B-Instruct',
                              repo_type="model",
                              local_dir='/home/mentianyi/my_huggingface/Qwen2-VL-2B-Instruct/',
                              resume_download=True)
        except Exception as e:
            print(e)
            sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--do_download_coco', action='store_true', default=True)
    parser.add_argument('--do_download_qwen2vl2', action='store_true', default=True)
    args = parser.parse_args()

    if args.do_download_coco:
        download_coco()
    if args.do_download_qwen2vl2:
        do_download_qwen2vl2()
