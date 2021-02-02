import unittest

from src.spider.QQZoneFriendSpider import QQZoneFriendSpider

class FriendSpiderTest(unittest.TestCase):
    """
    测试获取好友数据（基本信息，不是说说内容）
    """

    def test_init(self):
        QQZoneFriendSpider()

    def test_get_friend_list(self):
        fs = QQZoneFriendSpider(use_redis=False, analysis=False)
        fs.get_friend_list()

    def test_get_friend_detail(self):
        fs = QQZoneFriendSpider(use_redis=False, analysis=False, debug=True)
        fs.get_friend_detail()

    def test_clean_friend_data(self):
        fs = QQZoneFriendSpider(use_redis=False, analysis=True, export_csv=False)
        fs.clean_friend_data()
        print("friend df:", fs.friend_df.shape)

    def test_get_first_friend_info(self):
        fs = QQZoneFriendSpider(use_redis=False, analysis=True)
        fs.get_first_friend_info()
        print(fs.user_info.first_friend, fs.user_info.first_friend_time)

    def test_download_friend_header(self):
        fs = QQZoneFriendSpider(use_redis=True, analysis=True)
        fs.download_head_image()
        print("spend time to wait:", fs.image_thread_pool.time_spend)

if __name__ =='__main__':
    unittest.main()