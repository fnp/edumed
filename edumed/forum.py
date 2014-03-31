from pybb.permissions import DefaultPermissionHandler


class ForumPermissionHandler(DefaultPermissionHandler):
    def may_post_as_admin(self, user):
        """ return True if `user` may post as admin """
        return False

    def may_create_topic(self, user, forum):
        """ return True if `user` is allowed to create a new topic in `forum` """
        return user.is_authenticated()

    def may_create_post(self, user, topic):
        """ return True if `user` is allowed to create a new post in `topic` """

        if topic.forum.hidden and (not user.is_staff):
            # if topic is hidden, only staff may post
            return False

        if topic.closed and (not user.is_staff):
            # if topic is closed, only staff may post
            return False

        return user.is_authenticated()
        