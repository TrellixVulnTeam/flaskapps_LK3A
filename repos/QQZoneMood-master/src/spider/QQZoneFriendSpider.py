from src.spider.QQZoneSpider import QQZoneSpider
from urllib import parse
import json
import pandas as pd
from src.util import util
import math
import threading
import datetime
from src.util.constant import FINISH_FRIEND_INFO_ALL, STOP_FRIEND_INFO_SPIDER_KEY, WEB_SPIDER_INFO, \
    FRIEND_INFO_PRE, FRIEND_INFO_COUNT_KEY, EXPIRE_TIME_IN_SECONDS, FRIEND_LIST_KEY, STOP_SPIDER_KEY, STOP_SPIDER_FLAG, \
    FRIEND_NUM_KEY
from src.util.util import remove_special_tag


class QQZoneFriendSpider(QQZoneSpider):
    """
    爬取自己的好友的数量、共同群组等基本信息（不是爬好友的动态）
    """
    def __init__(self, use_redis=False, debug=False, analysis=True, recover=False,
                 username='', mood_begin=0, mood_num=-1, stop_time='-1', from_web=False, nickname='', no_delete=True, cookie_text='',
                 export_excel=False, export_csv = True, pool_flag='127.0.0.1',
                 download_small_image=False, download_big_image=False,
                 download_mood_detail=True, download_like_detail=True, download_like_names=True):
        """
        :param use_redis: 是否使用redis
        :param debug: 是否开启debug模式
        :param analysis: 如果为true, 会执行爬虫程序，再执行分析程序，如果为false，只执行分析程序
        """
        QQZoneSpider.__init__(self, use_redis, debug, recover=recover, username=username, mood_num=mood_num,
                              mood_begin=mood_begin, stop_time=stop_time, from_web=from_web, nickname=nickname,
                              no_delete=no_delete, cookie_text=cookie_text, pool_flag=pool_flag,                               download_small_image=download_small_image, download_big_image=download_big_image,
                              download_mood_detail=download_mood_detail, download_like_detail=download_like_detail,
                              download_like_names=download_like_names)

        if self.g_tk == 0 and analysis == False:
            self.login()
        self.friend_detail = []
        self.friend_list = []
        self.friend_df = pd.DataFrame()
        self.re = self.connect_redis()
        self.friend_thread_list = []
        self.export_excel = export_excel
        self.export_csv = export_csv
        self.error_friend_num = 0

    def get_friend_list(self):
        """
        获取好友列表信息
        :return:
        """
        friend_list_url = self.get_friend_list_url()
        friend_content = self.get_json(self.req.get(url=friend_list_url, headers=self.headers, timeout=20).content.decode('utf-8'))
        self.friend_list = json.loads(friend_content)['data']['items']
        if self.use_redis:
            self.re.set(FRIEND_LIST_KEY + self.username, json.dumps(self.friend_list, ensure_ascii=False))
            if not self.no_delete:
                self.re.expire(FRIEND_LIST_KEY + self.username, EXPIRE_TIME_IN_SECONDS)
        self.save_data_to_json(self.friend_list, self.FRIEND_LIST_FILE_NAME)
        print('获取好友列表信息完成')
        return len(self.friend_list)

    def download_head_image(self):
        """
        下载好友头像
        不需要cookie验证
        :return:
        """
        if len(self.friend_list) == 0:
            self.load_friend_data()
        friend_num = len(self.friend_list)
        thread_num = self.calculate_thread_num(friend_num)
        print("下载头像的线程数量：", thread_num)
        begin_time = datetime.datetime.now()
        thread_list = []
        for i in range(thread_num):
            t = threading.Thread(target=self.do_download_image, args=(i, friend_num, thread_num))
            thread_list.append(t)
        for t in thread_list:
            t.setDaemon(False)
            t.start()
        for t in thread_list:
            t.join()
        print('耗时:', (datetime.datetime.now() - begin_time).seconds, '秒')
        print("下载全部头像完成")

    def do_download_image(self, index, friend_num, step = 1):
        while index < friend_num:
            item = self.friend_list[index]
            url = item['img']
            if self.debug:
                print(url)
            name = item['uin']
            self.download_image(url, self.FRIEND_HEADER_IMAGE_PATH + str(name))
            index += step

    def get_friend_detail(self):
        """
        根据好友列表获取好友详情
        :return:
        """
        try:
            friend_num = self.get_friend_list()
            if self.use_redis:
                self.re.set(FRIEND_NUM_KEY + self.username, friend_num)
                if not self.no_delete:
                    self.re.expire(FRIEND_NUM_KEY + self.username, EXPIRE_TIME_IN_SECONDS)
            if self.use_redis:
                self.re.rpush(WEB_SPIDER_INFO + self.username, FRIEND_INFO_PRE + ":" + str(friend_num))
                if not self.no_delete:
                    self.re.expire(WEB_SPIDER_INFO + self.username, EXPIRE_TIME_IN_SECONDS)
            self.user_info.friend_num = friend_num
            thread_num = self.calculate_thread_num(friend_num)
            self.logging_info("获取好友基本信息的线程数量：" + str(thread_num))
            self.logging_info("开始获取好友数据...")
            for i in range(thread_num):
                begin_index = i
                t = threading.Thread(target=self.do_get_friend_detail, args=(begin_index, friend_num, thread_num, True))
                self.friend_thread_list.append(t)
            for t in self.friend_thread_list:
                t.setDaemon(False)
                t.start()

            # 等待全部子线程结束
            for t in self.friend_thread_list:
                t.join()

        except BaseException as e:
            self.format_error(e, "Faled to get friend info")

        if self.use_redis:
            self.re.set(STOP_FRIEND_INFO_SPIDER_KEY + self.username, FINISH_FRIEND_INFO_ALL)
            self.re.set(self.FRIEND_DETAIL_FILE_NAME, json.dumps(self.friend_detail, ensure_ascii=False))
            if not self.no_delete:
                self.re.expire(STOP_FRIEND_INFO_SPIDER_KEY + self.username, EXPIRE_TIME_IN_SECONDS)
                self.re.expire(self.FRIEND_DETAIL_FILE_NAME, EXPIRE_TIME_IN_SECONDS)
        else:
            self.save_data_to_json(self.friend_detail, self.FRIEND_DETAIL_FILE_NAME)
        print("获取好友数据成功，文件路径为：", self.FRIEND_DETAIL_FILE_NAME)

    # 保证每个线程至少爬20次，最多开self.thread_num个线程
    def calculate_thread_num(self, num):
        if num >= 20 * self.thread_num:
            thread_num = self.thread_num
        else:
            thread_num = math.ceil(num / 20)
        return thread_num

    def do_get_friend_detail(self, index, friend_num, step=1, until_stop_time=True):
        # 避免好友数量为0
        if step < 1:
            step = 1
        while index < friend_num and until_stop_time:
            friend = self.friend_list[index]
            uin = friend['uin']
            if self.debug:
                print('正在爬取好友:', uin, '数据...,', 'index=', index)
            url = self.get_friend_detail_url(uin)
            content = self.get_json(self.req.get(url, headers=self.headers, timeout=20).content.decode('utf-8'))

            try:
                data = json.loads(content)
                data = data['data']
                data['friendUin'] = uin
            except BaseException as e:
                print("Failed to get friend detail for:{}".format(friend))
                self.format_error(e, friend)
                if self.debug:
                    print(data)
                self.error_friend_num += 1
                continue
            finally:
                index += step
            self.friend_detail.append(data)

            if self.use_redis:
                # 这里保存的是friend detail的长度，在多线程的情况下，只有friend detail才能表示所有的数据
                self.re.set(FRIEND_INFO_COUNT_KEY + self.username, len(self.friend_detail) + self.error_friend_num)
                if not self.no_delete:
                    self.re.expire(FRIEND_INFO_COUNT_KEY + self.username, EXPIRE_TIME_IN_SECONDS)
                until_stop_time = False if self.re.get(STOP_SPIDER_KEY + str(self.username)) == STOP_SPIDER_FLAG else True

    def get_friend_list_url(self):
        friend_url = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?'
        params = {
            'uin': self.username,
            'follow_flag': 0,
            'groupface_flag': 0,
            'fupdate': 1,
            'g_tk': self.g_tk,
            'qzonetoken': ''
        }
        friend_url = friend_url + parse.urlencode(params)
        return friend_url

    def get_friend_detail_url(self, uin):
        detail_url = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/friendship/cgi_friendship?'
        params = {
            'activeuin': self.username,
            'passiveuin': uin,
            'situation': 1,
            'isCalendar': 1,
            'g_tk': self.g_tk
        }
        return detail_url + parse.urlencode(params)

    def load_friend_data(self):
        try:
            if self.use_redis:
                self.friend_detail = self.re.get(self.FRIEND_DETAIL_FILE_NAME)
                self.friend_list = self.re.get(self.FRIEND_LIST_FILE_NAME)
                if self.friend_detail is None or self.friend_list is None:
                    raise BaseException
            else:
                raise BaseException
        except BaseException as e:
            if self.use_redis:
                self.format_error(e, "Failed to load data from redis")
                print("try to load data from json now")
            try:
                self.friend_detail = self.load_data_from_json(self.FRIEND_DETAIL_FILE_NAME)
                self.friend_list = self.load_data_from_json(self.FRIEND_LIST_FILE_NAME)

                if self.friend_detail is None or self.friend_list is None:
                    raise FileNotFoundError
                print("Success to load data from json")
            except FileNotFoundError as e:
                self.format_error(e, "Failed to load data from json...")
                print("now, try to start spider to get friend info...")
                self.friend_list = []
                self.friend_detail = []
                self.login()
                self.get_friend_detail()

    def clean_friend_data(self):
        """
        清洗好友数据，生成csv
        :return:
        """
        try:
            if len(self.friend_list) == 0:
                self.load_friend_data()
            friend_total_num = len(self.friend_list)
            print("valid friend num:", friend_total_num)
            friend_list_df = pd.DataFrame(self.friend_list)
            self.friend_detail_list = []
            if friend_total_num == 0:
                print("该用户没有好友")
                return False
            for friend in self.friend_detail:
                try:
                    friend_uin = friend['friendUin']
                    add_friend_time = friend['addFriendTime']
                    img = friend_list_df.loc[friend_list_df['uin'] == friend_uin, 'img'].values[0]
                    nick = friend['nick']
                    nick_name = remove_special_tag(nick[str(friend_uin)])

                    common_friend_num = len(friend['common']['friend'])
                    common_group_num = len(friend['common']['group'])
                    common_group_names = friend['common']['group']
                    self.friend_detail_list.append(
                        dict(uin=self.username, friend_uin=friend_uin, add_friend_time=add_friend_time,
                             nick_name=nick_name, common_friend_num=common_friend_num,
                             common_group_num=common_group_num, common_group_names=common_group_names, img=img))

                except BaseException as e:
                    if self.debug:
                        print("单向好友:", friend)
                    self.friend_detail_list.append(
                        dict(uin=0, friend_uin=friend['friendUin'], add_friend_time=0,
                             nick_name='单向好友', common_friend_num=0,
                             common_group_num=0, common_group_names='', img=''))

            friend_df = pd.DataFrame(self.friend_detail_list)
            friend_df.sort_values(by='add_friend_time', inplace=True)
            friend_df['add_friend_time2'] = friend_df['add_friend_time'].apply(lambda x: util.get_full_time_from_mktime(x))
            friend_df.fillna('', inplace=True)

            if self.export_excel:
                friend_df.to_excel(self.FRIEND_DETAIL_EXCEL_FILE_NAME)
            if self.export_csv:
                friend_df.to_csv(self.FRIEND_DETAIL_LIST_FILE_NAME)
            if self.debug:
                print("Finish to clean friend data...")
                print("File Name:", self.FRIEND_DETAIL_LIST_FILE_NAME)
            self.friend_df = friend_df
            return True
        except BaseException as e:
            self.format_error(e, "Failed to parse friend_info")
            return False

    def get_friend_total_num(self):
        self.load_friend_data()
        friend_total_num = len(self.friend_list)
        return friend_total_num

    def calculate_friend_num_timeline(self, timestamp, friend_df):
        """
        :param timestamp: 传入时间戳
        :return: 用户在给定时间点的好友数量
        """
        friend_total_num = friend_df.shape[0]
        friend_df_time = friend_df[friend_df['add_friend_time'] > timestamp]
        friend_time_num = friend_total_num - friend_df_time.shape[0]
        if self.debug:
            print(util.get_standard_time_from_mktime(timestamp), friend_time_num)
        return friend_time_num

    def get_friend_result_file_name(self):
        return self.FRIEND_DETAIL_LIST_FILE_NAME

    def get_most_common_friend(self):
        if self.friend_df.empty:
            try:
                self.friend_df = pd.read_csv(self.FRIEND_DETAIL_LIST_FILE_NAME)
            except FileNotFoundError:
                self.clean_friend_data()

        max_index = self.friend_df['common_friend_num'].max()
        most_friend = self.friend_df.loc[self.friend_df['common_friend_num'] == max_index, ['common_friend_num', 'nick_name']].values[0]
        self.user_info.most_common_friend_num = most_friend[0]
        self.user_info.most_friend = most_friend[1]

    def get_most_group(self):
        if self.friend_df.empty:
            try:
                self.friend_df = pd.read_csv(self.FRIEND_DETAIL_LIST_FILE_NAME)
            except FileNotFoundError:
                self.clean_friend_data()
        self.friend_df.fillna('', inplace=True)
        common_group_names = self.friend_df['common_group_names']
        common_group_names_list = []
        for item in common_group_names:
            if item != '':
                try:
                    if type(item) != list:
                        item = json.loads(item.replace('\'', '\"'))
                    common_group_names_list.extend(item)
                except:
                    pass

        if len(common_group_names_list) > 0:
            df = pd.DataFrame(common_group_names_list)
            df['count'] = 1
            result = df.groupby(by='name').agg({'count': sum}).reset_index()
            most_group = result.loc[result['count'] == result['count'].max(), :].values[0]

            self.user_info.most_group = most_group[0]
            self.user_info.most_group_member = most_group[1]
            print(most_group)

    def get_first_friend_info(self):
        if self.friend_df.empty:
            try:
                self.friend_df = pd.read_csv(self.FRIEND_DETAIL_LIST_FILE_NAME)
            except FileNotFoundError:
                self.clean_friend_data()
        self.get_single_friend()
        # self.user_info.friend_num = self.friend_df.shape[0]
        zero_index = self.friend_df[self.friend_df['add_friend_time'] == 0].index
        self.friend_df.drop(index=zero_index, axis=0, inplace=True)
        self.friend_df.reset_index(inplace=True)
        early_time = util.get_standard_time_from_mktime(self.friend_df.loc[0,'add_friend_time'])

        early_nick = self.friend_df.loc[0, 'nick_name']
        first_header_url = self.FRIEND_HEADER_IMAGE_PATH + str(int(self.friend_df.loc[0, 'friend_uin'])) + '.jpg'

        self.user_info.first_friend = early_nick
        self.user_info.first_friend_time = util.get_standard_time_with_name(early_time)
        self.user_info.first_friend_header = first_header_url
        self.user_info.save_user()

    def get_single_friend(self):
        single_friend = self.friend_df[self.friend_df['uin'] == 0].shape[0]
        self.user_info.single_friend = single_friend


if __name__ == '__main__':
    friend_spider = QQZoneFriendSpider(use_redis=True, debug=True, analysis=False)
    friend_spider.get_friend_detail()
    friend_spider.download_head_image()
    friend_spider.clean_friend_data()
    friend_spider.get_first_friend_info()
    # friend_spider.calculate_friend_num_timeline(1411891250)

