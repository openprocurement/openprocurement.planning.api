# -*- coding: utf-8 -*-

from pyramid.security import (
    ALL_PERMISSIONS,
    Allow,
    Everyone,
)


class Root(object):
    __name__ = None
    __parent__ = None
    __acl__ = [
        (Allow, Everyone, 'view_plan'),
        (Allow, 'g:brokers', 'create_plan'),
        (Allow, 'g:brokers', 'edit_plan'),
        (Allow, 'g:Administrator', 'edit_plan'),
        (Allow, 'g:admins', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request
        from openprocurement.planning.api.utils import get_db
        self.db = get_db(request.registry)


def factory(request):
    request.validated['plan_src'] = {}
    root = Root(request)
    if not request.matchdict or not request.matchdict.get('plan_id'):
        return root
    request.validated['plan_id'] = request.matchdict['plan_id']
    plan = request.plan
    plan.__parent__ = root
    request.validated['plan'] = plan
    if request.method != 'GET':
        request.validated['plan_src'] = plan.serialize('plain')

    request.validated['id'] = request.matchdict['plan_id']
    return plan
