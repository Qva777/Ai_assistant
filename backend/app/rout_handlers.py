import re
import requests
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from config import Config


class AIHandler:
    """ Make TextLoader and index """

    def __init__(self):
        self.loader = TextLoader("dataset/data.txt")
        self.index = VectorstoreIndexCreator().from_loaders([self.loader])

    def handle(self, response):
        """ Make request to AI API using simple data set """
        response_str = str(response)
        query_result = self.index.query(response_str)
        return query_result


class LinkOpener:
    """ Make a request to the specified link """

    @staticmethod
    def open_link(link, username):
        url = f'{link}{username}'
        headers = {'accept': 'application/json', 'Token': f'{Config.TOKEN}'}
        response = requests.get(url, headers=headers)
        return response.json()


class Parser:
    """ Parse json response """

    @staticmethod
    def extract_info_user_message(user_message):
        """ Extract the nickname|links from the user message """

        # Find @username|link in the user message
        pattern = r'(@\w+(?:\.\w+)*)|\b(?:sound|music|track|song)\b'
        matches = re.findall(pattern, user_message)

        # Dict that will be sent to AI
        result = {'user_message': user_message, 'data': []}

        for match in matches:
            # Extracted username
            if match.startswith('@'):

                username = match[1:]

                # Make request to remote db
                response = LinkOpener.open_link(Config.url_search_usr, username)

                # Extract user data from the response
                Parser.extract_data(username, response, result)

            else:
                ai_handler = AIHandler()
                query_result = ai_handler.handle(user_message)

                # Search integer (days)
                pattern = r'\b\d+\b\s*'
                matches = re.findall(pattern, query_result)

                if matches:
                    days = int(matches[0])
                    response = LinkOpener.open_link(Config.url_sound, days)

                    # Extract music data from the response
                    Parser.extract_music_data(response, result)

        return result

    @staticmethod
    def extract_data(username, response, result):
        """ Extracts relevant data from the response for the given username """

        for author in response['data']['stats']:
            if author['uniqueId'] == username:
                return Parser.extract_author_data(author, result)
        return None

    @staticmethod
    def extract_author_data(author, result):
        """  Extract detail fields from the author's data '"""

        # Open detail info about user
        data = LinkOpener.open_link(Config.url_search_usr_id, author["authorId"])

        # Get main info
        most_popular_hashtag = max(data["hashtags"], key=lambda x: x["count"])
        most_popular_video = max(data["videos"], key=lambda x: x["likes"])
        least_popular_video = min(data["videos"], key=lambda x: x["likes"])
        trend_views = data["calculations"]["trendViews"]
        trend_likes = data["calculations"]["trendLikes"]
        trend_comments = data["calculations"]["trendComments"]
        trend_shares = data["calculations"]["trendShares"]
        effective_rate = data["calculations"]["effectiveRate"]
        number_of_comments = data["calculations"]["numberOfComments"]
        comments_per_1000_likes = data["calculations"]["numberOfCommentsPer1000Likes"]
        count_mention_authors = len(data["mentionAuthors"])
        most_location_data_popular = max(data["locationData"], key=lambda x: x["rate"])
        least_location_data_popular = min(data["locationData"], key=lambda x: x["rate"])
        most_categories_popular = max(data["categories"], key=lambda x: x["count"])
        least_categories_popular = min(data["categories"], key=lambda x: x["count"])
        author_avg_subs_daily_rise = data["authorAvgSubsDailyRise"]

        # Add in dict
        required_data = {
            'authorId': author['authorId'],
            'uniqueId': author['uniqueId'],
            'subscribers': author['subscribers'],
            'subscribedAt': author['subscribedAt'],
            'clips': author['clips'],
            'likes': author['likes'],
            'diggCount': author['diggCount'],
            "Most popular hashtag": most_popular_hashtag,
            "Hashtags Count": most_popular_hashtag,
            "Most popular Video": f"{Config.url_base_video}{most_popular_video['videoId']}",
            "Number of likes of the most popular video": f"{Config.url_base_video}{most_popular_video['videoId']}",
            "Least popular Video": f"{Config.url_base_video}{least_popular_video['videoId']}",
            "Number of likes of the least popular video": f"{Config.url_base_video}{least_popular_video['videoId']}",
            "Trend Views": trend_views,
            "Trend Likes": trend_likes,
            "Trend Comments": trend_comments,
            "Trend Shares": trend_shares,
            "Effective Rate": effective_rate,
            "Number of Comments": number_of_comments,
            "Number of Comments Per 1000 Likes": comments_per_1000_likes,
            "Count mention authors": count_mention_authors,
            "Most popular use of location": most_location_data_popular,
            "Least popular use of location": least_location_data_popular,
            "Most popular use of categories": most_categories_popular,
            "Least popular use of categories": least_categories_popular,
            "Average daily subscriber growth": author_avg_subs_daily_rise,
        }
        result['data'].append(required_data)
        return result

    @staticmethod
    def extract_music_data(response, result):
        """ Extract music fields """
        if response['data']['stats']:
            first_entry = response['data']['stats'][0]

            music_info = first_entry['music']
            music_id = music_info.get('musicId')
            reposts = music_info.get('reposts')
            url = music_info.get('url')
            title = music_info.get('title')
            creator = music_info.get('creator')

            result_songs = {

                "Music id": music_id,
                "Title": title,
                "Creator": creator,
                "Reposts": reposts,
                "Url": url,
            }

            result['data'].append(result_songs)
            return result
