from pybb.permissions import DefaultPermissionHandler


class ForumPermissionHandler(DefaultPermissionHandler):
    def may_post_as_admin(self, user):
        """ return True if `user` may post as admin """
        return False
