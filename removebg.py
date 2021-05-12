#简单整合难免出错，大佬多指教
import requests

while True:
    chose = input(
        """
        ***************************************
        *          欢迎使用本工具          skye*
        * 工具是调用www.remove.bg的API实现抠图 *
        *    因此自行前往网站注册申请API密钥    *
        *       个人账户每月免费50张           *
        *=====================================*
        *       开始去除背景 请按 1            *
        *       退出工具     请按 0           *
        ***************************************        
        """
    )
    if chose == '1':
        api_key = "zdj7j4ZLkTrKSxc5dn6MAy8c"
        while True:
            chose = input("""
            **********************************
            *      本地图片 请按 1           *
            *      网络图片 请按 2           *
            **********************************
            """)
            if chose == '1':
                print("""
                _______________________________________
                请将处理图片放于本工具同一目录之下！！！
                请将处理图片放于本工具同一目录之下！！！
                请将处理图片放于本工具同一目录之下！！！
                ---------------------------------------
                """)
                image_path = input("请填入本地图片名称：\n")
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_file': open(image_path, 'rb')},
                    data={'size': 'auto'},
                    headers={'X-Api-Key': api_key},
                )
                if response.status_code == requests.codes.ok:
                    with open('no-bg-' + image_path, 'wb') as out:
                        out.write(response.content)
                else:
                    print("Error:" + response.status_code + response.text)
                    with open("removebg_error_logs.txt", 'rt', encoding="utf-8") as logs:
                        logs.write("Error:" + response.status_code + response.text + "\n")
                exit()
            elif chose == '2':
                image_url = input("请填入图片的URL链接：\n")
                response = requests.post(
                    'https://api.remove.bg/v1.0/removebg',
                    files={'image_url': image_url},
                    data={'size': 'auto'},
                    headers={'X-Api-Key': api_key},
                )
                if response.status_code == requests.codes.ok:
                    with open('no-bg-' + image_url, 'wb') as out:
                        out.write(response.content)
                else:
                    print("Error:", response.status_code, response.text)
                    with open("removebg_error_logs.txt", 'rt', encoding="utf-8") as logs:
                        logs.write("Error:" + response.status_code + response.text + "\n")
                exit()
            else:
                print("输入有误请重新输入~~~")
    elif chose == '0':
        print("欢迎下次使用~~~")
        break
    else:
        print("输入有误请重新输入~~~")
