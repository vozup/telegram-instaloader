from pathlib import Path
from common.config import Config
from common.common import site_name

from instaloader import *


def is_shortcode(shortcode: str):
    if shortcode.startswith('http'):
        return False
    if len(shortcode) != 11:
        print("Shortcode is incorrect")
        raise Exception("Invalid shortcode")
    return True


def get_post_shortcode(http_link: str):
    # Check if http_link is already shortcode
    if is_shortcode(http_link):
        return http_link
    else:
        # Get shortcode from http link
        if site_name(http_link)[1] != "instagram":
            raise Exception(f"Link: {http_link} to non instagram site!")

        splited = http_link.split('/')
        if len(splited) < 5:
            raise Exception('Wrong http link to post')

        shortcode = http_link.split('/')[4]
        if len(shortcode) != 11:
            raise Exception(f"Shortcode: {shortcode} is incorrect")
        return shortcode


class Loader:
    def __init__(self):
        download_video_thumbnails = Config().get_instaloader_param('download_video_thumbnails')
        save_metadata = Config().get_instaloader_param('save_metadata')
        post_metadata_txt_pattern = Config().get_instaloader_param('post_metadata_txt_pattern')
        base_download_path = Config().get_instaloader_param('base_download_path')
        filename_pattern = Config().get_instaloader_param('filename_pattern')

        self.instance = Instaloader(download_video_thumbnails=download_video_thumbnails,
                                    save_metadata=save_metadata,
                                    post_metadata_txt_pattern=post_metadata_txt_pattern,
                                    filename_pattern=filename_pattern)
        self.base_download_path = base_download_path

    def get_post(self, shortcode: str):
        return Post.from_shortcode(self.instance.context, get_post_shortcode(shortcode))

    def download_post(self, shortcode: str, dir_name: str = None):
        """
        Download post by shortcode
        :param shortcode: may be shortcode or http link to post
        :param dir_name: template dirname for downloded media
        :return: True if something was downloaded, False otherwise, i.e. file was already there
        """
        shortcode = get_post_shortcode(shortcode)
        post = self.get_post(shortcode)
        if not dir_name:
            dir_name = post.owner_username
        return self.instance.download_post(post, target=Path(self.base_download_path + dir_name))

    def download_all_posts(self, username: str, dir_name: str = None):
        """
        Download all post from username account
        :param username: insta username
        :param dir_name: template dirname for downloded media
        :return:
        """
        if not dir_name:
            dir_name = Path(self.base_download_path + username)
        profile = Profile.from_username(self.instance.context, username)
        print(f"{profile.username} total posts: {profile.get_posts().count}")
        for post in profile.get_posts():
            self.instance.download_post(post, target=dir_name)
