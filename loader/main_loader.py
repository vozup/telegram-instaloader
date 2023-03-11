from pathlib import Path

from instaloader import *


def is_shortcode(shortcode: str):
    if shortcode.startswith('http'):
        return False
    if len(shortcode) != 11:
        print("Shortcode is incorrect")
        raise Exception("Invalid shortcode")
    return True


def get_shortcode(http_link: str):
    # Check if http_link is already shortcode
    if is_shortcode(http_link):
        return http_link
    else:
        # Get shortcode from http link
        shortcode = http_link.split('/')[4]
        if len(shortcode) != 11:
            print("Shortcode is incorrect")
            raise Exception("Invalid shortcode")
        return shortcode


class Loader:
    def __init__(self, download_video_thumbnails=False, save_metadata=False,
                 post_metadata_txt_pattern="", base_download_path="D:\\InstaDownloads\\"):
        self.instance = Instaloader(download_video_thumbnails=download_video_thumbnails,
                                    save_metadata=save_metadata,
                                    post_metadata_txt_pattern=post_metadata_txt_pattern)
        self.base_download_path = base_download_path

    def get_post(self, shortcode: str):
        return Post.from_shortcode(self.instance.context, get_shortcode(shortcode))

    def download_post(self, shortcode: str, dir_name: str = None):
        """
        Download post by shortcode
        :param shortcode: may be shortcode or http link to post
        :param dir_name: template dirname for downloded media
        :return: True if something was downloaded, False otherwise, i.e. file was already there
        """
        shortcode = get_shortcode(shortcode)
        post = self.get_post(shortcode)
        if not dir_name:
            dir_name = Path(self.base_download_path + post.owner_username)
        return self.instance.download_post(post, target=dir_name)

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
